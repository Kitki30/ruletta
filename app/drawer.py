import math

def fill_circle(tft, x0, y0, r, color):
    r2 = r * r
    for y in range(-r, r+1):
        x_span = int((r2 - y*y) ** 0.5)
        tft.hline(x0 - x_span, y0 + y, 2 * x_span + 1, color)

def draw_roulette(tft, x0, y0, r):
    sectors = 6
    colors = [0x0000, 0xF800] * 3
    angle_step = 2 * math.pi / sectors

    for y in range(-r, r+1):
        x_span = int((r*r - y*y) ** 0.5)
        start_x = None
        prev_sector = None

        for x in range(-x_span, x_span+1):
            angle = math.atan2(y, x)
            if angle < 0:
                angle += 2 * math.pi
            sector = int(angle // angle_step)

            if prev_sector is None:
                start_x = x
                prev_sector = sector
            elif sector != prev_sector:
                tft.hline(x0 + start_x, y0 + y, x - start_x, colors[prev_sector])
                start_x = x
                prev_sector = sector

        if start_x is not None:
            tft.hline(x0 + start_x, y0 + y, x_span - start_x + 1, colors[prev_sector])

def draw_lamps(tft, x0, y0, r, lamp_radius=5):
    """Draw lamps"""
    sectors = 6
    angle_step = 2 * math.pi / sectors
    lamps = []

    for i in range(sectors):
        angle = i * angle_step + angle_step / 2  # Center
        lx = int(x0 + (r + 10) * math.cos(angle))
        ly = int(y0 + (r + 10) * math.sin(angle))
        lamps.append((lx, ly))
        fill_circle(tft, lx, ly, lamp_radius, 0x7BEF)

    return lamps

def light_lamp(tft, lamps, idx, color=0xFFE0):
    """Light up one light"""
    if 0 <= idx < len(lamps):
        lx, ly = lamps[idx]
        fill_circle(tft, lx, ly, 5, color)