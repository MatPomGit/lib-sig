"""Reference tests for FFT bins, PSD units, windowing, and Parseval's law."""

import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from lib_sig import (
    ChannelDescriptor, SignalBlock, SignalValidationError, TimeAxis,
    SpectralEstimate, periodogram_psd, rfft_spectrum,
)


def signal(x, y=None, *, fs=16., start=0., irregular=False, mask=None):
    if y is None:
        y = [0.] * len(x)
    t = (
        TimeAxis("irregular", "sensor", timestamps_s=tuple(start + k / fs for k in range(len(x))))
        if irregular else TimeAxis("regular", "sensor", start_s=start, sampling_rate_hz=fs)
    )
    return SignalBlock(
        samples=tuple((float(a), float(b)) for a, b in zip(x, y)),
        channels=(ChannelDescriptor("A", "V"), ChannelDescriptor("B", "mV")),
        time_axis=t, source_id="synthetic/spectral", mask=mask,
    )


class SpectralTests(unittest.TestCase):
    def test_real_fft_has_exact_bin_and_unscaled_amplitude(self):
        n, k = 16, 3
        x = [2. * math.cos(2. * math.pi * k * i / n) for i in range(n)]
        result = rfft_spectrum(signal(x))
        self.assertIsInstance(result, SpectralEstimate)
        self.assertEqual(result.kind, "rfft")
        self.assertEqual(len(result.frequencies_hz), 9)
        self.assertEqual(len(result.values[0]), 2)
        self.assertAlmostEqual(result.frequencies_hz[k], 3.)
        self.assertAlmostEqual(result.values[k][0].real, 16., places=10)
        self.assertAlmostEqual(result.values[k][0].imag, 0., places=10)
        for i, row in enumerate(result.values):
            if i != k:
                self.assertAlmostEqual(abs(row[0]), 0., places=10)

    def test_psd_integrates_to_sinusoidal_variance(self):
        n, k = 16, 3
        x = [2. * math.cos(2 * math.pi * k * i / n) for i in range(n)]
        result = periodogram_psd(signal(x))
        self.assertEqual(result.kind, "psd")
        self.assertEqual(result.units, ("V²/Hz", "mV²/Hz"))
        self.assertAlmostEqual(result.values[k][0], 2.0, places=10)
        df = result.frequencies_hz[1] - result.frequencies_hz[0]
        self.assertAlmostEqual(sum(row[0] for row in result.values) * df, 2.0, places=10)

    def test_dc_and_nyquist_are_not_doubled(self):
        n = 16
        x = [3. + 2. * (-1)**i for i in range(n)]
        result = periodogram_psd(signal(x), detrend="none")
        self.assertAlmostEqual(result.values[0][0], 9., places=10)
        self.assertAlmostEqual(result.values[8][0], 4., places=10)
        self.assertAlmostEqual(sum(row[0] for row in result.values), 13., places=10)

    def test_default_constant_detrending_removes_dc(self):
        result = periodogram_psd(signal([7.] * 16))
        self.assertTrue(all(abs(row[0]) < 1e-10 for row in result.values))
        undetrended = periodogram_psd(signal([7.] * 16), detrend="none")
        self.assertAlmostEqual(undetrended.values[0][0], 49., places=10)

    def test_hann_is_periodic_and_preserves_normalised_energy(self):
        n = 32
        x = [math.sin(2. * math.pi * 5 * i / n) for i in range(n)]
        result = periodogram_psd(signal(x, fs=32.), window="hann", detrend="none")
        self.assertAlmostEqual(sum(row[0] for row in result.values), 0.5, places=10)
        fft = rfft_spectrum(signal([1.] * 8), window="hann")
        self.assertAlmostEqual(fft.values[0][0].real, 4., places=10)

    def test_odd_n_doubles_highest_bin(self):
        n, k = 15, 3
        x = [math.sin(2 * math.pi * k * i / n) for i in range(n)]
        result = periodogram_psd(signal(x, fs=15.))
        self.assertEqual(len(result.frequencies_hz), 8)
        self.assertAlmostEqual(sum(row[0] for row in result.values), 0.5, places=10)

    def test_multichannel_units_and_provenance(self):
        x = [math.cos(math.pi * i / 2) for i in range(16)]
        y = [3 * math.sin(math.pi * i / 2) for i in range(16)]
        result = periodogram_psd(signal(x, y, fs=8., start=6.))
        self.assertEqual(result.source_id, "synthetic/spectral")
        self.assertEqual(result.timebase, "sensor")
        self.assertEqual(result.start_s, 6.)
        self.assertEqual(result.sampling_rate_hz, 8.)
        self.assertEqual(result.sample_count, 16)
        self.assertEqual(result.units, ("V²/Hz", "mV²/Hz"))
        self.assertAlmostEqual(result.values[4][0], 1., places=10)
        self.assertAlmostEqual(result.values[4][1], 9., places=10)

    def test_masked_missing_sample_is_not_interpolated(self):
        mask = ((True, True), (False, True)) + ((True, True),) * 6
        s = signal([1., math.nan] + [1.] * 6, mask=mask)
        for function in (rfft_spectrum, periodogram_psd):
            with self.subTest(function=function.__name__), self.assertRaises(SignalValidationError) as context:
                function(s)
            self.assertEqual(context.exception.code, "DATA_LOSS")

    def test_irregular_sample_axis_rejected(self):
        s = signal([1.] * 8, irregular=True)
        for function in (rfft_spectrum, periodogram_psd):
            with self.subTest(function=function.__name__), self.assertRaises(SignalValidationError) as context:
                function(s)
            self.assertEqual(context.exception.code, "IRREGULAR_SAMPLING")

    def test_short_signal_or_unknown_processing_parameters_rejected(self):
        s = signal([1.] * 8)
        inputs = [dict(window="rectangular"), dict(detrend="linear"),
                  dict(window=None), dict(detrend=None)]
        for kw in inputs:
            with self.subTest(kw=kw), self.assertRaises(SignalValidationError) as context:
                periodogram_psd(s, **kw)
            self.assertEqual(context.exception.code, "INVALID_SPECTRUM")
        with self.assertRaises(SignalValidationError):
            periodogram_psd(signal([1.]))
        with self.assertRaises(SignalValidationError):
            periodogram_psd(None)

    def test_parseval_for_nontrivial_nonharmonic_sequence(self):
        values = [float(z) for z in (1, -2, 0, 4, 3, -1, 2, 5)]
        s = signal(values, fs=8.)
        estimate = periodogram_psd(s, window="boxcar", detrend="none")
        df = estimate.frequencies_hz[1] - estimate.frequencies_hz[0]
        integrated = sum(v[0] for v in estimate.values) * df
        mean_square = sum(x * x for x in values) / len(values)
        self.assertAlmostEqual(integrated, mean_square, places=10)

    def test_input_is_not_mutated(self):
        s = signal([1., 2., -3., 0., 2., 4., -1., 0.])
        old = s.samples
        periodogram_psd(s, window="hann")
        self.assertEqual(s.samples, old)

    def test_unrepresentable_fft_raises_data_loss(self):
        s = signal([1e308] * 8)
        with self.assertRaises(SignalValidationError) as ctx:
            rfft_spectrum(s, detrend="none")
        self.assertEqual(ctx.exception.code, "DATA_LOSS")


if __name__ == "__main__":
    unittest.main()
