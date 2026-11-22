"""Core sampled-signal types and dependency-free causal FIR operations."""

from .core import ChannelDescriptor, SignalBlock, SignalValidationError, TimeAxis, TransformProvenance
from .filters import fir_filter, moving_average
from .spectral import SpectralEstimate, periodogram_psd, rfft_spectrum

__all__ = [
    "ChannelDescriptor", "SignalBlock", "SignalValidationError",
    "TimeAxis", "TransformProvenance", "fir_filter", "moving_average",
    "SpectralEstimate", "periodogram_psd", "rfft_spectrum",
]
