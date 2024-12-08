import bitmath

def size_readable(bytes, precision=3):
    return bitmath.Byte(bytes=bytes).best_prefix().format('{value:.%sf} {unit}' % precision)
