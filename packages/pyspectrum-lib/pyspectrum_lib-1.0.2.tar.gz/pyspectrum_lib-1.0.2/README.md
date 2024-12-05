# Mathematical library for calculating the signal spectrum
The main functionality is the calculation of raw spectrum values and the calculation of EEG spectrum values.
Working with the library is possible in iterative mode (adding new data to the internal buffer, calculating spectrum values) and in one-time spectrum calculation mode for a given array. When working in the iterative mode, the spectrum is calculated with the frequency set during initialization.

## Initialization
### Main parameters
1. Raw signal sampling frequency. Need to be >= 1.
2. Spectrum calculation frequency. Need to be <= 16 kHz.
3. Spectrum calculation window length. Need to be <= signal sampling frequency.
### Optional parameters
1. Upper bound of frequencies for spectrum calculation. Default value is sampling_rate / 2.
2. Normalization of the EEG spectrum by the width of the wavebands. Disabled by default.
3. Weight coefficients for alpha, beta, theta, gamma, delta waves. By default has 1.0 value.
## Creation

```python
sampling_rate = 250 # raw signal sampling frequency
fft_window = sampling_rate * 4 # spectrum calculation window length
process_win_rate = 5 # spectrum calculation frequency
spectrum_math = SpectrumMath(sampling_rate, fft_window, process_win_rate)   
```
## Optional initialization
1. Additional spectrum settings:

```python
bord_frequency = 50 # upper bound of frequencies for spectrum calculation
normalize_spect_by_bandwidth = True # normalization of the EEG spectrum by the width of the wavebands
pectrum_math.init_params(bord_frequency, normalize_spect_by_bandwidth)
```
2. Waves coefficients:

```python
delta_coef = 0.0
theta_coef = 1.0
alpha_coef = 1.0
beta_coef = 1.0
gamma_coef = 0.0
spectrum_math.set_waves_coeffs(delta_coef, theta_coef, alpha_coef, beta_coef, gamma_coef)
```
3. Setting the smoothing of the spectrum calculation by Henning (by default) or Hemming window:

```python
spectrum_math.set_hanning_win_spect() # by Hanning (by default)

spectrum_math.set_hamming_win_spect() # by Hamming
```
## Initializing a data array for transfer to the library
Array of double values with length less or equals then 15 * saignal sampling frequency.
## Types
#### RawSpectrumData
Structure containing the raw spectrum values (with boundary frequency taken into library).

Fields:
- all_bins_nums - Integer value. Number of FFT bars. Contained only in the C++ interface.
- all_bins_values - Double array. Raw FFT bars values.
- total_raw_pow - Double value. Total raw spectrum power.

#### WavesSpectrumData
Structure containing the waves values.

Absolute frequency values (double type):
- delta_raw
- theta_raw
- alpha_raw
- beta_raw
- gamma_raw

Relative (percent) values (double type):
- delta_rel
- theta_rel
- alpha_rel
- beta_rel
- gamma_rel

## FFT band resolution
The library automatically matches the optimal buffer length (degree 2) to calculate the FFT during initialization, depending on the specified window length. Receiving resolution for the FFT bands (number of FFT bands per 1 Hz):

```python
spectrum_math.get_fft_bins_for_1_hz()
```
## Spectrum calculation in iterative mode
1. Adding and process data:

```python
samples = [0 for _ in range(sample_count)]
spectrum_math.push_and_process_data(samples)
```
2. Getting the results:

```python
raw_spectrum_data = spectrum_math.read_raw_spectrum_info_arr()
waves_spectrum_data = spectrum_math.read_waves_spectrum_info_arr()
```
4. Updating the number of new samples. Is necessary for correct calculation of elements in the array of obtained structures, if a large portion of data is added to the library all at once.

```python
spectrum_math.set_new_sample_size()
```
## Spectrum calculation for a single array
1. Compute spectrum:

```python
samples = [0 for _ in range(sample_count)]
spectrum_math.compute_spectrum(samples)
```
2. Getting the results:

```python
raw_spectrum_data = spectrum_math.read_raw_spectrum_info()
waves_spectrum_data = spectrum_math.read_waves_spectrum_info()
```
## Finishing work with the library

```python
del spectrum_lib
```