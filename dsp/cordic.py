#!/usr/bin/env python3
from .config import *

def cordic(fi):
    if fi < 0 or fi > 8 * ONE:
        raise ValueError("fi value shall be inside [0, %d] interval, but %d given" % (8 * ONE, fi))

    n = 0
    while fi > PI_8:
        n += 1
        fi -= PI_8

    q, n = int(n / 4) % 4, n % 4
    x, y = 0, 0
    _cordic_pi_8 = _cordic_pi_8_asf
    #_cordic_pi_8 = _cordic_pi_8_k2sf # can speed up calculation up to two times

    if n == 0:
        c, x, y = _cordic_pi_8(x0=ONE,          y0=ZERO,        z0=   0 + fi,   clockwise=False)
    elif n == 1:
        c, x, y = _cordic_pi_8(x0=SQRT2 >> 1,   y0=SQRT2 >> 1,  z0=PI_8 - fi,   clockwise=True)
    elif n == 2:
        c, x, y = _cordic_pi_8(x0=SQRT2 >> 1,   y0=SQRT2 >> 1,  z0=   0 + fi,   clockwise=False)
    elif n == 3:
        c, x, y = _cordic_pi_8(x0=ZERO,         y0=ONE,         z0=PI_8 - fi,   clockwise=True)

    if q == 0:
        _cos, _sin = +x, +y
    elif q == 1:
        _cos, _sin = -y, +x
    elif q == 2:
        _cos, _sin = -x, -y
    elif q == 3:
        _cos, _sin = +y, -x

    return c, _cos, _sin

# the specific constants bound to the CORDIC modification, calculated at compile time
I0          = 1 + int(FIX_FP_MAIN_SIZE / 3) # upper bound to achive FIX_FP_MAIN_SIZE precision
SIGMA       = 1 << FIX_FP_REST_SIZE         # lower bound to remove excess iteration
def _cordic_pi_8_asf(x0, y0, z0, clockwise):
    x, y, z = x0, y0, z0
    i       = I0
    cnt     = 0 
    while z > SIGMA:
        j = 1 + (i << 1)
        step = ONE >> i
        while z > step:
            cnt += 1
            z -= step
            if clockwise:
                x, y = x - (x >> j) + (y >> i), y - (y >> j) - (x >> i)
            else:
                x, y = x - (x >> j) - (y >> i), y - (y >> j) + (x >> i)
        i += 1
    return cnt, x, y
