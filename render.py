#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news summary (1024x1024 PNG).

The picture is a one-page newspaper front: a navy masthead, six
colour-coded story rows, and a source line at the foot. Every story was
researched on 2026-11-26 from Reuters, AP, CNN, the BBC and Fox Weather;
the wording and the sources are documented in README.md.

Run it from anywhere: it writes entry.png next to this file.
"""

import os
from PIL import Image, ImageDraw, ImageFont

# --- canvas ---------------------------------------------------------------
CANVAS_W, CANVAS_H = 1024, 1024
MASTHEAD_H = 148
FOOT_H = 36
ROWS = 6
ROW_H = (CANVAS_H - MASTHEAD_H - FOOT_H) // ROWS  # 140
GUTTER = 48
TEXT_X = 112
NUM_COL_W = 84

# --- palette --------------------------------------------------------------
PALETTE = {
    "navy": (11, 34, 57),
    "ink": (18, 28, 40),
    "grey": (58, 68, 80),
    "paper": (244, 246, 248),
    "white": (255, 255, 255),
    "mist": (196, 210, 224),
    "rule": (214, 220, 226),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def load(name, size):
    """Load one DejaVu face at the given point size."""
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


FONTS = {
    "title": load("DejaVuSans-Bold.ttf", 52),
    "date": load("DejaVuSans.ttf", 28),
    "kicker": load("DejaVuSans-Bold.ttf", 22),
    "head": load("DejaVuSans-Bold.ttf", 34),
    "body": load("DejaVuSans.ttf", 25),
    "num": load("DejaVuSans-Bold.ttf", 44),
    "foot": load("DejaVuSans.ttf", 20),
}

# --- the day in six rows ---------------------------------------------------
# Each row: (accent colour, kicker, headline, deck)
STORIES = [
    ((192, 57, 43), "USA", "Thanksgiving storm batters the US",
     "A coastal storm lashed the East Coast with 60 mph gusts and 400,000 outages; the 100th Macy's parade moved to Saturday."),
    ((142, 68, 173), "NORTH KOREA", "Kim urges wider nuclear deployment",
     "Kim Jong Un told officials to deploy tactical nuclear weapons across multiple domains; KCNA called the arsenal irreversible."),
    ((36, 113, 163), "EUROPE", "EU leaders split over budget, Ukraine loan",
     "Leaders in Brussels wrestled over a 1.6 trillion euro budget and a 45 billion euro loan for Ukraine, aiming for a deal in December."),
    ((185, 119, 14), "THAILAND", "Bangkok refinery blast injures nine",
     "An explosion and fire at Bangchak's Bangkok refinery injured at least nine people and shut the 120,000-barrel-a-day plant."),
    ((17, 122, 101), "INDONESIA", "13 dead in flooded Indonesian mine",
     "Thirteen miners were confirmed dead and 13 remain trapped in a flooded illegal gold mine in Bogor; rain halted the search."),
    ((101, 67, 33), "BRITAIN", "UK-EU treaties carry 10-year exit clause",
     "The UK and EU published food-trade and emissions treaty texts; quitting within 10 years means paying to rebuild border checks."),
]


def flow_lines(draw, font, text, width):
    """Split text into lines that each fit `width` pixels (greedy)."""
    words = text.split()
    lines = []
    while words:
        line = words.pop(0)
        while words:
            trial = line + " " + words[0]
            if draw.textlength(trial, font=font) > width:
                break
            line = trial
            words.pop(0)
        lines.append(line)
    return lines


def paint_masthead(draw):
    draw.rectangle([0, 0, CANVAS_W, MASTHEAD_H], fill=PALETTE["navy"])
    draw.text((GUTTER, 26), "THE WORLD TODAY", font=FONTS["title"], fill=PALETTE["white"])
    draw.text((GUTTER, 96), "Thursday, 26 November 2026  ·  Six stories that defined the day",
              font=FONTS["date"], fill=PALETTE["mist"])


def paint_row(draw, index, story, top):
    accent, kicker, head, deck = story
    bottom = top + ROW_H
    fill = PALETTE["white"] if index % 2 == 0 else PALETTE["paper"]
    draw.rectangle([0, top, CANVAS_W, bottom], fill=fill)
    draw.rectangle([0, top, NUM_COL_W, bottom], fill=accent)
    label = str(index + 1)
    label_w = draw.textlength(label, font=FONTS["num"])
    draw.text((NUM_COL_W / 2 - label_w / 2, top + ROW_H / 2 - 30), label,
              font=FONTS["num"], fill=PALETTE["white"])
    draw.text((TEXT_X, top + 10), kicker, font=FONTS["kicker"], fill=accent)
    draw.text((TEXT_X, top + 38), head, font=FONTS["head"], fill=PALETTE["ink"])
    wrapped = flow_lines(draw, FONTS["body"], deck, CANVAS_W - TEXT_X - GUTTER)
    line_y = top + 84
    for piece in wrapped[:2]:
        draw.text((TEXT_X, line_y), piece, font=FONTS["body"], fill=PALETTE["grey"])
        line_y += 31
    if index < ROWS - 1:
        draw.line([0, bottom, CANVAS_W, bottom], fill=PALETTE["rule"], width=1)


def paint_foot(draw):
    foot_y = CANVAS_H - FOOT_H
    draw.rectangle([0, foot_y, CANVAS_W, CANVAS_H], fill=PALETTE["navy"])
    draw.text((GUTTER, foot_y + 7),
              "Sources: Reuters, AP, CNN, BBC, Fox Weather  ·  Image: make.fun news-image-20261126",
              font=FONTS["foot"], fill=PALETTE["mist"])


def check_fit(draw):
    """Refuse to save if a headline or deck would overflow its row."""
    for accent, kicker, head, deck in STORIES:
        head_w = draw.textlength(head, font=FONTS["head"])
        if head_w > CANVAS_W - TEXT_X - GUTTER:
            raise SystemExit(f"headline too wide ({head_w:.0f}px): {head}")
        wrapped = flow_lines(draw, FONTS["body"], deck, CANVAS_W - TEXT_X - GUTTER)
        if len(wrapped) > 2:
            raise SystemExit(f"deck wraps to {len(wrapped)} lines: {deck}")


def main():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), PALETTE["white"])
    draw = ImageDraw.Draw(img)
    paint_masthead(draw)
    for i, story in enumerate(STORIES):
        paint_row(draw, i, story, MASTHEAD_H + i * ROW_H)
    paint_foot(draw)
    check_fit(draw)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("saved", out, os.path.getsize(out), "bytes;", img.size)


if __name__ == "__main__":
    main()
