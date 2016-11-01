#!/usr/bin/env python3
from math import sin, cos, pi

from tools.html_chart_helper import *
from dsp.config     import ONE, ZERO, FIX_FP_MAIN_SIZE
from dsp.cordic     import cordic
from dsp.dithering  import Dither
from dsp.smooth     import Lowpass_fir_filter, N_pass_filter

def find_error_bit_position(delta):
    i = 0
    delta = abs(delta)
    while delta < 1:
        delta *= 2
        i += 1
    return i

def check_aproximation_quality():
    report = []
    x = 1.0
    i = 0
    while i < 24:
        a = 1.0 / 2**i
        report.append((i, find_error_bit_position(sin(a) - a)))
        i += 1
    put_html_to_file('analytics/sin_aprox_bit_error',
        make_html_chart(report, 'iter', 'bit'))

def check_sin_quality():
    test_data = []
    fi = 0.0
    while fi < 2*pi:
        fi += 0.001
        fix_fi = int(fi % (2*pi) * ONE)
        _cnt, _cos, _sin = cordic(fix_fi)
        test_data.append((fi, _cnt, _cos / ONE, _sin / ONE))

    report1 = []
    report2 = []
    for fi, _cnt, _cos, _sin in test_data:
        delta = sin(fi) - _sin
        report1.append((fi, delta))
        report2.append((fi, _cnt, find_error_bit_position(delta)))

    put_html_to_file('analytics/sin_delta', 
        make_html_chart(report1, 'rad', 'delta'))
    put_html_to_file('analytics/sin_error_position', 
        make_html_chart2(report2, 'rad', 'number_of_iteration', 'bit_error_position'))

def check_dithering():
    dithering = Dither().apply

    test_data = []
    x = 0
    LSB = ONE >> FIX_FP_MAIN_SIZE
    while x < 20 * LSB:
        x += 1
        f = x/10
        test_data.append((x, f / LSB, dithering(int(f))))

    report1 = []
    report2 = []
    for x, f_real, f_out in test_data:
        report1.append((x, f_real, f_out))
        report2.append((x, f_real - f_out))
    put_html_to_file('analytics/dithering', 
        make_html_chart2(report1, 'rad', 'f_value','f_and_noise'))
    put_html_to_file('analytics/dithering_noise', 
        make_html_chart(report2, 'rad', 'noise'))

def check_smooth():
    smooth = N_pass_filter(4, Lowpass_fir_filter).apply

    test_data = []
    x = 0
    while x < 80:
        x += 1
        f = ONE if x < 40 else ZERO
        test_data.append((x, f, smooth(f)))

    put_html_to_file('analytics/smooth', 
        make_html_chart2(test_data, 'rad', 'f_value','f_smooth'))

if __name__ == "__main__":
    check_aproximation_quality()
    check_sin_quality()
    check_dithering()
    check_smooth()
    