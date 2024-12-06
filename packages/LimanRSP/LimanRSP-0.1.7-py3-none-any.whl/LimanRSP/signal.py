import numpy as np
from scipy.signal import butter, filtfilt
from scipy.integrate import cumulative_trapezoid
from scipy.fftpack import fft, ifft, fftshift, fftfreq
from enum import Enum

from .enums import SignalFilterName, SignalFilterType


def filter_signal(x, lf: float, rf: float, fname: SignalFilterName, ftype: SignalFilterType):
    return x


class Units(Enum):
    ACCELERATION = "Виброускорение, м/c^2"
    VELOCITY = "Виброскорость, мм/с"
    DISPLACEMENT = "Виброперемещение, мкм"

class Window(Enum):
    HANNING = np.hanning
    HAMMING = np.hamming


"""
Функции окна
"""
def apply_window(x, w=None):
    n = len(x)
    f = np.hanning
    if w:
        if w == Window.HAMMING:
            f = np.hamming
    y = f(n) * x
    return y

"""
Функции фильтрации
"""
def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)


"""
Функции перевода единиц измерения
"""
def accel_to_dB(x):
    return 20 * np.log10(x / 1e-6)

def g_to_accel(x):
    g = 9.81  # м/с^2
    return g * x

def integrate(x, t):
    return cumulative_trapezoid(x, t, initial=0)

def accel_to_vibro(x, t):
    return 1000 * integrate(x, t)

def vibro_to_disp(x, t):
    return 1000 * integrate(x, t)

def accel_to_disp(x, t):
    return vibro_to_disp(accel_to_vibro(x, t), t)


"""
Функции обработки сигнала
"""
def signal_to_amp_spectr(x, fs):
    # Вычисление спектра огибающей
    n = len(x)
    frequencies = np.fft.fftfreq(n, d=1/fs)  # Частоты для БПФ
    spectrum = np.fft.fft(x)  # БПФ огибающей
    amp_spectrum = 2 / n * np.abs(spectrum)  # Модуль спектра
    return frequencies[:n//2], amp_spectrum[:n//2]

def signal_to_avg_amp_spectr(x, fs, fl, fr, percent=0.25):
    avg_amp_spectr = None
    avg_points_per_spectr = int(fs)
    print(len(x), avg_points_per_spectr)
    avg_spectr_count = len(x) // avg_points_per_spectr
    avg_spectr_iter = 0
    while avg_spectr_iter < avg_spectr_count:

        temp_signal = x[int((1 - percent) * avg_spectr_iter * avg_points_per_spectr):int(((1 - percent) * avg_spectr_iter + 1) * avg_points_per_spectr)]
        temp_signal = bandpass_filter(temp_signal, fl, fr, fs)
        temp_signal = apply_window(temp_signal)


        freqs, temp_amp_spectr = signal_to_amp_spectr(temp_signal, fs)
        if avg_amp_spectr is None:
            avg_amp_spectr = temp_amp_spectr
        else:
            avg_amp_spectr += temp_amp_spectr

        avg_spectr_iter += 1

    if avg_spectr_count != 0:
      avg_amp_spectr /= avg_spectr_count

    return freqs, avg_amp_spectr

if __name__ == '__main__':
    x = [0, 1, 2, 3]
    y = [0.5, 0.4, 0.1]
    integrate(y, x)