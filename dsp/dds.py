from math import sqrt, pi

#!/usr/bin/env python3
from .config        import *
from .cordic        import cordic
from .dithering     import Dither
from .smooth        import Lowpass_fir_filter, N_pass_filter

class DDS(object):
    def __init__(self, magnitude = ZERO, frequency = 1, fi = ZERO):
        self._fi                = fi
        self._magnitude         = magnitude
        self._frequency         = frequency

        #internal services
        self.__magnitude_filter = N_pass_filter(4, Lowpass_fir_filter).apply
        self.__frequency_filter = N_pass_filter(4, Lowpass_fir_filter).apply
        self.__dither           = Dither().apply

        # initialize internal filter memory
        while self.__magnitude_filter(self._magnitude) != self._magnitude:
            pass
        while self.__frequency_filter(self._frequency) != self._frequency:
            pass

    def get_next_sample(self, dt):
        self._fi       += FIX_POINT_MUL(PI_8, 16 * dt * self.__frequency_filter(self._frequency))
        self._fi       %= PI_8 << 4

        _, _cos, _sin   = cordic(self._fi)
        scaled_sin      = FIX_POINT_MUL(_sin, self.__magnitude_filter(self._magnitude))
        out             = self.__dither(scaled_sin)
        return out
