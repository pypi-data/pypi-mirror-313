import ctypes
import pathlib
import platform
import sys
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class RawSpectrumData:
    all_bins_values: list
    total_raw_pow: float


@dataclass
class WavesSpectrumData:
    delta_raw: float
    theta_raw: float
    alpha_raw: float
    beta_raw: float
    gamma_raw: float
    delta_rel: float
    theta_rel: float
    alpha_rel: float
    beta_rel: float
    gamma_rel: float


_libname = None
if sys.platform == "win32":
    arc = platform.architecture()
    if arc[0].__contains__("64"):
        _libname = pathlib.Path(__file__).parent.resolve() / "libs" / "win" / "spectrumlib-x64.dll"
    else:
        _libname = pathlib.Path(__file__).parent.resolve() / "libs" / "win" / "spectrumlib-x32.dll"
elif sys.platform.startswith("linux"):
    print('Not implemented')
elif sys.platform == "darwin":
    _libname = pathlib.Path(__file__).parent.resolve() / "libs" / "macos" / "libspectrumlib.dylib"
else:
    raise FileNotFoundError("This platform (%s) is currently not supported by pyspectrum-lib." % sys.platform)

_spectrum_lib = ctypes.CDLL(str(_libname))


class SpectrumMath:
    class _NativeRawSpectrumData(ctypes.Structure):
        _fields_ = [('all_bins_nums', ctypes.c_int), ('all_bins_values', ctypes.POINTER(ctypes.c_double)),
                    ('total_raw_pow', ctypes.c_double)]

    class _NativeWavesSpectrumData(ctypes.Structure):
        _fields_ = [('delta_raw', ctypes.c_double), ('theta_raw', ctypes.c_double), ('alpha_raw', ctypes.c_double),
                    ('beta_raw', ctypes.c_double), ('gamma_raw', ctypes.c_double), ('delta_rel', ctypes.c_double),
                    ('theta_rel', ctypes.c_double), ('alpha_rel', ctypes.c_double), ('beta_rel', ctypes.c_double),
                    ('gamma_rel', ctypes.c_double)]

    def __init__(self, sample_rate: int, fft_window: int, process_win_freq: int):
        spectrum_math = ctypes.POINTER(ctypes.c_void_p)

        self._create_spectrum_math = _spectrum_lib.createSpectrumMath
        self._create_spectrum_math.restype = ctypes.POINTER(spectrum_math)
        self._create_spectrum_math.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_int)

        self._free_spectrum_math = _spectrum_lib.freeSpectrumMath
        self._free_spectrum_math.restype = None
        self._free_spectrum_math.argtypes = (ctypes.POINTER(spectrum_math),)

        self._init_params = _spectrum_lib.SpectrumMathInitParams
        self._init_params.restype = None
        self._init_params.argtypes = (ctypes.POINTER(spectrum_math), ctypes.c_int, ctypes.c_bool)

        self._set_waves_coeffs = _spectrum_lib.SpectrumMathSetWavesCoeffs
        self._set_waves_coeffs.restype = None
        self._set_waves_coeffs.argtypes = (
            ctypes.POINTER(spectrum_math), ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,
            ctypes.c_double)

        self._set_hanning_win_spect = _spectrum_lib.SpectrumMathSetHanningWinSpect
        self._set_hanning_win_spect.restype = None
        self._set_hanning_win_spect.argtypes = (ctypes.POINTER(spectrum_math),)

        self._set_hamming_win_spect = _spectrum_lib.SpectrumMathSetHammingWinSpect
        self._set_hamming_win_spect.restype = None
        self._set_hamming_win_spect.argtypes = (ctypes.POINTER(spectrum_math),)

        # SpectrumMathSetSquaredSpect(SpectrumMath * spectrumMathPtr, bool
        # fl);
        self._set_squared_spect = _spectrum_lib.SpectrumMathSetSquaredSpect
        self._set_squared_spect.restype = None
        self._set_squared_spect.argtypes = (ctypes.POINTER(spectrum_math), ctypes.c_bool)

        self._push_data = _spectrum_lib.SpectrumMathPushData
        self._push_data.restype = None
        self._push_data.argtypes = (ctypes.POINTER(spectrum_math), ctypes.c_void_p, ctypes.c_size_t)

        self._process_data = _spectrum_lib.SpectrumMathProcessData
        self._process_data.restype = None
        self._process_data.argtypes = (ctypes.POINTER(spectrum_math),)

        self._compute_spectrum = _spectrum_lib.SpectrumMathComputeSpectrum
        self._compute_spectrum.restype = None
        self._compute_spectrum.argtypes = (ctypes.POINTER(spectrum_math), ctypes.c_void_p, ctypes.c_int)

        self._get_fft_bins_for_1_hz = _spectrum_lib.SpectrumMathGetFFTBinsFor1Hz
        self._get_fft_bins_for_1_hz.restype = ctypes.c_double
        self._get_fft_bins_for_1_hz.argtypes = (ctypes.POINTER(spectrum_math),)

        self._read_raw_spectrum_info = _spectrum_lib.SpectrumMathReadRawSpectrumInfo
        self._read_raw_spectrum_info.restype = None
        self._read_raw_spectrum_info.argtypes = (ctypes.POINTER(spectrum_math), self._NativeRawSpectrumData)

        self._read_waves_spectrum_info = _spectrum_lib.SpectrumMathReadWavesSpectrumInfo
        self._read_waves_spectrum_info.restype = None
        self._read_waves_spectrum_info.argtypes = (ctypes.POINTER(spectrum_math), self._NativeWavesSpectrumData)

        self._read_spectrum_arr_size = _spectrum_lib.SpectrumMathReadSpectrumArrSize
        self._read_spectrum_arr_size.restype = ctypes.c_uint32
        self._read_spectrum_arr_size.argtypes = (ctypes.POINTER(spectrum_math),)

        self._read_raw_spectrum_info_arr = _spectrum_lib.SpectrumMathReadRawSpectrumInfoArr
        self._read_raw_spectrum_info_arr.restype = None
        self._read_raw_spectrum_info_arr.argtypes = (ctypes.POINTER(spectrum_math), ctypes.c_void_p, ctypes.c_void_p)

        self._read_waves_spectrum_info_arr = _spectrum_lib.SpectrumMathReadWavesSpectrumInfoArr
        self._read_waves_spectrum_info_arr.restype = None
        self._read_waves_spectrum_info_arr.argtypes = (ctypes.POINTER(spectrum_math), ctypes.c_void_p, ctypes.c_void_p)

        self._set_new_sample_size = _spectrum_lib.SpectrumMathSetNewSampleSize
        self._set_new_sample_size.restype = None
        self._set_new_sample_size.argtypes = (ctypes.POINTER(spectrum_math),)

        self._clear_data = _spectrum_lib.SpectrumMathClearData
        self._clear_data.restype = None
        self._clear_data.argtypes = (ctypes.POINTER(spectrum_math),)

        self._native_ptr = self._create_spectrum_math(sample_rate, fft_window, process_win_freq)

    def init_params(self, up_border_frequency: int, normalize_spect_by_bandwidth: bool):
        self._init_params(self._native_ptr, up_border_frequency, normalize_spect_by_bandwidth)

    def set_waves_coeffs(self, d_coef: float, t_coef: float, a_coef: float, b_coef: float, g_coef: float):
        self._set_waves_coeffs(self._native_ptr, d_coef, t_coef, a_coef, b_coef, g_coef)

    def set_hanning_win_spect(self):
        self._set_hanning_win_spect(self._native_ptr)

    def set_hamming_win_spect(self):
        self._set_hamming_win_spect(self._native_ptr)

    def set_squared_spect(self, fl: bool):
        self._set_squared_spect(self._native_ptr, fl)

    def push_and_process_data(self, samples: List[float]):
        self._push_data(self._native_ptr, (ctypes.c_double * len(samples))(*samples), len(samples))
        self._process_data(self._native_ptr)

    def compute_spectrum(self, samples: List[float]):
        self._compute_spectrum(self._native_ptr, (ctypes.c_double * len(samples))(*samples), ctypes.c_int(len(samples)))

    def get_fft_bins_for_1_hz(self) -> float:
        return self._get_fft_bins_for_1_hz(self._native_ptr)

    def read_raw_spectrum_info(self) -> Optional[RawSpectrumData]:
        data = self._NativeRawSpectrumData()
        self._read_raw_spectrum_info(self._native_ptr, data)

        if data.all_bins_values is None:
            return None

        return RawSpectrumData([data.all_bins_values[x] for x in range(data.all_bins_nums)], data.total_raw_pow)

    def read_waves_spectrum_info(self) -> WavesSpectrumData:
        data = self._NativeWavesSpectrumData()
        self._read_waves_spectrum_info(self._native_ptr, data)

        return WavesSpectrumData(data.delta_raw,
                                 data.theta_raw,
                                 data.alpha_raw,
                                 data.beta_raw,
                                 data.gamma_raw,
                                 data.delta_rel,
                                 data.theta_rel,
                                 data.alpha_rel,
                                 data.beta_rel,
                                 data.gamma_rel)

    def read_spectrum_arr_size(self) -> int:
        return self._read_spectrum_arr_size(self._native_ptr)

    def read_raw_spectrum_info_arr(self) -> List[RawSpectrumData]:
        spectrum_size = self.read_spectrum_arr_size()

        if spectrum_size == 0:
            return []

        native_result = [self._NativeRawSpectrumData() for _ in range(spectrum_size)]
        native_result = (self._NativeRawSpectrumData * len(native_result))(*native_result)

        self._read_raw_spectrum_info_arr(self._native_ptr, native_result, ctypes.byref(ctypes.c_uint32(spectrum_size)))

        return [RawSpectrumData([native_result[i].all_bins_values[x] for x in range(native_result[i].all_bins_nums)],
                                native_result[i].total_raw_pow) for i in range(spectrum_size)]

    def read_waves_spectrum_info_arr(self) -> List[WavesSpectrumData]:
        spectrum_size = self.read_spectrum_arr_size()

        if spectrum_size == 0:
            return []

        native_result = [self._NativeWavesSpectrumData() for _ in range(spectrum_size)]
        native_result = (self._NativeWavesSpectrumData * len(native_result))(*native_result)

        self._read_waves_spectrum_info_arr(self._native_ptr, native_result, ctypes.byref(ctypes.c_uint32(spectrum_size)))

        return [WavesSpectrumData(x.delta_raw,
                                  x.theta_raw,
                                  x.alpha_raw,
                                  x.beta_raw,
                                  x.gamma_raw,
                                  x.delta_rel,
                                  x.theta_rel,
                                  x.alpha_rel,
                                  x.beta_rel,
                                  x.gamma_rel) for x in native_result]

    def set_new_sample_size(self):
        self._set_new_sample_size(self._native_ptr)

    def clear_data(self):
        self._clear_data(self._native_ptr)

    def __del__(self):
        if self._native_ptr is not None:
            self._free_spectrum_math(self._native_ptr)
            self._native_ptr = None
