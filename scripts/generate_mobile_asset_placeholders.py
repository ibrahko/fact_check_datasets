#!/usr/bin/env python3
"""Generate placeholder PNG assets for the Check-IA mobile app.

Runs automatically as a postinstall hook (npm install) so the assets
exist before `expo prebuild` processes them.
"""
import pathlib
import struct
import zlib

MOBILE_DIR = pathlib.Path(__file__).parent.parent / "mobile"
ASSETS_DIR = MOBILE_DIR / "assets"

ASSETS = {
    "icon.png": (1024, 1024, (37, 99, 235)),
    "adaptive-icon.png": (1024, 1024, (37, 99, 235)),
    "splash.png": (1284, 2778, (255, 255, 255)),
    "favicon.png": (48, 48, (37, 99, 235)),
}


def _png_chunk(name: bytes, data: bytes) -> bytes:
    crc = zlib.crc32(name + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + name + data + struct.pack(">I", crc)


def make_png(width: int, height: int, color: tuple) -> bytes:
    r, g, b = color
    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = _png_chunk(
        b"IHDR",
        struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0),
    )
    raw = b"".join(
        b"\x00" + bytes([r, g, b]) * width for _ in range(height)
    )
    idat = _png_chunk(b"IDAT", zlib.compress(raw))
    iend = _png_chunk(b"IEND", b"")
    return signature + ihdr + idat + iend


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    for name, (width, height, color) in ASSETS.items():
        path = ASSETS_DIR / name
        if path.exists() and path.stat().st_size > 0:
            print(f"skip {path} (already non-empty)")
            continue
        data = make_png(width, height, color)
        path.write_bytes(data)
        print(f"wrote {path} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
