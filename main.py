#!/usr/bin/env python3
"""Entry point for the news-image-20261126 submission.

Pure standard library: copies the pre-rendered front-page PNG
(``entry.png``, produced by ``render.py`` at authoring time) into the
directory named by ``$MAKEFUN_OUTPUT_DIR`` (``/output`` when the
variable is unset).  Nothing is rendered here, so this runs in a bare
scoring sandbox with no Pillow and no fonts installed.

The image is validated before it is written: it must start with the
PNG signature, its IHDR dimensions must be at most 1024x1024, and its
size must be at most 1 MiB.  A failed check refuses to write anything
and exits non-zero.
"""

import os
import struct
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_WIDTH = 1024
MAX_HEIGHT = 1024
MAX_BYTES = 1024 * 1024

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    return 1


def validate(data):
    if len(data) < 33:
        return "entry.png is too short to be a PNG"
    if data[:8] != PNG_SIGNATURE:
        return "entry.png does not start with the PNG signature"
    if data[12:16] != b"IHDR":
        return "entry.png has no IHDR chunk where one is expected"
    width, height = struct.unpack(">II", data[16:24])
    if width == 0 or height == 0:
        return f"entry.png has invalid dimensions {width}x{height}"
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        return (
            f"entry.png is {width}x{height}, over the "
            f"{MAX_WIDTH}x{MAX_HEIGHT} limit"
        )
    if len(data) > MAX_BYTES:
        return f"entry.png is {len(data)} bytes, over the {MAX_BYTES} limit"
    return None


def main():
    try:
        with open(SOURCE, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        return fail(f"cannot read {SOURCE}: {exc}")

    problem = validate(data)
    if problem is not None:
        return fail(problem)

    target_dir = output_dir()
    target = os.path.join(target_dir, "entry.png")
    try:
        os.makedirs(target_dir, exist_ok=True)
        with open(target, "wb") as handle:
            handle.write(data)
    except OSError as exc:
        return fail(f"cannot write {target}: {exc}")

    print(f"wrote {target} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
