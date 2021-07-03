import os
import sys

import png

end = "\x1b[0m"
lowerhb = "\u2584"
higherhb = "\u2580"
br = 0
scr = 1  # SCaling Ratio
scr_impl = ""
oldstyle = ""
[term_h, term_w] = os.popen("stty size", "r").read().split(" ")
[term_h, term_w] = [int(term_h), int(term_w)]
if len(sys.argv) == 5:
    normarg = sys.argv[-4]
    br = int(sys.argv[-3])
    oldstyle = sys.argv[-2]
    scr = float(sys.argv[-1])
    scr_impl = "okay"
elif len(sys.argv) == 4:
    normarg = sys.argv[-3]
    br = int(sys.argv[-2])
    oldstyle = sys.argv[-1]
elif len(sys.argv) == 3:
    normarg = sys.argv[-2]
    br = int(sys.argv[-1])
elif len(sys.argv) == 2:
    normarg = sys.argv[-1]
else:
    normarg = sys.argv[-1]
    if not normarg.endswith(".png"):
        print("Error: No .png file selected")
        print("Usage: pngbanner image [brightness] [oldstyle] [scale]")
        print("\n Oldstyle argument should be true or false")
        sys.exit()
rd = png.Reader(normarg)
width, height, data, other = rd.read_flat()
isalpha = other["alpha"]
print(f"{width}x{height}")
scr_w = width / term_w
scr_h = height / term_h
plt = ("palette" in other, other.get("palette", ()))
th = int(height / scr)
tw = int(width / scr)
# if scr_impl=="": scr=int(scr_h)


def DrawImage(data, tw, th, plt):
    x, y = (0, 0)
    while y < th / 2:
        x = 0
        while x < tw:
            nx = int(scr * x)
            ny = int(scr * y) * 2
            nx1 = nx + (ny * width)
            nx2 = (
                (nx + ((ny - 1) * width)) if ny - 1 > 0 else (nx + ((ny) * width))
            )  # ugly fix
            if not plt[0]:
                p = (
                    data[nx1 * 4 : (nx1 + 1) * 4]
                    if isalpha == True
                    else data[nx1 * 3 : (nx1 + 1) * 3]
                )
                q = (
                    data[nx2 * 4 : (nx2 + 1) * 4]
                    if isalpha == True
                    else data[nx2 * 3 : (nx2 + 1) * 3]
                )
            else:
                p = plt[1][data[nx1]]
                q = plt[1][data[nx2]]
            r, g, b = (p[0], p[1], p[2]) if len(p) >= 3 else (0, 0, 0)
            r1, g1, b1 = (q[0], q[1], q[2]) if len(q) >= 3 else (0, 0, 0)
            draw = f"\x1b[48;2;{max(0, r + br)};{max(0, g + br)};{max(0, b + br)}m"
            draw1 = f"\x1b[38;2;{max(0, r1 + br)};{max(0, g1 + br)};{max(0, b1 + br)}m"
            x += 1
            print(f"{draw}{draw1}{higherhb}{end}", end="", flush=True) if (
                oldstyle == "false" or oldstyle != "true"
            ) else print(f"{draw}#{end}", end="")
        print()
        y += 1


DrawImage(data, tw, th, plt)
