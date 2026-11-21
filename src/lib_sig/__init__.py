"""Sampled signals, causal FIR operations and optional NumPy spectral analysis."""

from .core import ChannelDescriptor, SignalBlock, SignalValidationError, TimeAxis
from .filters import fir_filter, moving_average
from .spectral import SpectralEstimate, periodogram_psd, rfft_spectrum

__all__ = [
    "ChannelDescriptor", "SignalBlock", "SignalValidationError",
    "TimeAxis", "fir_filter", "moving_average",
    "SpectralEstimate", "periodogram_psd", "rfft_spectrum",
]
