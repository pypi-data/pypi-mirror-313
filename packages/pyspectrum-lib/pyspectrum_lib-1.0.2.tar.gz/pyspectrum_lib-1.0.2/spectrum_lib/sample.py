import math

from spectrum_lib.spectrum_lib import SpectrumMath


def get_sin_wave_sample(sampling_rate: int, hz: int, step: int):
    return 50 * math.sin(hz * step * (2 - math.pi / sampling_rate))


def main():
    sampling_rate = 250
    process_win_rate = 5
    fft_window = sampling_rate * 4
    bord_frequency = 50

    spectrum_math = SpectrumMath(sampling_rate, fft_window, process_win_rate)
    spectrum_math.init_params(bord_frequency, True)

    delta_coef = 0.0
    theta_coef = 1.0
    alpha_coef = 1.0
    beta_coef = 1.0
    gamma_coef = 0.0

    spectrum_math.set_waves_coeffs(delta_coef, theta_coef, alpha_coef, beta_coef, gamma_coef)
    spectrum_math.set_squared_spect(True)
    spectrum_math.set_hanning_win_spect()


    sample_count = 10
    current_sin_step = 0

    data = [0 for _ in range(sample_count)]

    while True:
        for i in range(sample_count):
            data[i] = get_sin_wave_sample(sampling_rate, 10, current_sin_step) # * 1e6
            current_sin_step += 1

        spectrum_math.push_and_process_data(data)

        raw_spectrum_data = spectrum_math.read_raw_spectrum_info_arr()
        waves_spectrum_data = spectrum_math.read_waves_spectrum_info_arr()

        # spectrum_math.compute_spectrum(data)
        #
        # raw_spectrum_data = spectrum_math.read_raw_spectrum_info()
        # waves_spectrum_data = spectrum_math.read_waves_spectrum_info()

        for i in range(len(raw_spectrum_data)):
            print(
                "{}: {}, {}".format(i, raw_spectrum_data[i].total_raw_pow, len(raw_spectrum_data[i].all_bins_values)))
            print("{}: {} {} {} {} {}".format(i, waves_spectrum_data[i].delta_raw, waves_spectrum_data[i].beta_raw,
                                              waves_spectrum_data[i].alpha_raw, waves_spectrum_data[i].gamma_raw,
                                              waves_spectrum_data[i].theta_raw))

        # if raw_spectrum_data is not None:
        #     print("{}, {}".format(raw_spectrum_data.total_raw_pow, len(raw_spectrum_data.all_bins_values)))

        for i in range(len(waves_spectrum_data)):
            print("{} {} {} {} {}".format(waves_spectrum_data[i].delta_raw, waves_spectrum_data[i].beta_raw,
                                          waves_spectrum_data[i].alpha_raw, waves_spectrum_data[i].gamma_raw,
                                          waves_spectrum_data[i].theta_raw))

        # if waves_spectrum_data is not None:
        #     print("{} {} {} {} {}".format(waves_spectrum_data.delta_raw, waves_spectrum_data.beta_raw,
        #                                   waves_spectrum_data.alpha_raw, waves_spectrum_data.gamma_raw,
        #                                   waves_spectrum_data.theta_raw))

        spectrum_math.set_new_sample_size()

    del spectrum_lib

if __name__ == '__main__':
    main()
