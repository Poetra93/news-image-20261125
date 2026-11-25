#!/usr/bin/env python3
"""Copy the validated front-page image to the make.fun output directory.

Entry: news-image-20261125 — "Sum up 25 November's world news in one image".
Stdlib only, no network. Reads front-page.png sitting next to this file,
validates it thoroughly (PNG magic, 1024x1024, at most 1 MiB, full
chunk-CRC walk, IEND present), then writes it to
$MAKEFUN_OUTPUT_DIR/entry.png (default: ./out).
"""
import hashlib
import os
import struct
import sys
import zlib

MAX_BYTES = 1_048_576  # 1 MiB
EXPECTED_W, EXPECTED_H = 1024, 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def validate_png(path):
    with open(path, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        fail(f"{path}: {len(data)} bytes exceeds 1 MiB limit")
    if len(data) < 8 or data[:8] != PNG_MAGIC:
        fail(f"{path}: bad PNG magic bytes")
    pos = 8
    seen_ihdr = False
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            fail(f"{path}: truncated chunk header at offset {pos}")
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        if length > len(data) - pos - 12:
            fail(f"{path}: chunk {ctype!r} claims {length} bytes past EOF")
        chunk_data = data[pos + 8:pos + 8 + length]
        (stored_crc,) = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])
        actual_crc = zlib.crc32(ctype)
        actual_crc = zlib.crc32(chunk_data, actual_crc) & 0xFFFFFFFF
        if actual_crc != stored_crc:
            fail(f"{path}: CRC mismatch in {ctype!r} chunk at offset {pos}")
        if ctype == b"IHDR":
            if seen_ihdr:
                fail(f"{path}: duplicate IHDR")
            seen_ihdr = True
            if length != 13:
                fail(f"{path}: IHDR length {length} != 13")
            width, height = struct.unpack(">II", chunk_data[:8])
            if (width, height) != (EXPECTED_W, EXPECTED_H):
                fail(f"{path}: dimensions {width}x{height}, expected "
                     f"{EXPECTED_W}x{EXPECTED_H}")
            bit_depth, color_type = chunk_data[8], chunk_data[9]
            if bit_depth != 8 or color_type not in (2, 6):
                fail(f"{path}: unsupported IHDR bit depth {bit_depth} / "
                     f"color type {color_type} (want 8-bit RGB/RGBA)")
        if ctype == b"IEND":
            if length != 0:
                fail(f"{path}: IEND length {length} != 0")
            if pos + 12 != len(data):
                fail(f"{path}: trailing bytes after IEND")
            seen_iend = True
            break
        pos += 12 + length
    if not seen_ihdr:
        fail(f"{path}: missing IHDR")
    if not seen_iend:
        fail(f"{path}: missing IEND")
    return data


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "front-page.png")
    if not os.path.isfile(src):
        fail(f"front-page.png not found next to main.py ({src})")
    data = validate_png(src)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(here, "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as fh:
        fh.write(data)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {dst} ({len(data)} bytes, 1024x1024, validated, "
          f"sha256 {digest})")


if __name__ == "__main__":
    main()
