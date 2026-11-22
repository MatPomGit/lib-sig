"""Independent scipy.signal reference for NumPy-backed Signal spectral API."""

import math
from pathlib import Path
import sys
import unittest

import numpy as np
from scipy import fft as scipy_fft
from scipy import signal as scipy_signal

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from lib_sig import ChannelDescriptor, SignalBlock, TimeAxis, periodogram_psd, rfft_spectrum


class SpectralReferenceTests(unittest.TestCase):
    def test_scipy_reference_psd_even_odd_hann_boxcar_detrend(self):
        for n in (15, 16):
            fs = 20.0
            values = np.asarray([
                0.7 + math.sin(2 * math.pi * 3 * i / n)
                + 0.35 * math.cos(2 * math.pi * 5 * i / n)
                + 0.08 * i / n
                for i in range(n)
            ], dtype=np.float64)
            block = SignalBlock(
                samples=tuple((float(x), float(2 * x)) for x in values),
                channels=(ChannelDescriptor("x", "V"), ChannelDescriptor("y", "mV")),
                time_axis=TimeAxis("regular", "reference", start_s=0.0, sampling_rate_hz=fs),
                source_id="synthetic/scipy-reference",
            )
            for window in ("boxcar", "hann"):
                for detrend in ("none", "constant"):
                    with self.subTest(n=n, window=window, detrend=detrend):
                        kwargs = {"window": window, "detrend": detrend}
                        actual = periodogram_psd(block, **kwargs)
                        ref_f, ref_psd = scipy_signal.periodogram(
                            values, fs=fs, window=window,
                            detrend=False if detrend == "none" else "constant",
                            scaling="density", return_onesided=True,
                        )
                        np.testing.assert_allclose(actual.frequencies_hz, ref_f, rtol=0, atol=1e-12)
                        np.testing.assert_allclose([row[0] for row in actual.values], ref_psd, rtol=1e-12, atol=1e-12)
                        np.testing.assert_allclose([row[1] for row in actual.values], 4 * ref_psd, rtol=1e-12, atol=1e-12)
                        actual_fft = rfft_spectrum(block, **kwargs)
                        centered = values - values.mean() if detrend == "constant" else values
                        window_values = scipy_signal.get_window(window, n, fftbins=True)
                        ref_fft = scipy_fft.rfft(centered * window_values)
                        np.testing.assert_allclose([row[0] for row in actual_fft.values], ref_fft, rtol=1e-12, atol=1e-12)


if __name__ == "__main__":
    unittest.main()
