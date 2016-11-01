#!/usr/bin/env python3
from .config import *

#NOTE: IIR filter can save memory and give some speed up, but IIR filter adds more non-liniar distortion
class Lowpass_fir_filter(object):
    def __init__(self, window_size_power = 3):
        self.__power    = window_size_power
        self.__history  = [ZERO] * (1 << self.__power)
        self.__acc      = ZERO

    def apply(self, value):
        self.__history.append(value)
        self.__acc -= self.__history.pop(0)
        self.__acc += value
        return self.__acc >> self.__power

class N_pass_filter(object):
    def __init__(self, n, Filter, **filter_arg):
        self.__v = ZERO
        self.__n = n
        self.__f = []
        for _ in range(self.__n):
            self.__f.append(Filter(**filter_arg).apply)

    def apply(self, value):
        if value != self.__v:
            self.__v = value
            for i in range(self.__n):
                self.__v = self.__f[i](self.__v)
        return self.__v