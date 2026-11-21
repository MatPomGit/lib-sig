"""Core sampled-signal types and dependency-free causal FIR operations."""

from .core import ChannelDescriptor, SignalBlock, SignalValidationError, TimeAxis
from .filters import fir_filter, moving_average

__all__ = [
    "ChannelDescriptor", "SignalBlock", "SignalValidationError",
    "TimeAxis", "fir_filter", "moving_average",
]
