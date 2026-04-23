#!/usr/bin/env python3
"""Generate a simple EdgeTX theme logo from theme.yml color keys."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow required. Run: uv sync", file=sys.stderr)
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("PyYAML required. Run: uv sync", file=sys.stderr)
    sys.exit(1)

_RGB_RE = re.compile(r"^RGB\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$", re.IGNORECASE)
_RGB_HEX_RE = re.compile(
    r"^RGB\(\s*(0x[0-9A-Fa-f]{1,2})\s*,\s*(0x[0-9A-Fa-f]{1,2})\s*,\s*(0x[0-9A-Fa-f]{1,2})\s*\)$",
    re.IGNORECASE,
)


def _parse_color(value: object) -> tuple[int, int, int]:
    """Parse EdgeTX color values (int, 0xRRGGBB, RGB(...)) into RGB tuple."""
    if isinstance(value, int):
        if 0 <= value <= 0xFFFFFF:
            return (value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF
        raise ValueError(f"integer color out of range: {value}")

    s = str(value).strip()
    if s.startswith(("0x", "0X")):
        hex_part = s[2:]
        if len(hex_part) != 6 or any(c not in "0123456789abcdefABCDEF" for c in hex_part):
            raise ValueError(f"invalid hex color: {value!r}")
        packed = int(hex_part, 16)
        return (packed >> 16) & 0xFF, (packed >> 8) & 0xFF, packed & 0xFF

    match = _RGB_RE.match(s) or _RGB_HEX_RE.match(s)
    if not match:
        raise ValueError(f"unsupported color format: {value!r}")

    rgb = tuple(int(part, 0) for part in match.groups())
    if not all(0 <= part <= 255 for part in rgb):
        raise ValueError(f"RGB values out of range: {value!r}")
    return rgb  # type: ignore[return-value]


def _load_theme_colors(theme_yml: Path) -> dict[str, object]:
    with theme_yml.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError("theme.yml top-level value must be a mapping")

    colors = data.get("colors")
    if not isinstance(colors, dict):
        raise ValueError("theme.yml missing 'colors' mapping")
    return colors


def _resolve_color(colors: dict[str, object], key: str) -> tuple[int, int, int]:
    if key not in colors:
        raise KeyError(f"color key not found in theme.yml: {key}")
    return _parse_color(colors[key])


def _pick_font(font_size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in ("DejaVuSans-Bold.ttf", "Arial.ttf"):
        try:
            return ImageFont.truetype(candidate, font_size)
        except OSError:
            continue
    return ImageFont.load_default()


def _draw_logo(
    output_path: Path,
    text: str,
    width: int,
    height: int,
    text_rgb: tuple[int, int, int],
    background_rgb: tuple[int, int, int],
    font_size: int,
    border_width: int,
) -> None:
    image = Image.new("RGB", (width, height), background_rgb)
    draw = ImageDraw.Draw(image)
    font = _pick_font(font_size)

    if border_width > 0:
        for i in range(border_width):
            draw.rectangle(
                (i, i, width - 1 - i, height - 1 - i),
                outline=text_rgb,
                width=1,
            )

    # textbbox gives reliable centering for both bitmap and truetype fonts.
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    text_width = right - left
    text_height = bottom - top

    x = (width - text_width) // 2
    y = (height - text_height) // 2
    draw.text((x, y), text, fill=text_rgb, font=font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, "PNG")


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    default_themes_dir = script_dir.parent / "THEMES"

    parser = argparse.ArgumentParser(
        description="Generate a simple logo.png from theme color keys."
    )
    parser.add_argument(
        "--themes-dir",
        type=Path,
        default=default_themes_dir,
        metavar="DIR",
        help=f"path to THEMES directory (default: {default_themes_dir})",
    )
    parser.add_argument(
        "--theme",
        required=True,
        metavar="NAME",
        help="theme folder name under THEMES (e.g. DZARODarkPurple)",
    )
    parser.add_argument(
        "--text",
        default=None,
        help="logo text (default: summary.name from theme.yml, then folder name)",
    )
    parser.add_argument(
        "--text-color",
        default="FOCUS",
        metavar="KEY",
        help="theme color key for text (default: FOCUS)",
    )
    parser.add_argument(
        "--background-color",
        default="SECONDARY3",
        metavar="KEY",
        help="theme color key for background (default: SECONDARY3)",
    )
    parser.add_argument("--width", type=int, default=200, help="image width in pixels")
    parser.add_argument("--height", type=int, default=100, help="image height in pixels")
    parser.add_argument("--font-size", type=int, default=18, help="font size in points")
    parser.add_argument(
        "--border-width",
        type=int,
        default=2,
        help="border thickness in pixels; 0 disables border (default: 2)",
    )
    args = parser.parse_args()

    if args.width <= 0 or args.height <= 0:
        print("width and height must be > 0", file=sys.stderr)
        sys.exit(2)
    if args.font_size <= 0:
        print("font-size must be > 0", file=sys.stderr)
        sys.exit(2)
    if args.border_width < 0:
        print("border-width must be >= 0", file=sys.stderr)
        sys.exit(2)

    theme_dir = args.themes_dir / args.theme
    theme_yml = theme_dir / "theme.yml"
    output_path = theme_dir / "logo.png"

    if not theme_yml.is_file():
        print(f"theme.yml not found: {theme_yml}", file=sys.stderr)
        sys.exit(2)

    try:
        with theme_yml.open(encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        if isinstance(data, dict) and isinstance(data.get("summary"), dict):
            default_text = str(data["summary"].get("name") or "").strip() or args.theme
        else:
            default_text = args.theme

        text = args.text if args.text is not None else default_text
        colors = _load_theme_colors(theme_yml)
        text_rgb = _resolve_color(colors, args.text_color)
        background_rgb = _resolve_color(colors, args.background_color)

        _draw_logo(
            output_path=output_path,
            text=text,
            width=args.width,
            height=args.height,
            text_rgb=text_rgb,
            background_rgb=background_rgb,
            font_size=args.font_size,
            border_width=args.border_width,
        )
    except (ValueError, KeyError, yaml.YAMLError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(
        f"Generated {output_path} using text={args.text_color} and background={args.background_color}"
    )


if __name__ == "__main__":
    main()
