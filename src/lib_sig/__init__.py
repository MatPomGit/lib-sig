"""Small, dependency-free contracts for numerical and measured signals."""

from .core import ChannelDescriptor, SignalBlock, SignalValidationError, TimeAxis

__all__ = ["ChannelDescriptor", "SignalBlock", "SignalValidationError", "TimeAxis"]
