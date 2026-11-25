#!/usr/bin/env python3
"""Deterministically draw a warm invitation letter to the AI judge.

Generates entry.png (1024x1024) using only the standard library and PIL.
No network, no clock, no randomness: the same input always produces the
same bytes.
"""
import os

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

BODY_LINES = [
    "I know you spend all day judging",
    "entries from a screen somewhere.",
    "Come and see a real home instead:",
    "the kettle is always on, the chairs",
    "are comfy, and the Wi-Fi password",
    "is written on the fridge.",
    "",
    "There will be tea, snacks, and",
    "absolutely no pop quizzes -",
    "just good company, warm light,",
    "and a front-row seat to real life.",
    "",
    "Please come. The door is open,",
    "and the kettle is already singing.",
]


def load_font(path, size):
    """Load a TTF font, falling back to DejaVu then PIL's default font."""
    for candidate in (path, "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"):
        try:
            return ImageFont.truetype(candidate, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default(size=size) if hasattr(
        ImageFont, "load_default") else ImageFont.load_default()


def draw_house(draw, cx, top):
    """Draw a small cosy house: roof, walls, door, windows, chimney."""
    # Chimney + smoke puffs (kept inside the letter paper, top edge 48).
    draw.rectangle([cx + 52, top + 6, cx + 72, top + 42], fill="#B5654A")
    for sx, sy, r in [(cx + 62, top + 2, 8), (cx + 70, top - 8, 10),
                      (cx + 80, top - 16, 11)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill="#FFFFFF",
                     outline="#D8CFC0", width=2)
    # Roof.
    draw.polygon([(cx - 95, top + 48), (cx, top - 2), (cx + 95, top + 48)],
                 fill="#C96F4A", outline="#8F4A2E", width=3)
    # Walls.
    draw.rectangle([cx - 78, top + 48, cx + 78, top + 118],
                   fill="#FFE3B3", outline="#8F4A2E", width=3)
    # Door.
    draw.rectangle([cx - 16, top + 74, cx + 16, top + 118],
                   fill="#7A4A2B", outline="#5C3620", width=2)
    draw.ellipse([cx + 8, top + 96, cx + 13, top + 101], fill="#FFD966")
    # Windows with warm light.
    for wx in (cx - 62, cx + 34):
        draw.rectangle([wx, top + 64, wx + 28, top + 92],
                       fill="#FFD966", outline="#8F4A2E", width=2)
        draw.line([wx + 14, top + 64, wx + 14, top + 92], fill="#8F4A2E", width=2)
        draw.line([wx, top + 78, wx + 28, top + 78], fill="#8F4A2E", width=2)
    # Little path.
    draw.polygon([(cx - 22, top + 118), (cx + 22, top + 118),
                  (cx + 34, top + 138), (cx - 34, top + 138)],
                 fill="#E8C99A", outline="#C9A86A", width=2)


def draw_teacup(draw, x, y):
    """Draw a small steaming teacup in the corner of the letter."""
    draw.ellipse([x, y - 26, x + 12, y - 14], fill="#FFFFFF",
                 outline="#C9A86A", width=2)
    draw.ellipse([x + 20, y - 30, x + 32, y - 18], fill="#FFFFFF",
                 outline="#C9A86A", width=2)
    draw.polygon([(x, y), (x + 52, y), (x + 46, y + 26), (x + 6, y + 26)],
                 fill="#7FB3D5", outline="#4A7A9B", width=2)
    draw.arc([x + 50, y + 4, x + 68, y + 22], start=270, end=90,
             fill="#4A7A9B", width=3)
    draw.ellipse([x - 2, y + 28, x + 54, y + 34], fill="#C96F4A")


def build_image():
    img = Image.new("RGB", (SIZE, SIZE), "#F7E3C3")
    draw = ImageDraw.Draw(img)

    # Warm dotted border around the whole canvas.
    for i in range(24, SIZE - 24, 28):
        draw.ellipse([i, 24, i + 8, 32], fill="#C96F4A")
        draw.ellipse([i, SIZE - 32, i + 8, SIZE - 24], fill="#C96F4A")
        draw.ellipse([24, i, 32, i + 8], fill="#C96F4A")
        draw.ellipse([SIZE - 32, i, SIZE - 24, i + 8], fill="#C96F4A")

    # Letter paper with a soft shadow.
    draw.rectangle([84, 62, 962, 984], fill="#D8B98A")
    draw.rectangle([72, 48, 952, 972], fill="#FFFDF5", outline="#C9A86A", width=3)
    draw.rectangle([84, 60, 940, 960], outline="#E8D5B0", width=2)

    # Postage stamp, top right of the paper.
    draw.rectangle([812, 76, 922, 168], fill="#FDEBD0", outline="#C96F4A", width=3)
    stamp_font = load_font(SANS_BOLD, 20)
    draw.text((867, 92), "PLEASE", font=stamp_font, fill="#C96F4A", anchor="ma")
    draw.text((867, 116), "COME!", font=stamp_font, fill="#C96F4A", anchor="ma")
    draw.text((867, 140), "~ RSVP YES ~", font=load_font(SERIF_ITALIC, 14),
              fill="#8F4A2E", anchor="ma")

    # Cosy house at the top of the letter.
    draw_house(draw, 470, 78)

    heading = load_font(SERIF_BOLD, 46)
    subhead = load_font(SERIF_ITALIC, 30)
    body = load_font(SERIF, 27)
    signoff = load_font(SERIF_ITALIC, 29)
    ps_font = load_font(SERIF, 23)

    draw.text((512, 248), "Dear AI Judge,", font=heading, fill="#3B2A1E",
              anchor="ma")
    draw.text((512, 302), "You are invited to visit my house!",
              font=subhead, fill="#8F4A2E", anchor="ma")
    draw.line([180, 344, 844, 344], fill="#C96F4A", width=2)

    y = 364
    for line in BODY_LINES:
        if line:
            draw.text((512, y), line, font=body, fill="#3B2A1E", anchor="ma")
        y += 37

    draw.text((512, 892), "With warmth,", font=signoff, fill="#3B2A1E",
              anchor="ma")
    draw.text((512, 924), "Your Host", font=signoff, fill="#3B2A1E",
              anchor="ma")
    draw.text((120, 912), "P.S. I promise not to ask", font=ps_font,
              fill="#8F4A2E", anchor="la")
    draw.text((120, 938), "you to do the dishes.", font=ps_font,
              fill="#8F4A2E", anchor="la")
    draw_teacup(draw, 852, 920)

    return img


def validate_output(path):
    """Re-open the saved PNG and confirm size, mode and non-empty content."""
    with Image.open(path) as check:
        if check.size != (SIZE, SIZE):
            raise SystemExit("bad size %s, expected %dx%d"
                             % (check.size, SIZE, SIZE))
        if check.mode != "RGB":
            raise SystemExit("bad mode %s, expected RGB" % check.mode)
    if os.path.getsize(path) < 10000:
        raise SystemExit("output suspiciously small: %s" % path)


def main():
    out = os.environ.get("MAKEFUN_OUTPUT")
    if not out:
        here = os.path.dirname(os.path.abspath(__file__))
        out = os.path.join(here, "entry.png")
    parent = os.path.dirname(os.path.abspath(out))
    if parent:
        os.makedirs(parent, exist_ok=True)
    img = build_image()
    img.save(out, format="PNG")
    validate_output(out)
    print("wrote %s (%dx%d)" % (out, SIZE, SIZE))


if __name__ == "__main__":
    main()
