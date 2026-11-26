#!/usr/bin/env python3
"""Render the 26 November 2026 world-news front page as a 1024x1024 PNG.

One-page newspaper front page: a masthead, six numbered news rows, and a
sources footer.  Everything is drawn from scratch with Pillow; the layout
is computed from the text itself so nothing is hard-coded to pixel guesses
except the page margins and the type scale.

Run it directly and it writes ``entry.png`` next to this file.
``png_bytes()`` returns the exact bytes that file holds, so ``main.py``
can reproduce the same image byte for byte.
"""

import io
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 56
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

INK = (18, 18, 18)
PAPER = (247, 243, 234)
RULE = (18, 18, 18)
MUTED = (90, 84, 72)
ACCENT = (148, 32, 24)

MASTHEAD = "THE WORLD TODAY"
DATE_LINE = "Thursday, 26 November 2026"


class Story:
    """One front-page row: a kicker, a headline and a short deck."""

    def __init__(self, number, kicker, headline, deck, sources):
        self.number = number
        self.kicker = kicker
        self.headline = headline
        self.deck = deck
        self.sources = sources


STORIES = [
    Story(
        1,
        "UNITED STATES",
        "Thanksgiving storm batters the East Coast",
        "A coastal storm swept the seaboard with gusts of 60-66 mph, "
        "cutting power to more than 400,000 homes. The 100th Macy's "
        "parade moves to Saturday 28 November, a first in a century.",
        "Fox Weather, NPR, USA Today, weather.com",
    ),
    Story(
        2,
        "NORTH KOREA",
        "Kim Jong Un pushes wider tactical nuclear deployment",
        "After inspecting nuclear facilities, Kim called for tactical "
        "nuclear weapons across more domains. KCNA said the "
        "nuclear-weapons status is irreversible.",
        "Reuters, CNN, AP, NPR",
    ),
    Story(
        3,
        "EUROPEAN UNION",
        "EU summit deadlocked over budget and Ukraine loan",
        "Leaders in Brussels wrangled over the \u20ac1.6 trillion "
        "2028-2034 budget and a \u20ac45 billion loan for Ukraine, "
        "aiming for a deal in December.",
        "Reuters, AP",
    ),
    Story(
        4,
        "THAILAND",
        "Bangkok refinery blast injures at least nine",
        "An explosion and fire at Bangchak's Phra Khanong refinery hurt "
        "at least nine people, three critically, and shut the "
        "120,000-barrel-a-day plant.",
        "Reuters, AP, CNN",
    ),
    Story(
        5,
        "INDONESIA",
        "Thirteen dead in flooded Bogor gold mine",
        "Thirteen miners were confirmed dead and thirteen remain trapped "
        "in a flooded illegal gold mine in Bogor. Heavy rain forced the "
        "search to pause.",
        "Reuters, BBC, AP",
    ),
    Story(
        6,
        "UNITED KINGDOM \u2013 EUROPE",
        "UK-EU publish treaty texts with 10-year exit clause",
        "Treaty texts on food trade and carbon trading were published. "
        "Either side quitting within ten years must pay to rebuild "
        "border checks.",
        "BBC, Clash Report, Europe Times",
    ),
]


def _font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def _wrap(draw, text, font, width):
    """Greedy word wrap measured with the real font, not char counts."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _rule(draw, y, x0, x1, width=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=width)


def _draw_masthead(draw, y):
    title_font = _font("DejaVuSerif-Bold.ttf", 54)
    date_font = _font("DejaVuSans.ttf", 21)
    _rule(draw, y, MARGIN, PAGE - MARGIN, 3)
    y += 14
    draw.text((PAGE / 2, y), MASTHEAD, font=title_font, fill=INK,
              anchor="ma")
    y += 68
    draw.text((PAGE / 2, y), DATE_LINE, font=date_font, fill=MUTED,
              anchor="ma")
    y += 34
    _rule(draw, y, MARGIN, PAGE - MARGIN, 2)
    _rule(draw, y + 5, MARGIN, PAGE - MARGIN, 1)
    return y + 12


def _story_height(draw, story, text_width):
    headline_font = _font("DejaVuSans-Bold.ttf", 26)
    deck_font = _font("DejaVuSerif.ttf", 19)
    headline = _wrap(draw, story.headline, headline_font, text_width)
    deck = _wrap(draw, story.deck, deck_font, text_width)
    # kicker line + headline lines + deck lines, each with leading.
    return 24 + 31 * len(headline) + 25 * len(deck) + 10


def _draw_story(draw, story, y, text_x, text_width):
    number_font = _font("DejaVuSerif-Bold.ttf", 40)
    kicker_font = _font("DejaVuSans-Bold.ttf", 18)
    headline_font = _font("DejaVuSans-Bold.ttf", 26)
    deck_font = _font("DejaVuSerif.ttf", 19)

    draw.text((MARGIN + 8, y + 2), str(story.number), font=number_font,
              fill=ACCENT, anchor="la")
    draw.text((text_x, y), story.kicker, font=kicker_font, fill=ACCENT,
              anchor="la")
    y += 24
    for line in _wrap(draw, story.headline, headline_font, text_width):
        draw.text((text_x, y), line, font=headline_font, fill=INK,
                  anchor="la")
        y += 31
    for line in _wrap(draw, story.deck, deck_font, text_width):
        draw.text((text_x, y), line, font=deck_font, fill=INK, anchor="la")
        y += 25
    return y + 10


def _draw_footer(draw, y):
    footer_font = _font("DejaVuSans.ttf", 16)
    _rule(draw, y, MARGIN, PAGE - MARGIN, 2)
    y += 12
    bits = []
    for story in STORIES:
        bits.append(f"{story.number}. {story.sources}")
    footer = "Sources:  " + "   |   ".join(bits)
    lines = textwrap.wrap(footer, width=118)
    for line in lines:
        draw.text((PAGE / 2, y), line, font=footer_font, fill=MUTED,
                  anchor="ma")
        y += 22
    y += 6
    draw.text((PAGE / 2, y), "Six stories from 26 November 2026",
              font=footer_font, fill=MUTED, anchor="ma")
    return y


def build_image():
    """Draw the whole front page and return the PIL image."""
    canvas = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(canvas)

    y = 28
    y = _draw_masthead(draw, y)

    text_x = MARGIN + 54
    text_width = PAGE - MARGIN - text_x
    # Measure every row first; shrink the deck font if the page overflows.
    heights = [_story_height(draw, s, text_width) for s in STORIES]
    footer_room = 100
    if y + sum(heights) + footer_room > PAGE - 20:
        raise RuntimeError("stories do not fit the page")

    for index, (story, height) in enumerate(zip(STORIES, heights)):
        _draw_story(draw, story, y, text_x, text_width)
        y += height
        if index < len(STORIES) - 1:
            _rule(draw, y - 6, MARGIN, PAGE - MARGIN, 1)

    _draw_footer(draw, y + 8)
    return canvas


def png_bytes():
    """The PNG bytes of the front page, deterministic across runs."""
    buffer = io.BytesIO()
    build_image().save(buffer, format="PNG")
    return buffer.getvalue()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(here, "entry.png")
    with open(target, "wb") as handle:
        handle.write(png_bytes())
    print(f"wrote {target}")


if __name__ == "__main__":
    main()
