"""Real-input FFT and one-sided periodogram spectral-density estimates.

NumPy performs the FFT. No home-grown FFT engine, implicit resampling,
missing-data interpolation, or automatic external service access.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
from typing import Literal

from ..core import ChannelDescriptor, SignalBlock, SignalValidationError, TransformProvenance


@dataclass(frozen=True, slots=True)
class SpectralEstimate:
    """Immutable result with bin-major values: values[frequency][channel].

    kind='rfft': unnormalised complex DFT, units equal to input units.
    kind='psd': one-sided power spectral density, units input_unit²/Hz.
    """

    frequencies_hz: tuple[float, ...]
    values: tuple[tuple[complex | float, ...], ...]
    channels: tuple[ChannelDescriptor, ...]
    units: tuple[str, ...]
    kind: Literal["rfft", "psd"]
    window: Literal["boxcar", "hann"]
    detrend: Literal["none", "constant"]
    sample_count: int
    sampling_rate_hz: float
    source_id: str
    timebase: str
    start_s: float
    provenance: tuple[TransformProvenance, ...]


# Estimated temporary arrays and Python result objects; not a hard RSS bound.
MAX_SPECTRAL_ESTIMATED_BYTES = 64 * 1024 * 1024


def _check_spectral_budget(block: SignalBlock) -> None:
    n, channels = block.sample_count, block.channel_count
    bins = n // 2 + 1
    # Input, detrended/windowed buffers, FFT, PSD, and boxed output tuples.
    estimated = (24 * n * channels + 8 * n + 96 * bins * channels + 24 * bins)
    if estimated > MAX_SPECTRAL_ESTIMATED_BYTES:
        raise SignalValidationError(
            "RESOURCE_LIMIT",
            f"estimated spectral buffers need {estimated} bytes; limit is {MAX_SPECTRAL_ESTIMATED_BYTES}",
        )


def _prepare(
    block: SignalBlock,
    window: str,
    detrend: str,
):
    """Validate the measurement contract and prepare float64 input.

    NumPy is loaded lazily: users of the core/FIR modules do not need it.
    """
    if not isinstance(block, SignalBlock):
        raise SignalValidationError("INVALID_SHAPE", "block must be a SignalBlock")
    if block.time_axis.kind != "regular":
        raise SignalValidationError("IRREGULAR_SAMPLING", "FFT and PSD require regular sampling")
    if block.sample_count < 2:
        raise SignalValidationError("INVALID_SPECTRUM", "at least two samples are required")
    if window not in ("boxcar", "hann") or type(window) is not str:
        raise SignalValidationError("INVALID_SPECTRUM", "window must be boxcar or hann")
    if detrend not in ("none", "constant") or type(detrend) is not str:
        raise SignalValidationError("INVALID_SPECTRUM", "detrend must be none or constant")
    if block.mask is not None and any(not all(row) for row in block.mask):
        raise SignalValidationError("DATA_LOSS", "missing samples must be resolved explicitly")
    _check_spectral_budget(block)

    try:
        import numpy as np
    except ImportError as exc:
        raise SignalValidationError(
            "DEPENDENCY_UNAVAILABLE", "spectral operations require NumPy"
        ) from exc

    try:
        try:
            samples = np.asarray(block.samples, dtype=np.float64)
        except (ValueError, TypeError, OverflowError) as exc:
            raise SignalValidationError("DATA_LOSS", "samples cannot be represented as float64") from exc
        if samples.shape != (block.sample_count, block.channel_count) or not np.isfinite(samples).all():
            raise SignalValidationError("DATA_LOSS", "samples contain unrepresentable values")
    
        n = block.sample_count
        if window == "boxcar":
            weights = np.ones(n, dtype=np.float64)
        else:
            # Periodic (DFT-even) Hann window, matching scipy.signal.get_window.
            weights = np.hanning(n + 1)[:-1]
        if detrend == "constant":
            with np.errstate(over="ignore", invalid="ignore"):
                samples = samples - samples.mean(axis=0, keepdims=True)
        if not np.isfinite(samples).all():
            raise SignalValidationError("DATA_LOSS", "detrending produced invalid values")
    
        fs = float(block.time_axis.sampling_rate_hz)
        spacing = 1.0 / fs
        if not math.isfinite(spacing) or spacing <= 0:
            raise SignalValidationError("INVALID_SPECTRUM", "sampling interval is not representable")
        try:
            with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
                bins = np.fft.rfftfreq(n, d=spacing)
                spectrum = np.fft.rfft(samples * weights[:, None], axis=0)
        except (ValueError, OverflowError, FloatingPointError) as exc:
            raise SignalValidationError("DATA_LOSS", "FFT computation failed") from exc
        if not np.isfinite(spectrum).all() or not np.isfinite(bins).all():
            raise SignalValidationError("DATA_LOSS", "FFT result is not finite")
        return np, weights, bins, spectrum
    except MemoryError as exc:
        raise SignalValidationError("RESOURCE_LIMIT", "spectral buffer allocation failed") from exc


def _result(
    block: SignalBlock,
    frequencies,
    values,
    kind: Literal["rfft", "psd"],
    window: str,
    detrend: str,
    *,
    backend_version: str,
    window_energy: float | None = None,
) -> SpectralEstimate:
    units = (
        tuple(ch.unit for ch in block.channels)
        if kind == "rfft"
        else tuple(f"{ch.unit}²/Hz" for ch in block.channels)
    )
    params = {
        "backend": "numpy.fft.rfft",
        "backend_version": backend_version,
        "window": window,
        "detrend": detrend,
        "fft_length": block.sample_count,
        "sampling_rate_hz": float(block.time_axis.sampling_rate_hz),
        "normalization": "none" if kind == "rfft" else "one_sided_density",
    }
    if kind == "psd":
        params["window_energy"] = window_energy
        params["doubling"] = "positive_bins_excluding_even_nyquist"
    record = TransformProvenance(
        operation="rfft_spectrum" if kind == "rfft" else "periodogram_psd",
        parameters_json=json.dumps(params, sort_keys=True, separators=(",", ":"), allow_nan=False),
        input_sample_count=block.sample_count,
        output_sample_count=len(frequencies),
        timestamp_policy="frequency_bins_from_sampling_rate",
        missing_policy="reject_any_missing_sample",
    )
    cast = complex if kind == "rfft" else float
    try:
        return SpectralEstimate(
            frequencies_hz=tuple(float(f) for f in frequencies),
            values=tuple(tuple(cast(v) for v in row) for row in values),
            channels=block.channels,
            units=units,
            kind=kind,
            window=window,
            detrend=detrend,
            sample_count=block.sample_count,
            sampling_rate_hz=float(block.time_axis.sampling_rate_hz),
            source_id=block.source_id,
            timebase=block.time_axis.timebase,
            start_s=block.timestamp_at(0),
            provenance=block.provenance + (record,),
        )
    except MemoryError as exc:
        raise SignalValidationError("RESOURCE_LIMIT", "spectral result materialization failed") from exc


def rfft_spectrum(
    block: SignalBlock,
    *,
    window: Literal["boxcar", "hann"] = "boxcar",
    detrend: Literal["none", "constant"] = "none",
) -> SpectralEstimate:
    """Compute an unnormalised real-input DFT (nonnegative frequencies only).

    Returns N//2 + 1 complex bins per channel, including DC and Nyquist for
    even N. No amplitude doubling, density scaling or hidden zero-padding.
    """
    np, _, frequencies, fft = _prepare(block, window, detrend)
    return _result(block, frequencies, fft, "rfft", window, detrend, backend_version=np.__version__)


def periodogram_psd(
    block: SignalBlock,
    *,
    window: Literal["boxcar", "hann"] = "boxcar",
    detrend: Literal["none", "constant"] = "constant",
) -> SpectralEstimate:
    """Compute a one-sided periodogram PSD in channel_unit²/Hz.

    For each channel P[k] = |rfft(window * data)[k]|² /
    (sampling_rate_hz * sum(window²)). Interior positive-frequency bins are
    doubled. DC and (when N is even) Nyquist are never doubled. The Hann
    window is periodic; detrending occurs before windowing.
    """
    np, weights, frequencies, fft = _prepare(block, window, detrend)
    fs = float(block.time_axis.sampling_rate_hz)
    try:
        energy = float(np.sum(weights * weights))
        scale = fs * energy
        if not math.isfinite(scale) or scale <= 0:
            raise SignalValidationError("INVALID_SPECTRUM", "PSD scaling is not finite and positive")
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            power = np.abs(fft) ** 2 / scale
            if block.sample_count % 2 == 0:
                power[1:-1, :] *= 2.0
            else:
                power[1:, :] *= 2.0
        if not np.isfinite(power).all():
            raise SignalValidationError("DATA_LOSS", "PSD cannot be represented as finite float64")
    except MemoryError as exc:
        raise SignalValidationError("RESOURCE_LIMIT", "PSD buffer allocation failed") from exc
    return _result(block, frequencies, power, "psd", window, detrend, backend_version=np.__version__, window_energy=energy)
