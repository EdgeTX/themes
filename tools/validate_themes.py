#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml", "rich"]
# ///
"""Validate EdgeTX theme directories against the theme specification."""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required. Run: uv run tools/validate_themes.py", file=sys.stderr)
    sys.exit(1)

from rich.console import Console
from rich.text import Text

console = Console(highlight=False)

REQUIRED_COLOR_KEYS = [
    "PRIMARY1", "PRIMARY2", "PRIMARY3",
    "SECONDARY1", "SECONDARY2", "SECONDARY3",
    "FOCUS", "EDIT", "ACTIVE", "WARNING", "DISABLED",
]
OPTIONAL_COLOR_KEYS = ["QM_BG", "QM_FG"]
ALL_COLOR_KEYS = set(REQUIRED_COLOR_KEYS + OPTIONAL_COLOR_KEYS)

REQUIRED_IMAGES = ["logo.png", "screenshot1.png", "screenshot2.png", "screenshot3.png"]
BACKGROUND_RESOLUTIONS = [
    "background_320x240.png",
    "background_320x480.png",
    "background_480x272.png",
    "background_480x320.png",
    "background_800x480.png",
]
KNOWN_FILES = set(
    ["theme.yml", "readme.txt"]
    + REQUIRED_IMAGES
    + BACKGROUND_RESOLUTIONS
)


def _is_extra_screenshot(filename: str) -> bool:
    """Return True if filename is a screenshot beyond the required 3 (e.g., screenshot4.png)."""
    return filename.lower().startswith("screenshot") and filename.lower().endswith(".png")

_RGB_RE = re.compile(
    r"^RGB\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$", re.IGNORECASE
)
_RGB_HEX_RE = re.compile(
    r"^RGB\(\s*(0x[0-9A-Fa-f]{1,2})\s*,\s*(0x[0-9A-Fa-f]{1,2})\s*,\s*(0x[0-9A-Fa-f]{1,2})\s*\)$",
    re.IGNORECASE,
)


def _is_valid_color(value) -> bool:
    """Return True if value is a recognisable EdgeTX color."""
    if isinstance(value, int):
        return 0 <= value <= 0xFFFFFF
    v = str(value).strip()
    if v.startswith(("0x", "0X")):
        hex_part = v[2:]
        return len(hex_part) == 6 and all(c in "0123456789abcdefABCDEF" for c in hex_part)
    m = _RGB_RE.match(v) or _RGB_HEX_RE.match(v)
    if m:
        parts = [int(x, 0) for x in m.groups()]
        return all(0 <= p <= 255 for p in parts)
    return False


def _find_icase(directory: Path, name: str) -> bool:
    """Return True if a file matching name (case-insensitively) exists in directory."""
    target = name.lower()
    return any(f.name.lower() == target for f in directory.iterdir())


@dataclass
class Result:
    name: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_theme(theme_dir: Path) -> Result:
    result = Result(name=theme_dir.name)

    # --- theme.yml ---
    yml_path = theme_dir / "theme.yml"
    if not yml_path.exists():
        result.errors.append("theme.yml is missing")
        return result

    try:
        with yml_path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        result.errors.append(f"theme.yml parse error: {e}")
        return result

    if not isinstance(data, dict):
        result.errors.append("theme.yml: top-level value must be a YAML mapping")
        return result

    # --- summary section ---
    summary = data.get("summary")
    if not isinstance(summary, dict):
        result.errors.append("theme.yml: missing 'summary' section")
    else:
        for key in ("name", "author", "info"):
            if not summary.get(key):
                result.errors.append(f"theme.yml summary: missing or empty '{key}'")

    # --- colors section ---
    colors = data.get("colors")
    if not isinstance(colors, dict):
        result.errors.append("theme.yml: missing 'colors' section")
    else:
        for key in REQUIRED_COLOR_KEYS:
            if key not in colors:
                result.errors.append(f"theme.yml colors: missing required key '{key}'")
            elif not _is_valid_color(colors[key]):
                result.errors.append(
                    f"theme.yml colors: invalid value for '{key}': {colors[key]!r}"
                    " (expected 0xRRGGBB hex or RGB(r,g,b))"
                )

        for key in OPTIONAL_COLOR_KEYS:
            if key not in colors:
                result.warnings.append(
                    f"theme.yml colors: optional key '{key}' not set (added in EdgeTX 2.12)"
                )
            elif not _is_valid_color(colors[key]):
                result.errors.append(
                    f"theme.yml colors: invalid value for '{key}': {colors[key]!r}"
                )

        unknown_keys = set(colors.keys()) - ALL_COLOR_KEYS
        for key in sorted(unknown_keys):
            result.warnings.append(f"theme.yml colors: unknown key '{key}' (possible typo)")

    # --- required images ---
    for img in REQUIRED_IMAGES:
        if not _find_icase(theme_dir, img):
            result.errors.append(f"missing required file: {img}")

    # --- background images ---
    present_bgs = [bg for bg in BACKGROUND_RESOLUTIONS if _find_icase(theme_dir, bg)]
    if not present_bgs:
        result.warnings.append("no background images present (none of the 5 resolution variants)")
    elif len(present_bgs) < len(BACKGROUND_RESOLUTIONS):
        missing_bgs = [bg for bg in BACKGROUND_RESOLUTIONS if bg not in present_bgs]
        result.warnings.append(
            f"only {len(present_bgs)}/{len(BACKGROUND_RESOLUTIONS)} background resolutions present"
            f" (missing: {', '.join(missing_bgs)})"
        )

    # --- unknown files ---
    actual_files = {f.name.lower() for f in theme_dir.iterdir() if f.is_file()}
    known_lower = {k.lower() for k in KNOWN_FILES}
    unknown = sorted(actual_files - known_lower)
    for uf in unknown:
        if not _is_extra_screenshot(uf):
            result.warnings.append(f"unexpected file: {uf}")

    return result


def validate_all(themes_dir: Path, single: str | None = None) -> list[Result]:
    if not themes_dir.is_dir():
        console.print(f"[bold red]Error:[/] themes directory not found: {themes_dir}")
        sys.exit(2)

    if single:
        theme_path = themes_dir / single
        if not theme_path.is_dir():
            console.print(f"[bold red]Error:[/] theme directory not found: {theme_path}")
            sys.exit(2)
        dirs = [theme_path]
    else:
        dirs = sorted(d for d in themes_dir.iterdir() if d.is_dir())

    return [validate_theme(d) for d in dirs]


def print_results(results: list[Result], strict: bool) -> int:
    failed = 0
    warned = 0

    for r in results:
        errors_in_strict = r.errors + (r.warnings if strict else [])
        if errors_in_strict:
            line = Text()
            line.append("✗ ", style="bold red")
            line.append(r.name, style="bold")
            failed += 1
        else:
            line = Text()
            line.append("✓ ", style="bold green")
            line.append(r.name, style="bold")
        console.print(line)

        for msg in r.errors:
            console.print(f"    [bold red]ERROR:[/] {msg}")
        for msg in r.warnings:
            if strict:
                console.print(f"    [bold red]ERROR:[/] {msg}")
            else:
                console.print(f"    [bold yellow]WARN :[/] {msg}")
                warned += 1

    total = len(results)
    passed = total - failed
    console.print()

    summary = Text()
    summary.append(f"{total} theme{'s' if total != 1 else ''} validated")
    summary.append(", ")
    summary.append(f"{passed} passed", style="green" if passed else "")
    summary.append(", ")
    summary.append(f"{failed} failed", style="bold red" if failed else "")
    if not strict:
        summary.append(", ")
        summary.append(
            f"{warned} warning{'s' if warned != 1 else ''}",
            style="yellow" if warned else "",
        )
    console.print(summary)

    return 1 if failed else 0


def main() -> None:
    script_dir = Path(__file__).parent
    default_themes = script_dir.parent / "THEMES"

    parser = argparse.ArgumentParser(
        description="Validate EdgeTX theme directories against the theme specification."
    )
    parser.add_argument(
        "--themes-dir",
        type=Path,
        default=default_themes,
        metavar="DIR",
        help=f"path to the THEMES directory (default: {default_themes})",
    )
    parser.add_argument(
        "--theme",
        metavar="NAME",
        help="validate a single theme by folder name instead of all themes",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat warnings as errors (non-zero exit if any warnings)",
    )
    args = parser.parse_args()

    results = validate_all(args.themes_dir, single=args.theme)
    sys.exit(print_results(results, strict=args.strict))


if __name__ == "__main__":
    main()
