def bresenham(x0, y0, x1, y1):
    line = []
    (x, y) = (x0, y0)

    if x0 < x1:
        xi = 1
        dx = x1 - x0
    else:
        xi = -1
        dx = x0 - x1

    if y0 < y1:
        yi = 1
        dy = y1 - y0
    else:
        yi = -1
        dy = y0 - y1

    line.append((x, y))
    if dx > dy:
        ai = (dy - dx) * 2
        bi = dy * 2
        d = bi - dx
        while x != x1:
            if d >= 0:
                x += xi
                y += yi
                d += ai
            else:
                d += bi
                x += xi
            line.append((x, y))
    else:
        ai = (dx - dy) * 2
        bi = dx * 2
        d = bi - dy
        while y != y1:
            if d >= 0:
                x += xi
                y += yi
                d += ai
            else:
                d += bi
                y += yi
            line.append((x, y))
    return line
