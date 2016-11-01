from math import sqrt, pi

#!/usr/bin/env python3
from .config        import *
from .cordic        import cordic
from .dithering     import Dither
from .smooth        import Lowpass_fir_filter, N_pass_filter

class DDS(object):
    def __init__(self, magnitude = ZERO, frequency = 1, fi = ZERO):
        self.fi                 = fi
        self._magnitude         = magnitude
        self._active__magnitude = ZERO
        self._frequency         = frequency
        self._active__frequency = ZERO

        #internal services
        self.__magnitude_filter = N_pass_filter(4, Lowpass_fir_filter).apply
        self.__frequency_filter = N_pass_filter(4, Lowpass_fir_filter).apply
        self.__dither           = Dither().apply

        # initialize internal filter memory
        while self._magnitude != self._smooth_magnitude:
            pass
        while self._frequency != self._smooth_frequency:
            pass

    @property
    def _smooth_magnitude(self):
        if self._active__magnitude != self._magnitude:
            self._active__magnitude = self.__magnitude_filter(self._magnitude)
        return self._active__magnitude


    @property
    def _smooth_frequency(self):
        if self._active__frequency != self._frequency:
            self._active__frequency = self.__frequency_filter(self._frequency)
        return self._active__frequency

    def get_next_sample(self, dt):
        self.fi        += FIX_POINT_MUL(PI_8, 16 * dt * self._smooth_frequency)
        self.fi        %= PI_8 << 4

        _, _cos, _sin   = cordic(self.fi)
        mag = self._smooth_magnitude
        scaled_sin      = FIX_POINT_MUL(_sin,  mag)
        out             = self.__dither(scaled_sin)
        return out
