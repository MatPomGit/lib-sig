"""Minimal causal finite impulse response filters."""

from .fir import fir_filter, moving_average

__all__ = ["fir_filter", "moving_average"]
