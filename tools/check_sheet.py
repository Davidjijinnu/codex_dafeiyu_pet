"""Basic v2 sprite-sheet format checks; this is not animation/identity QA."""

import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

COUNTS = (6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sheet", type=Path)
    args = parser.parse_args()
    data = args.sheet.read_bytes()
    errors = []
    with Image.open(args.sheet) as source:
        if source.format not in ("PNG", "WEBP"):
            errors.append("Expected PNG or WebP encoding")
        if source.size != (1536, 2288):
            errors.append(f"Expected 1536x2288, got {source.size}")
        if source.mode not in ("RGBA", "LA") and "transparency" not in source.info:
            errors.append("The sheet has no transparency channel")
        image = source.convert("RGBA")
    if not 0 < len(data) <= 20 * 1024 * 1024:
        errors.append("The encoded file must be nonempty and no larger than 20 MiB")
    if image.size == (1536, 2288):
        for row, count in enumerate(COUNTS):
            for col in range(8):
                cell = image.crop((col * 192, row * 208,
                                   (col + 1) * 192, (row + 1) * 208))
                alpha = cell.getchannel("A")
                if col < count and alpha.getbbox() is None:
                    errors.append(f"Missing artwork at row {row}, column {col}")
                if col >= count and alpha.getbbox() is not None:
                    errors.append(f"Unused cell is occupied: row {row}, column {col}")
        if image.getchannel("A").getextrema()[0] != 0:
            errors.append("No fully transparent background pixels found")
    print(json.dumps({"ok": not errors, "size": image.size,
                      "required_frames": sum(COUNTS), "bytes": len(data),
                      "sha256": hashlib.sha256(data).hexdigest(),
                      "errors": errors}, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
