from enum import Enum


class SignalFilterType(str, Enum):
    LOWPASS = 'lowpass'
    HIGHPASS = 'highpass'
    BANDPASS = 'bandpass'
    BANDSTOP = 'bandstop'

class SignalWindowName(str, Enum):
    HANNING = 'hanning'
    HAMMING = 'hamming'
    BLACKMAN = 'blackman'
    KAIZER = 'kaizer'

class SignalFilterName(str, Enum):
    CHEBYSHEV_I = 'cheby1'
    CHEBYSHEV_II = 'cheby2'
    BUTTERWORTH = 'butterworth'
