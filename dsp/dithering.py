#!/usr/bin/env python3
from .config import *

class Dither(object):
    def __init__(self):
        self.__twister = ZERO # can be initialized by random to achive a better noise quality

    def _spin_twister(self, probability):
        self.__twister += probability
        self.__twister &= FIX_FP_REST_MASK
        return 1 if self.__twister < probability else 0

    def apply(self, value):
        noise = self._spin_twister(value & FIX_FP_REST_MASK)
        #print(value>>FIX_FP_REST_SIZE, value & FIX_FP_REST_MASK, noise)
        return (value >> FIX_FP_REST_SIZE) + noise