"""Deterministic core-contract tests: no hardware, network or model access."""

from dataclasses import FrozenInstanceError
import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from lib_sig import ChannelDescriptor, SignalBlock, SignalValidationError, TimeAxis


class SignalCoreTests(unittest.TestCase):
    def setUp(self):
        self.channels = (ChannelDescriptor("x", "m/s²"), ChannelDescriptor("y", "m/s²"))
        self.axis = TimeAxis("regular", "monotonic", start_s=1.0, sampling_rate_hz=50.0)

    def block(self, **changes):
        options = dict(samples=((1.0, 2.0), (3.0, 4.0)), channels=self.channels,
                       time_axis=self.axis, source_id="imu/synthetic")
        options.update(changes)
        return SignalBlock(**options)

    def test_regular_axis_count_and_timestamps(self):
        block = self.block()
        self.assertEqual((block.sample_count, block.channel_count), (2, 2))
        self.assertAlmostEqual(block.timestamp_at(1), 1.02)
        with self.assertRaises(IndexError):
            block.timestamp_at(2)
        with self.assertRaises(IndexError):
            block.timestamp_at(True)

    def test_irregular_axis_and_nonuniform_timestamps(self):
        axis = TimeAxis("irregular", "sensor", timestamps_s=(1.0, 1.015, 1.08))
        block = self.block(time_axis=axis, samples=((1., 2.), (3., 4.), (5., 6.)))
        self.assertEqual(block.timestamp_at(2), 1.08)
        self.assertIsNone(axis.sampling_rate_hz)

    def test_invalid_regular_axis(self):
        cases = [dict(start_s=math.nan, sampling_rate_hz=10.),
                 dict(start_s=0., sampling_rate_hz=0.),
                 dict(start_s=0., sampling_rate_hz=True),
                 dict(start_s=0., sampling_rate_hz=10., timestamps_s=(1.,)),
                 dict(start_s=0., sampling_rate_hz=math.inf)]
        for case in cases:
            with self.subTest(case=case), self.assertRaises(SignalValidationError) as exc:
                TimeAxis("regular", "monotonic", **case)
            self.assertEqual(exc.exception.code, "TIMEBASE_MISMATCH")

    def test_invalid_irregular_axis(self):
        for stamps in ((), (2., 1.), (1., 1.), (math.nan,), [1., 2.], (0., math.inf)):
            with self.subTest(stamps=stamps), self.assertRaises(SignalValidationError) as exc:
                TimeAxis("irregular", "sensor", timestamps_s=stamps)
            self.assertEqual(exc.exception.code, "IRREGULAR_SAMPLING")

    def test_no_implicit_channel_units(self):
        for name, unit in (("", "V"), ("eeg", ""), ("eeg", None)):
            with self.subTest(name=name, unit=unit), self.assertRaises(SignalValidationError):
                ChannelDescriptor(name, unit)

    def test_reject_non_rectangular_and_non_tuple_rows(self):
        for samples in (((1.,), (2., 3.)), [[1., 2.], [3., 4.]], (), ((1., 2.), [3., 4.])):
            with self.subTest(samples=samples), self.assertRaises(SignalValidationError) as exc:
                self.block(samples=samples)
            self.assertEqual(exc.exception.code, "INVALID_SHAPE")

    def test_reject_duplicate_channels(self):
        with self.assertRaises(SignalValidationError):
            self.block(channels=(ChannelDescriptor("X", "m"), ChannelDescriptor("x", "m")))

    def test_incomplete_irregular_axis_fails_closed(self):
        axis = TimeAxis("irregular", "monotonic", timestamps_s=(1.,))
        with self.assertRaises(SignalValidationError) as exc:
            self.block(time_axis=axis)
        self.assertEqual(exc.exception.code, "TIMEBASE_MISMATCH")

    def test_unmasked_nonfinite_is_data_loss(self):
        for value in (math.nan, math.inf, -math.inf):
            with self.subTest(value=value), self.assertRaises(SignalValidationError) as exc:
                self.block(samples=((value, 1.), (2., 3.)))
            self.assertEqual(exc.exception.code, "DATA_LOSS")

    def test_extremely_large_integer_is_rejected_as_nonfinite(self):
        with self.assertRaises(SignalValidationError) as exc:
            self.block(samples=((10**1000, 1.), (2., 3.)))
        self.assertEqual(exc.exception.code, "DATA_LOSS")

    def test_masked_nonfinite_data_is_explicit(self):
        block = self.block(samples=((math.nan, 1.), (2., 3.)),
                           mask=((False, True), (True, True)))
        self.assertTrue(math.isnan(block.samples[0][0]))
        self.assertFalse(block.mask[0][0])

    def test_mask_must_match_shape_and_booleans(self):
        for mask in (((True,), (False,)), ((True, 1), (True, True)),
                     ((True, True),), [[True, True], [True, True]]):
            with self.subTest(mask=mask), self.assertRaises(SignalValidationError) as exc:
                self.block(mask=mask)
            self.assertEqual(exc.exception.code, "INVALID_SHAPE")

    def test_reject_bool_samples(self):
        with self.assertRaises(SignalValidationError):
            self.block(samples=((True, 2.), (3., 4.)))

    def test_public_contract_is_immutable(self):
        block = self.block()
        with self.assertRaises(FrozenInstanceError):
            block.source_id = "other"
        with self.assertRaises(TypeError):
            block.samples[0][0] = 5.


if __name__ == "__main__":
    unittest.main()
