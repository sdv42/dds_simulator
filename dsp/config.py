from math import sqrt, pi

# NOTE: fix point number representation Q1.21 : INTEGER_PART . FRACTION_PART_MAIN | FRACTION_PART_REST
FIX_FP_REST_SIZE    = 5
FIX_FP_REST_MASK    = (1 << FIX_FP_REST_SIZE) - 1
FIX_FP_MAIN_SIZE    = 16
FIX_FP_SIZE         = FIX_FP_MAIN_SIZE + FIX_FP_REST_SIZE
FIX_IP_SIZE         = 1

# compile time constants:
ONE         = int(1) << FIX_FP_SIZE
ZERO        = int(0)

SQRT2       = int(sqrt(2) * ONE)
PI_8        = int(pi/8 * ONE)

# platform related parameters
SAMPLE_RATE = int(1     << 18)
SAMPLE_dT   = int(ONE   >> 18)

def FIX_POINT_MUL(a, b):
    return (a * b) >> FIX_FP_SIZE # NOTE: The fix point multiplication shall be adapted to the choosen platform

def FIX_POINT_DIV(a, b):
    return int(a / b)