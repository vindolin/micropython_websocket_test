def hsl2rgb(hsl):
    """convert rgb values in the range 0-255 to an rgb tuple"""
    h, s, l = hsl

    v = (l * (256 + s)) >> 8 if (l < 128) else (((l + s) << 8) - l * s) >> 8

    if v <= 0:
        r = g = b = 0
    else:
        m = l + l - v
        h *= 6
        sextant = h >> 8
        fract = h - (sextant << 8)
        vsf = int(v * fract * (v - m) / v) >> 8
        mid1 = m + vsf
        mid2 = v - vsf

        if sextant == 0:
            return v, mid1, m
        elif sextant == 1:
            return mid2, v, m
        elif sextant == 2:
            return m, v, mid1
        elif sextant == 3:
            return m, mid2, v
        elif sextant == 4:
            return mid1, m, v
        elif sextant == 5:
            return v, m, mid2

    return r, g, b
