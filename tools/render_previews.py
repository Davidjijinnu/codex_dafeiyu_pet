"""Render GIF previews from the encoded v2 sheet with fixed cell bounds."""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw

STATES = (
    ("idle", [280, 110, 110, 140, 140, 320]),
    ("running-right", [120] * 7 + [220]),
    ("running-left", [120] * 7 + [220]),
    ("waving", [140] * 3 + [280]),
    ("jumping", [140] * 4 + [280]),
    ("failed", [140] * 7 + [240]),
    ("waiting", [150] * 5 + [260]),
    ("running", [120] * 5 + [220]),
    ("review", [150] * 5 + [280]),
)


def save(frames, durations, path):
    frames[0].save(path, save_all=True, append_images=frames[1:],
                   duration=durations, loop=0, disposal=2, optimize=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sheet", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("build/previews"))
    args = parser.parse_args()
    image = Image.open(args.sheet).convert("RGBA")
    if image.size != (1536, 2288):
        parser.error("Expected a 1536x2288 v2 sheet")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    def cell(row, col):
        return image.crop((col * 192, row * 208,
                           (col + 1) * 192, (row + 1) * 208))

    combined, timing = [], []
    for row, (name, durations) in enumerate(STATES):
        frames = [cell(row, col) for col in range(len(durations))]
        save(frames, durations, args.output_dir / f"{name}.gif")
        for frame in frames:
            card = Image.new("RGBA", (240, 260), "#e9f3ed")
            card.alpha_composite(frame, (24, 16))
            ImageDraw.Draw(card).text((12, 237), name, fill="#18332d")
            combined.append(card.convert("RGB"))
        timing.extend(durations)
    save(combined, timing, args.output_dir / "all-states.gif")
    transition = [cell(0, 0)] + [cell(4, i) for i in range(5)] + [cell(0, 0)]
    save(transition, [450, 140, 140, 140, 140, 280, 450],
         args.output_dir / "idle-jump-idle.gif")
    directions = [cell(9 + i // 8, i % 8) for i in range(16)]
    save(directions, [180] * 16, args.output_dir / "look-loop.gif")
    print(f"Rendered previews to {args.output_dir}")


if __name__ == "__main__":
    main()
