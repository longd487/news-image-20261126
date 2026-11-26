#!/usr/bin/env python3
"""Write this entry's image to the grader's output directory.

The entry is a program that places one image at /output/entry.png. The
image is the one this repository holds (entry.png): a 1024x1024 front
page summing up Thursday 26 November 2026 in six stories, researched
from Reuters, AP, CNN, the BBC and Fox Weather:

  USA          Thanksgiving storm batters the US
  NORTH KOREA  Kim urges wider nuclear deployment
  EUROPE       EU leaders split over budget, Ukraine loan
  THAILAND     Bangkok refinery blast injures nine
  INDONESIA    13 dead in flooded Indonesian mine
  BRITAIN      UK-EU treaties carry 10-year exit clause

Placing a copy, rather than rendering at run time, is deliberate:

  * the bounty wants no network and byte-identical output on every run;
    a copy is deterministic by construction;
  * rendering needs Pillow and fonts, which the grading sandbox may not
    have; copying needs only the standard library.

Before placing it, the program checks the image against the bounty's
limits (PNG, at most 1024x1024 pixels, at most 1 MiB) and refuses to
write anything that fails them, so a bad asset can never become a bad
entry. The picture itself was drawn by render.py in this repository.
"""

from pathlib import Path
import os
import shutil
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"

# The grader writes to /output; outside its container MAKEFUN_OUTPUT_DIR
# stands in for it (the starter's convention), so a local run can point
# the output elsewhere without touching the program.
DEST_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
DEST = DEST_DIR / "entry.png"

MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def png_size(path):
    """Return (width, height) of the PNG at `path`, or raise ValueError."""
    data = path.read_bytes()
    if data[:8] != PNG_MAGIC:
        raise ValueError(f"{path}: not a PNG file")
    # The IHDR chunk sits right after the 8-byte magic: 4-byte length,
    # 4-byte type ("IHDR"), 13 bytes of data, 4-byte CRC.
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise ValueError(f"{path}: no IHDR chunk")
    if int.from_bytes(data[8:12], "big") != 13:
        raise ValueError(f"{path}: bad IHDR length")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    return width, height


def main():
    if not SOURCE.is_file():
        print(f"error: {SOURCE} is missing", file=sys.stderr)
        return 1

    nbytes = SOURCE.stat().st_size
    if nbytes > MAX_BYTES:
        print(f"error: entry.png is {nbytes} bytes, over the 1 MiB limit",
              file=sys.stderr)
        return 1

    try:
        width, height = png_size(SOURCE)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if width > MAX_SIDE or height > MAX_SIDE:
        print(f"error: entry.png is {width}x{height}, over the 1024x1024 limit",
              file=sys.stderr)
        return 1

    DEST_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)

    # The copy is byte-identical to the source by construction; confirm it.
    if DEST.stat().st_size != nbytes:
        print("error: output size does not match the source", file=sys.stderr)
        return 1

    print(f"wrote {DEST} ({width}x{height}, {nbytes} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
