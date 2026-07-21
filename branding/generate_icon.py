#!/usr/bin/env python3
"""Generate Ravive's app icon from the same OKLCH tokens the UI uses.

The mark is "resolve": four vertical bands whose cells subdivide left to right,
from four coarse blocks to a solid field. It states what the app does — low
resolution becoming high — without a lens, a sparkle or a wand, the two reflexes
every upscaler icon falls into.

Outputs (written next to the repo root):
    logo_master_1024.png   1024 canvas, 824 body, transparent margin
    logo.icns              the macOS bundle icon (via iconutil)
    logo.jpg               the in-app header asset, composited on --surface-2

Run:  python3 branding/generate_icon.py
"""

import math
import os
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- tokens, copied verbatim from gui.py's :root -----------------------------
BG = (0.215, 0.007, 250)          # between --surface-1 and --surface-2
ACCENT = (0.780, 0.150, 72)       # --accent
SURFACE_2 = (0.235, 0.008, 250)   # --surface-2, the JPEG matte

# --- geometry ----------------------------------------------------------------
CANVAS = 1024
BODY = 824                # Apple's content area inside a 1024 macOS icon
SQUIRCLE_N = 5.8          # superellipse exponent ~ Apple's continuous corner
MARK_W = 608              # the mark is 2:1 — it should read as footage, not a chart
SS = 4                    # supersample factor

# (rows across the mark's height, gap as a fraction of cell size) per band.
# Same coverage story left to right: coarse and airy resolving into dense.
BANDS = [(3, 0.150), (6, 0.100), (12, 0.050)]
CELL_RADIUS = 0.14        # fraction of cell size
CELL_RADIUS_MAX = 9       # px at 1024 — keeps the finest band from perforating


def oklch_to_rgb(L, C, h_deg):
    """OKLCH -> 8-bit sRGB. Same math the browser applies to the CSS tokens."""
    h = math.radians(h_deg)
    a, b = C * math.cos(h), C * math.sin(h)

    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3

    lin = (
        +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )

    def encode(v):
        v = max(0.0, min(1.0, v))
        v = 12.92 * v if v <= 0.0031308 else 1.055 * (v ** (1 / 2.4)) - 0.055
        return int(round(v * 255))

    return tuple(encode(v) for v in lin)


def superellipse(cx, cy, half, n, steps=2048):
    """Points of |x/half|^n + |y/half|^n = 1 — a squircle, not a rounded rect."""
    pts = []
    for i in range(steps):
        t = 2 * math.pi * i / steps
        ct, st = math.cos(t), math.sin(t)
        x = half * math.copysign(abs(ct) ** (2 / n), ct)
        y = half * math.copysign(abs(st) ** (2 / n), st)
        pts.append((cx + x, cy + y))
    return pts


def build():
    size = CANVAS * SS
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # body
    d.polygon(
        superellipse(size / 2, size / 2, BODY * SS / 2, SQUIRCLE_N),
        fill=oklch_to_rgb(*BG) + (255,),
    )

    # mark — one colour throughout; the progression is carried by cell size
    colour = oklch_to_rgb(*ACCENT) + (255,)
    w = MARK_W * SS
    h = w / 2
    x0 = (size - w) / 2
    y0 = (size - h) / 2
    band_w = w / len(BANDS)

    for idx, (rows, gap_ratio) in enumerate(BANDS):
        cell = h / rows
        cols = max(1, int(round(band_w / cell)))
        cell = band_w / cols          # square the cells to the band exactly
        gap = cell * gap_ratio
        radius = min((cell - gap) * CELL_RADIUS, CELL_RADIUS_MAX * SS)

        for r in range(int(round(h / cell))):
            for c in range(cols):
                cx0 = x0 + idx * band_w + c * cell + gap / 2
                cy0 = y0 + r * cell + gap / 2
                d.rounded_rectangle(
                    [cx0, cy0, cx0 + cell - gap, cy0 + cell - gap],
                    radius=radius,
                    fill=colour,
                )

    return img.resize((CANVAS, CANVAS), Image.LANCZOS)


def main():
    icon = build()

    master = os.path.join(ROOT, "logo_master_1024.png")
    icon.save(master)

    # .icns
    iconset = os.path.join(ROOT, "Ravive.iconset")
    shutil.rmtree(iconset, ignore_errors=True)
    os.makedirs(iconset)
    for px in (16, 32, 128, 256, 512):
        icon.resize((px, px), Image.LANCZOS).save(
            os.path.join(iconset, f"icon_{px}x{px}.png")
        )
        icon.resize((px * 2, px * 2), Image.LANCZOS).save(
            os.path.join(iconset, f"icon_{px}x{px}@2x.png")
        )
    subprocess.run(
        ["iconutil", "-c", "icns", iconset, "-o", os.path.join(ROOT, "logo.icns")],
        check=True,
    )
    shutil.rmtree(iconset, ignore_errors=True)

    # In-app header asset. JPEG has no alpha and the header applies its own
    # border-radius, so crop inside the squircle and matte on the body colour —
    # any corner of the superellipse left in frame would show as a light halo.
    inner = int(BODY * 0.88)
    matte = Image.new("RGB", (CANVAS, CANVAS), oklch_to_rgb(*BG))
    matte.paste(icon, (0, 0), icon)
    matte.crop(
        (
            (CANVAS - inner) // 2,
            (CANVAS - inner) // 2,
            (CANVAS + inner) // 2,
            (CANVAS + inner) // 2,
        )
    ).resize((512, 512), Image.LANCZOS).save(
        os.path.join(ROOT, "logo.jpg"), quality=95
    )

    print("wrote logo_master_1024.png, logo.icns, logo.jpg")


if __name__ == "__main__":
    sys.exit(main())
