"""Domain-neutral, immutable sampled-signal metadata and validation.

No device access, signal processing or storage side effects.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from numbers import Real
from typing import Literal


class SignalValidationError(ValueError):
    """Input validation error with a stable machine-readable code."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(f"{code}: {message}")


def _finite_number(value: object) -> bool:
    if not isinstance(value, Real) or isinstance(value, bool):
        return False
    try:
        return math.isfinite(value)
    except (OverflowError, ValueError, TypeError):
        return False


def _required_name(value: object, field: str, code: str = "INVALID_UNITS") -> None:
    if not isinstance(value, str) or not value.strip():
        raise SignalValidationError(code, f"{field} must be a nonempty string")


@dataclass(frozen=True, slots=True)
class ChannelDescriptor:
    """One measured channel, including its unambiguous physical unit."""

    name: str
    unit: str
    source_id: str | None = None
    calibration_ref: str | None = None
    kind: str | None = None

    def __post_init__(self) -> None:
        _required_name(self.name, "channel name", "INVALID_SHAPE")
        _required_name(self.unit, "channel unit")
        for field in ("source_id", "calibration_ref", "kind"):
            value = getattr(self, field)
            if value is not None:
                _required_name(value, field, "INVALID_SHAPE")


@dataclass(frozen=True, slots=True)
class TimeAxis:
    """Regular or irregular sampling in explicit, finite seconds."""

    kind: Literal["regular", "irregular"]
    timebase: str
    start_s: float | None = None
    sampling_rate_hz: float | None = None
    timestamps_s: tuple[float, ...] | None = None

    def __post_init__(self) -> None:
        _required_name(self.timebase, "timebase", "TIMEBASE_MISMATCH")
        if self.kind == "regular":
            if (not _finite_number(self.start_s)
                    or not _finite_number(self.sampling_rate_hz)
                    or self.sampling_rate_hz <= 0
                    or self.timestamps_s is not None):
                raise SignalValidationError(
                    "TIMEBASE_MISMATCH", "regular time axis needs a finite start and positive Hz, without timestamps"
                )
        elif self.kind == "irregular":
            stamps = self.timestamps_s
            if (self.start_s is not None or self.sampling_rate_hz is not None
                    or type(stamps) is not tuple or not stamps
                    or any(not _finite_number(t) for t in stamps)
                    or any(b <= a for a, b in zip(stamps, stamps[1:]))):
                raise SignalValidationError(
                    "IRREGULAR_SAMPLING", "timestamps must be a nonempty, strictly increasing tuple of finite seconds"
                )
        else:
            raise SignalValidationError("TIMEBASE_MISMATCH", "time axis kind must be regular or irregular")

    def timestamp_at(self, index: int) -> float:
        if type(index) is not int or index < 0:
            raise IndexError("sample index must be a nonnegative integer")
        if self.kind == "regular":
            try:
                stamp = self.start_s + index / self.sampling_rate_hz
            except (OverflowError, ZeroDivisionError) as error:
                raise SignalValidationError("TIMEBASE_MISMATCH", "timestamp cannot be represented") from error
            if not math.isfinite(stamp):
                raise SignalValidationError("TIMEBASE_MISMATCH", "timestamp cannot be represented")
            return stamp
        return self.timestamps_s[index]


@dataclass(frozen=True, slots=True)
class TransformProvenance:
    """Immutable, machine-readable record of one signal transformation."""

    operation: str
    parameters_json: str
    input_sample_count: int
    output_sample_count: int
    timestamp_policy: str
    missing_policy: str
    group_delay_s: float | None = None

    def __post_init__(self) -> None:
        _required_name(self.operation, "operation", "INVALID_SHAPE")
        _required_name(self.timestamp_policy, "timestamp_policy", "INVALID_SHAPE")
        _required_name(self.missing_policy, "missing_policy", "INVALID_SHAPE")
        if not isinstance(self.parameters_json, str) or not self.parameters_json:
            raise SignalValidationError("INVALID_SHAPE", "parameters_json must not be empty")
        if (type(self.input_sample_count) is not int or self.input_sample_count < 1
                or type(self.output_sample_count) is not int or self.output_sample_count < 1):
            raise SignalValidationError("INVALID_SHAPE", "transform sample counts must be positive integers")
        if self.group_delay_s is not None and not _finite_number(self.group_delay_s):
            raise SignalValidationError("INVALID_SHAPE", "group delay must be finite when specified")


@dataclass(frozen=True, slots=True)
class SignalBlock:
    """Channels are columns; rows are samples. True in mask means valid."""

    samples: tuple[tuple[float, ...], ...]
    channels: tuple[ChannelDescriptor, ...]
    time_axis: TimeAxis
    source_id: str
    mask: tuple[tuple[bool, ...], ...] | None = None
    provenance: tuple[TransformProvenance, ...] = ()

    def __post_init__(self) -> None:
        _required_name(self.source_id, "source_id", "INVALID_SHAPE")
        if type(self.channels) is not tuple or not self.channels or any(
            not isinstance(ch, ChannelDescriptor) for ch in self.channels
        ):
            raise SignalValidationError("INVALID_SHAPE", "channels must be a nonempty tuple of ChannelDescriptor")
        names = [ch.name.casefold() for ch in self.channels]
        if len(set(names)) != len(names):
            raise SignalValidationError("INVALID_SHAPE", "channel names must be unique")
        if not isinstance(self.time_axis, TimeAxis):
            raise SignalValidationError("TIMEBASE_MISMATCH", "time_axis must be a TimeAxis")
        count = len(self.channels)
        if (type(self.samples) is not tuple or not self.samples
                or any(type(row) is not tuple or len(row) != count for row in self.samples)):
            raise SignalValidationError("INVALID_SHAPE", "samples must be a nonempty tuple of fixed-width rows")
        if self.time_axis.kind == "irregular" and len(self.time_axis.timestamps_s) != len(self.samples):
            raise SignalValidationError("TIMEBASE_MISMATCH", "timestamp count must equal sample count")
        if type(self.provenance) is not tuple or any(
            not isinstance(record, TransformProvenance) for record in self.provenance
        ):
            raise SignalValidationError("INVALID_SHAPE", "provenance must be a tuple of TransformProvenance")
        if self.mask is not None:
            if (type(self.mask) is not tuple or len(self.mask) != len(self.samples)
                    or any(type(row) is not tuple or len(row) != count
                           or any(type(flag) is not bool for flag in row) for row in self.mask)):
                raise SignalValidationError("INVALID_SHAPE", "mask must match samples and contain only booleans")
        previous_timestamp = None
        for i, row in enumerate(self.samples):
            if self.time_axis.kind == "regular":
                timestamp = self.time_axis.timestamp_at(i)
                if previous_timestamp is not None and timestamp <= previous_timestamp:
                    raise SignalValidationError(
                        "TIMEBASE_MISMATCH",
                        "sample period is not representable at this timebase precision",
                    )
                previous_timestamp = timestamp
            for j, value in enumerate(row):
                # Invalid measurements require an explicit mask; they are not silently coerced.
                if not isinstance(value, Real) or isinstance(value, bool):
                    raise SignalValidationError("INVALID_SHAPE", "samples must be numeric, not boolean")
                if not _finite_number(value) and (self.mask is None or self.mask[i][j]):
                    raise SignalValidationError("DATA_LOSS", "nonfinite samples require a false mask flag")

    @property
    def sample_count(self) -> int:
        return len(self.samples)

    @property
    def channel_count(self) -> int:
        return len(self.channels)

    def timestamp_at(self, index: int) -> float:
        if type(index) is not int or not 0 <= index < self.sample_count:
            raise IndexError("sample index out of range")
        return self.time_axis.timestamp_at(index)
