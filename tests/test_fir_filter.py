"""Deterministic tests of causal FIR filtering and measurement provenance."""

import json
import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from lib_sig import (
    ChannelDescriptor, SignalBlock, SignalValidationError, TimeAxis,
    TransformProvenance, fir_filter, moving_average,
)


def block(values, *, rate=10.0, start=1.0, irregular=False, mask=None):
    samples = tuple(tuple(row) for row in values)
    axis = (
        TimeAxis("irregular", "sensor", timestamps_s=tuple(start + i / rate for i in range(len(samples))))
        if irregular else TimeAxis("regular", "monotonic", start_s=start, sampling_rate_hz=rate)
    )
    return SignalBlock(
        samples=samples, channels=(ChannelDescriptor("x", "mV"), ChannelDescriptor("y", "mV")),
        time_axis=axis, source_id="synthetic/2ch", mask=mask,
    )


class FirFilterTests(unittest.TestCase):
    def test_impulse_response_and_time_alignment(self):
        signal = block(((1., 2.), (0., 2.), (0., 2.), (0., 2.)))
        result = fir_filter(signal, (0.5, 0.25))
        self.assertEqual(result.samples, ((0.25, 1.5), (0.0, 1.5), (0.0, 1.5)))
        self.assertEqual(result.sample_count, 3)
        self.assertAlmostEqual(result.timestamp_at(0), signal.timestamp_at(1))
        self.assertAlmostEqual(result.timestamp_at(2), signal.timestamp_at(3))
        self.assertEqual(result.channels, signal.channels)
        self.assertEqual(result.source_id, signal.source_id)
        self.assertEqual(result.time_axis.timebase, "monotonic")
        self.assertIsNone(result.mask)

    def test_moving_average_constant_preserves_dc_and_units(self):
        s = block(((1., -2.),) * 5)
        result = moving_average(s, 3)
        self.assertEqual(len(result.samples), 3)
        for x, y in result.samples:
            self.assertAlmostEqual(x, 1.0)
            self.assertAlmostEqual(y, -2.0)
        self.assertEqual(result.channels[0].unit, "mV")
        self.assertAlmostEqual(result.timestamp_at(0), 1.2)

    def test_two_point_moving_average_cancels_nyquist(self):
        s = block(tuple(((-1.) ** n, 8.) for n in range(8)), rate=8.0, start=0.0)
        out = moving_average(s, 2)
        for x, dc in out.samples:
            self.assertAlmostEqual(x, 0.0)
            self.assertAlmostEqual(dc, 8.0)

    def test_causal_difference_taps(self):
        s = block(((1., 3.), (2., 3.), (5., 3.)))
        out = fir_filter(s, (1., -1.))
        self.assertEqual(out.samples, ((1., 0.), (3., 0.)))

    def test_single_tap_is_identity(self):
        s = block(((2., 3.), (-4., 5.)))
        out = fir_filter(s, (1.0,))
        self.assertEqual(out.samples, s.samples)
        self.assertEqual(out.timestamp_at(0), s.timestamp_at(0))

    def test_masked_inputs_invalidate_overlapping_windows(self):
        s = block(((1., 10.), (math.nan, 10.), (3., 10.), (4., 10.)),
                  mask=((True, True), (False, True), (True, True), (True, True)))
        out = moving_average(s, 2)
        self.assertEqual(out.mask, ((False, True), (False, True), (True, True)))
        self.assertTrue(math.isnan(out.samples[0][0]))
        self.assertTrue(math.isnan(out.samples[1][0]))
        self.assertAlmostEqual(out.samples[2][0], 3.5)
        self.assertEqual(tuple(row[1] for row in out.samples), (10., 10., 10.))

    def test_all_valid_input_mask_is_retained(self):
        s = block(((2., 4.), (2., 4.)), mask=((True, True), (True, True)))
        out = moving_average(s, 2)
        self.assertEqual(out.mask, ((True, True),))
        self.assertEqual(out.samples, ((2., 4.),))

    def test_no_implicit_filtering_for_irregular_time_axis(self):
        s = block(((1., 2.), (3., 4.)), irregular=True)
        with self.assertRaises(SignalValidationError) as exc:
            moving_average(s, 2)
        self.assertEqual(exc.exception.code, "IRREGULAR_SAMPLING")

    def test_invalid_fir_coefficients_fail_closed(self):
        s = block(((1., 2.), (3., 4.)))
        bad = ((), [], (True,), (math.nan,), (math.inf,), (None,), ("1",), (10 ** 1000,), (1., 2., 3.))
        for taps in bad:
            with self.subTest(taps=str(taps)[:20]), self.assertRaises(SignalValidationError) as exc:
                fir_filter(s, taps)
            self.assertEqual(exc.exception.code, "INVALID_FILTER")

    def test_invalid_moving_average_window_fail_closed(self):
        s = block(((1., 2.), (3., 4.)))
        for w in (0, -1, True, 1.0, 3, "2", None):
            with self.subTest(window=w), self.assertRaises(SignalValidationError) as exc:
                moving_average(s, w)
            self.assertEqual(exc.exception.code, "INVALID_FILTER")

    def test_overflow_is_not_silently_masked(self):
        s = block(((1e308, 1.), (1e308, 1.)))
        with self.assertRaises(SignalValidationError) as exc:
            fir_filter(s, (2.0,))
        self.assertEqual(exc.exception.code, "DATA_LOSS")

    def test_valid_mode_reduces_length_and_preserves_causal_timestamp(self):
        s = block(tuple((float(i), float(i)) for i in range(5)), rate=20.0, start=0.0)
        out = moving_average(s, 5)
        self.assertEqual(out.sample_count, 1)
        self.assertAlmostEqual(out.timestamp_at(0), 0.2)
        self.assertEqual(out.samples, ((2.0, 2.0),))

    def test_resource_budget_rejects_expensive_fir_and_average(self):
        s = block(((1.0, 2.0),) * 2048)
        for run in (
            lambda: fir_filter(s, (1.0 / 1024,) * 1024),
            lambda: moving_average(s, 1024),
        ):
            with self.assertRaises(SignalValidationError) as exc:
                run()
            self.assertEqual(exc.exception.code, "RESOURCE_LIMIT")

    def test_budget_precedes_large_coefficient_conversion(self):
        s = block(((1.0, 2.0),) * 2048)
        # The coefficient cannot be represented as float; no conversion is
        # attempted when the declared filter already exceeds the MAC budget.
        with self.assertRaises(SignalValidationError) as exc:
            fir_filter(s, (10 ** 1000,) * 1024)
        self.assertEqual(exc.exception.code, "RESOURCE_LIMIT")

    def test_provenance_contains_exact_filter_and_is_immutable(self):
        s = block(((1.0, 2.0), (3.0, 4.0), (5.0, 6.0)))
        out = fir_filter(s, (0.75, -0.25))
        self.assertEqual(s.provenance, ())
        self.assertEqual(len(out.provenance), 1)
        record = out.provenance[0]
        self.assertIsInstance(record, TransformProvenance)
        self.assertEqual(record.operation, "fir")
        self.assertEqual(json.loads(record.parameters_json), {"taps": [0.75, -0.25]})
        self.assertEqual((record.input_sample_count, record.output_sample_count), (3, 2))
        self.assertEqual(record.timestamp_policy, "newest_input_sample")
        self.assertEqual(record.missing_policy, "invalidate_complete_window_per_channel")
        self.assertIsNone(record.group_delay_s)
        with self.assertRaises((AttributeError, TypeError)):
            record.operation = "other"

    def test_chained_provenance_and_mean_group_delay(self):
        s = block(tuple((float(n), 2.0) for n in range(5)), rate=20.0)
        first = fir_filter(s, (1.0,))
        second = moving_average(first, 3)
        self.assertEqual([record.operation for record in second.provenance], ["fir", "moving_average"])
        data = json.loads(second.provenance[-1].parameters_json)
        self.assertEqual(data["window"], 3)
        self.assertEqual(data["taps"], [1 / 3] * 3)
        self.assertAlmostEqual(second.provenance[-1].group_delay_s, 0.05)
        self.assertEqual(second.source_id, s.source_id)

    def test_timestamps_use_float_tolerance_not_bit_identity(self):
        s = block(tuple((float(n), 1.0) for n in range(8)), start=0.0, rate=10.0)
        out = moving_average(s, 3)
        self.assertNotEqual(out.timestamp_at(1), s.timestamp_at(3))
        for i in range(out.sample_count):
            self.assertTrue(math.isclose(
                out.timestamp_at(i), s.timestamp_at(i + 2),
                rel_tol=0.0, abs_tol=1e-12,
            ))

    def test_bad_block_type_rejected(self):
        with self.assertRaises(SignalValidationError) as exc:
            fir_filter(None, (1.,))
        self.assertEqual(exc.exception.code, "INVALID_SHAPE")


if __name__ == "__main__":
    unittest.main()
