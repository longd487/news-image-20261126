#!/usr/bin/env python3
"""Entry point for the news-image-20261126 submission.

Writes the front-page PNG produced by ``render.py`` to the directory
named by ``$MAKEFUN_OUTPUT_DIR`` (``/output`` when the variable is
unset).  The bytes written here are exactly the bytes ``render.py``
writes to ``entry.png`` next to itself, because both go through the
same ``render.png_bytes()`` call.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import render  # noqa: E402  (imported after the path fix above)


def output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    data = render.png_bytes()
    target_dir = output_dir()
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(data)
    print(f"wrote {target} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
