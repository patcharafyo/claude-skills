#!/usr/bin/env python3
"""Accent palettes for architecture-diagram pages.

Usage:
  python3 accent.py check  PAGE.html     Check every accent preset in a page.
  python3 accent.py make   "#0b6e4f" [NAME]
                                          Turn one brand colour into a ready
                                          :root[data-accent="NAME"] rule with a
                                          light and a dark variant, then check it.

Standard library only (Python 3.8+).

Targets (light page #ffffff, dark page #16181b):
  accent      >= 4.5:1 against the page and >= 3:1 against zones, so arrows
              and outlines stay clear and the colour also works as text.
  accent-soft  the fill of highlighted boxes: titles (ink) on it stay
              >= 7:1, subtitles (muted) >= 4.5:1, and its outline (the
              accent) >= 3:1 against it.
"""
import colorsys
import re
import sys

LIGHT = {"page": "#ffffff", "zone": "#f5f6f8", "ink": "#1c2024", "muted": "#5b6470"}
DARK = {"page": "#16181b", "zone": "#1f2226", "ink": "#eceef0", "muted": "#a3acb6"}


def rgb(hex_):
    h = hex_.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def hexs(c):
    return "#" + "".join("%02x" % round(max(0, min(1, v)) * 255) for v in c)


def lum(c):
    def ch(v):
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = lum(rgb(a)), lum(rgb(b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def mix(a, b, t):
    """t of colour a over colour b."""
    ca, cb = rgb(a), rgb(b)
    return hexs(tuple(t * x + (1 - t) * y for x, y in zip(ca, cb)))


def shift_lightness(hex_, step, ok):
    """Move HLS lightness by step until ok(hex) is true, keeping hue/saturation."""
    h, l, s = colorsys.rgb_to_hls(*rgb(hex_))
    for _ in range(200):
        cur = hexs(colorsys.hls_to_rgb(h, l, s))
        if ok(cur):
            return cur
        l = max(0.0, min(1.0, l + step))
    return cur


def derive(base):
    light = shift_lightness(base, -0.01, lambda c: contrast(c, LIGHT["page"]) >= 4.6)
    dark = shift_lightness(base, +0.01, lambda c: contrast(c, DARK["page"]) >= 6.0)
    return {
        "accent-l": light,
        "accent-soft-l": mix(light, LIGHT["page"], 0.08),
        "accent-d": dark,
        "accent-soft-d": mix(dark, DARK["page"], 0.17),
    }


def report(name, p):
    rows = [
        ("light", "accent vs page", contrast(p["accent-l"], LIGHT["page"]), 4.5),
        ("light", "accent vs zone", contrast(p["accent-l"], LIGHT["zone"]), 3.0),
        ("light", "accent vs soft", contrast(p["accent-l"], p["accent-soft-l"]), 3.0),
        ("light", "ink on soft", contrast(LIGHT["ink"], p["accent-soft-l"]), 7.0),
        ("light", "muted on soft", contrast(LIGHT["muted"], p["accent-soft-l"]), 4.5),
        ("dark", "accent vs page", contrast(p["accent-d"], DARK["page"]), 4.5),
        ("dark", "accent vs zone", contrast(p["accent-d"], DARK["zone"]), 3.0),
        ("dark", "accent vs soft", contrast(p["accent-d"], p["accent-soft-d"]), 3.0),
        ("dark", "ink on soft", contrast(DARK["ink"], p["accent-soft-d"]), 7.0),
        ("dark", "muted on soft", contrast(DARK["muted"], p["accent-soft-d"]), 4.5),
    ]
    ok = all(v >= need for *_, v, need in rows)
    print("%-9s %s" % (name, "PASS" if ok else "FAIL"))
    for mode, what, v, need in rows:
        flag = "" if v >= need else "   <-- below %.1f" % need
        print("   %-5s %-15s %5.2f%s" % (mode, what, v, flag))
    return ok


def rule(name, p):
    return (
        ':root[data-accent="%s"] {\n'
        "  --accent-l: %s; --accent-soft-l: %s;\n"
        "  --accent-d: %s; --accent-soft-d: %s;\n"
        "}" % (name, p["accent-l"], p["accent-soft-l"], p["accent-d"], p["accent-soft-d"])
    )


RULE_RE = re.compile(r':root(?:\[data-accent="([\w-]+)"\])?\s*\{([^}]*--accent-l[^}]*)\}')
VAR_RE = re.compile(r"--(accent-(?:soft-)?[ld])\s*:\s*(#[0-9a-fA-F]{3,6})")


def check(path):
    css = open(path, encoding="utf-8").read()
    found = 0
    ok = True
    for m in RULE_RE.finditer(css):
        values = dict(VAR_RE.findall(m.group(2)))
        if len(values) != 4:
            continue
        found += 1
        ok &= report(m.group(1) or "default", values)
    if not found:
        print("No accent presets found in", path)
        return 1
    return 0 if ok else 1


def main(argv):
    if len(argv) >= 3 and argv[1] == "check":
        return check(argv[2])
    if len(argv) >= 3 and argv[1] == "make":
        base = argv[2] if argv[2].startswith("#") else "#" + argv[2]
        name = argv[3] if len(argv) > 3 else "brand"
        p = derive(base)
        ok = report(name, p)
        print()
        print(rule(name, p))
        return 0 if ok else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
