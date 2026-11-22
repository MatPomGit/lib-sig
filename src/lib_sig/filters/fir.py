"""Finite, causal, valid-mode FIR filtering of sampled signal blocks.

A small dependency-free reference operation; not an FFT or resampling engine.
"""

from __future__ import annotations

import json
import math
from numbers import Real

from ..core import SignalBlock, SignalValidationError, TimeAxis, TransformProvenance


# A conservative bound for the pure-Python reference implementation.
MAX_FIR_MACS = 1_000_000


def _check_budget(block: SignalBlock, order: int) -> None:
    operations = (block.sample_count - order + 1) * order * block.channel_count
    if operations > MAX_FIR_MACS:
        raise SignalValidationError(
            "RESOURCE_LIMIT",
            f"FIR needs {operations} multiply-accumulates; limit is {MAX_FIR_MACS}",
        )


def fir_filter(block: SignalBlock, taps: tuple[float, ...]) -> SignalBlock:
    """Filter complete causal windows and record the exact coefficients."""
    return _apply_fir(block, taps, operation="fir", window=None)


def _apply_fir(
    block: SignalBlock, taps: tuple[float, ...], *, operation: str, window: int | None
) -> SignalBlock:
    """Return a causal, unpadded FIR result.

    taps[0] multiplies the current sample; taps[k] multiplies sample n-k.
    Only complete windows are produced (valid mode). Each output is stamped
    with the observation time of the newest sample in its input window.

    Missing input values invalidate every output window containing them;
    they are represented as NaN with mask=False, never silently interpolated.
    Sampling must be regular. Output units, channels and source are unchanged.
    """
    if not isinstance(block, SignalBlock):
        raise SignalValidationError("INVALID_SHAPE", "block must be a SignalBlock")
    if type(taps) is not tuple or not taps or len(taps) > block.sample_count:
        raise SignalValidationError(
            "INVALID_FILTER", "taps must be a nonempty tuple no longer than the signal"
        )
    # Reject unaffordable requests before converting potentially huge coefficients.
    order = len(taps)
    _check_budget(block, order)
    coefficients = []
    for tap in taps:
        if isinstance(tap, bool) or not isinstance(tap, Real):
            raise SignalValidationError("INVALID_FILTER", "taps must be real finite numbers")
        try:
            coefficient = float(tap)
        except (OverflowError, ValueError, TypeError) as exc:
            raise SignalValidationError("INVALID_FILTER", "tap is not representable") from exc
        if not math.isfinite(coefficient):
            raise SignalValidationError("INVALID_FILTER", "taps must be finite")
        coefficients.append(coefficient)

    if block.time_axis.kind != "regular":
        raise SignalValidationError("IRREGULAR_SAMPLING", "FIR requires regular sampling")

    output_rows = []
    output_mask = [] if block.mask is not None else None
    for newest in range(order - 1, block.sample_count):
        values, flags = [], []
        for ch in range(block.channel_count):
            if block.mask is not None and any(
                not block.mask[newest - k][ch] for k in range(order)
            ):
                values.append(float("nan"))
                flags.append(False)
                continue
            try:
                value = math.fsum(
                    coefficients[k] * block.samples[newest - k][ch]
                    for k in range(order)
                )
            except (OverflowError, ValueError) as exc:
                raise SignalValidationError(
                    "DATA_LOSS", "FIR calculation overflowed or became indeterminate"
                ) from exc
            if not math.isfinite(value):
                raise SignalValidationError("DATA_LOSS", "FIR output is not finite")
            values.append(value)
            flags.append(True)
        output_rows.append(tuple(values))
        if output_mask is not None:
            output_mask.append(tuple(flags))

    output_time = TimeAxis(
        kind="regular",
        timebase=block.time_axis.timebase,
        start_s=block.timestamp_at(order - 1),
        sampling_rate_hz=block.time_axis.sampling_rate_hz,
    )
    parameters = {"taps": coefficients}
    if window is not None:
        parameters["window"] = window
    record = TransformProvenance(
        operation=operation,
        parameters_json=json.dumps(parameters, separators=(",", ":"), allow_nan=False),
        input_sample_count=block.sample_count,
        output_sample_count=len(output_rows),
        timestamp_policy="newest_input_sample",
        missing_policy="invalidate_complete_window_per_channel",
        # General FIR filters need not have linear phase.
        group_delay_s=((order - 1) / (2 * block.time_axis.sampling_rate_hz))
        if window is not None else None,
    )
    return SignalBlock(
        samples=tuple(output_rows),
        channels=block.channels,
        time_axis=output_time,
        source_id=block.source_id,
        mask=tuple(output_mask) if output_mask is not None else None,
        provenance=block.provenance + (record,),
    )


def moving_average(block: SignalBlock, window: int) -> SignalBlock:
    """Causal boxcar smoothing with a complete window and unchanged units.

    The filter has weights 1/window, a DC gain of one and a lag of
    (window-1)/2 samples relative to the window centre. Timestamp represents
    the newest input sample (causal output), not its effective group delay.
    """
    if type(window) is not int or window < 1:
        raise SignalValidationError("INVALID_FILTER", "window must be a positive integer")
    if not isinstance(block, SignalBlock):
        raise SignalValidationError("INVALID_SHAPE", "block must be a SignalBlock")
    if window > block.sample_count:
        raise SignalValidationError("INVALID_FILTER", "window exceeds available samples")
    _check_budget(block, window)
    return _apply_fir(
        block, (1.0 / window,) * window, operation="moving_average", window=window
    )
