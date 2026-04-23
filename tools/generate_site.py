#!/usr/bin/env python3
"""Generate a static HTML theme gallery for EdgeTX themes."""

import argparse
import html
import json
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

COLOR_KEYS = [
    "PRIMARY1", "PRIMARY2", "PRIMARY3",
    "SECONDARY1", "SECONDARY2", "SECONDARY3",
    "FOCUS", "EDIT", "ACTIVE", "WARNING", "DISABLED",
]

DOWNLOAD_ALL_URL = (
    "https://github.com/EdgeTX/themes/releases/latest/download/edgetx-themes.zip"
)
RELEASE_BASE_URL = (
    "https://github.com/EdgeTX/themes/releases/download/individual-themes"
)


def hex_to_css(value) -> str:
    """Convert YAML-parsed 0xRRGGBB (int or str) to #rrggbb."""
    if isinstance(value, int):
        return "#{:06x}".format(value)
    v = str(value).strip()
    if v.startswith(("0x", "0X")):
        return "#" + v[2:].zfill(6)
    return v


def find_file_icase(directory: Path, name: str) -> Path | None:
    """Return the actual Path of a file matching name case-insensitively, or None."""
    target = name.lower()
    for f in directory.iterdir():
        if f.name.lower() == target:
            return f
    return None


def load_theme(theme_dir: Path) -> dict | None:
    yml_path = theme_dir / "theme.yml"
    if not yml_path.exists():
        return None
    with yml_path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    summary = data.get("summary", {})
    colors_raw = data.get("colors", {})
    colors = {k: hex_to_css(v) for k, v in colors_raw.items()}

    logo_path = find_file_icase(theme_dir, "logo.png")

    screenshots = []
    for i in range(1, 5):
        ss_path = find_file_icase(theme_dir, f"screenshot{i}.png")
        if ss_path:
            screenshots.append(ss_path.name)

    hero = logo_path.name if logo_path else (screenshots[0] if screenshots else None)

    return {
        "dir_name": theme_dir.name,
        "name": summary.get("name", theme_dir.name),
        "author": summary.get("author", ""),
        "info": summary.get("info", ""),
        "colors": colors,
        "screenshots": screenshots,
        "hero": hero,
    }


def copy_images(theme: dict, theme_dir: Path, out_themes_dir: Path) -> None:
    dest = out_themes_dir / theme["dir_name"]
    dest.mkdir(parents=True, exist_ok=True)
    if theme["hero"]:
        shutil.copy2(theme_dir / theme["hero"], dest / theme["hero"])
    for ss in theme["screenshots"]:
        shutil.copy2(theme_dir / ss, dest / ss)


def render_card(theme: dict) -> str:
    e = html.escape
    dir_name = e(theme["dir_name"])
    name = e(theme["name"])
    author = e(theme["author"])
    info = e(theme["info"])

    # Build ordered image list: hero first, then remaining screenshots
    carousel_images = []
    if theme["hero"]:
        carousel_images.append(theme["hero"])
    for ss in theme["screenshots"]:
        if ss != theme["hero"]:
            carousel_images.append(ss)

    if carousel_images:
        imgs = "".join(
            f'<img class="carousel-img{"  active" if i == 0 else ""}" '
            f'src="themes/{dir_name}/{e(img)}" alt="{name}" loading="lazy">\n'
            for i, img in enumerate(carousel_images)
        )
        dots = (
            '<div class="carousel-dots">'
            + "".join(
                f'<span class="dot{"  active" if i == 0 else ""}"></span>'
                for i in range(len(carousel_images))
            )
            + "</div>"
        ) if len(carousel_images) > 1 else ""
        carousel_html = f'<div class="carousel" data-count="{len(carousel_images)}">{imgs}{dots}</div>'
    else:
        carousel_html = '<div class="carousel carousel-placeholder"></div>'

    swatches = "".join(
        f'<div class="swatch" style="background:{theme["colors"].get(key, "#888")}" '
        f'title="{e(key)}: {e(theme["colors"].get(key, ""))}"></div>'
        for key in COLOR_KEYS
    )

    screenshots_json = json.dumps(
        [f"themes/{dir_name}/{ss}" for ss in theme["screenshots"]]
    )
    ss_btn = (
        f'<button class="ss-btn" onclick=\'openLightbox({screenshots_json},"{name}")\''
        f' {"" if theme["screenshots"] else "disabled"}'
        f'>Screenshots ({len(theme["screenshots"])})</button>'
    )

    return f"""
    <div class="card" data-name="{name.lower()}" data-author="{author.lower()}">
      {carousel_html}
      <div class="card-body">
        <h2 class="card-name">{name}</h2>
        <p class="card-author">{author}</p>
        {"" if not info else f'<p class="card-info">{info}</p>'}
        <div class="swatches">{swatches}</div>
        <div class="card-actions">{ss_btn}<a class="dl-theme-btn" href="{RELEASE_BASE_URL}/{theme['dir_name']}.zip">Download</a></div>
      </div>
    </div>"""


def render_page(themes: list[dict]) -> str:
    cards = "\n".join(render_card(t) for t in themes)
    count = len(themes)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>EdgeTX Theme Gallery</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :root {{
      --bg: #0d1117;
      --surface: #161b22;
      --border: #30363d;
      --text: #e6edf3;
      --text-muted: #8b949e;
      --accent: #2ea043;
      --accent-hover: #3fb950;
      --blue: #1f6feb;
      --blue-hover: #388bfd;
      --radius: 8px;
      --card-hover-border: #58a6ff;
      --carousel-bg: #0d1117;
      --carousel-placeholder-bg: #1c2128;
      --btn-hover-bg: #21262d;
      --dl-theme-color: #3fb950;
      --dl-theme-border: #2ea04366;
      --swatch-border: rgba(255,255,255,0.1);
      --dot: rgba(255,255,255,0.35);
      --dot-hover: rgba(255,255,255,0.65);
      --dot-active: rgba(255,255,255,0.9);
      --lb-fg: #e6edf3;
      --lb-fg-muted: #8b949e;
      --lb-btn-bg: #21262d;
      --lb-btn-border: #30363d;
    }}
    :root[data-theme="light"] {{
      --bg: #ffffff;
      --surface: #f6f8fa;
      --border: #d0d7de;
      --text: #1f2328;
      --text-muted: #656d76;
      --accent: #1a7f37;
      --accent-hover: #2da44e;
      --blue: #0969da;
      --blue-hover: #0550ae;
      --card-hover-border: #0969da;
      --carousel-bg: #eaeef2;
      --carousel-placeholder-bg: #d0d7de;
      --btn-hover-bg: #eaeef2;
      --dl-theme-color: #1a7f37;
      --dl-theme-border: #2da44e66;
      --swatch-border: rgba(0,0,0,0.1);
      --dot: rgba(0,0,0,0.35);
      --dot-hover: rgba(0,0,0,0.65);
      --dot-active: rgba(0,0,0,0.9);
    }}
    @media (prefers-color-scheme: light) {{
      :root:not([data-theme="dark"]) {{
        --bg: #ffffff;
        --surface: #f6f8fa;
        --border: #d0d7de;
        --text: #1f2328;
        --text-muted: #656d76;
        --accent: #1a7f37;
        --accent-hover: #2da44e;
        --blue: #0969da;
        --blue-hover: #0550ae;
        --card-hover-border: #0969da;
        --carousel-bg: #eaeef2;
        --carousel-placeholder-bg: #d0d7de;
        --btn-hover-bg: #eaeef2;
        --dl-theme-color: #1a7f37;
        --dl-theme-border: #2da44e66;
        --swatch-border: rgba(0,0,0,0.1);
        --dot: rgba(0,0,0,0.35);
        --dot-hover: rgba(0,0,0,0.65);
        --dot-active: rgba(0,0,0,0.9);
      }}
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
    }}

    /* Header */
    .site-header {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      padding: 12px 24px;
      display: flex;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
    }}
    .site-title {{
      font-size: 1.1rem;
      font-weight: 600;
      white-space: nowrap;
    }}
    .site-title span {{
      color: var(--text-muted);
      font-weight: 400;
      font-size: 0.9rem;
      margin-left: 8px;
    }}
    .search {{
      flex: 1;
      min-width: 180px;
      max-width: 360px;
      padding: 7px 12px;
      border-radius: var(--radius);
      border: 1px solid var(--border);
      background: var(--bg);
      color: var(--text);
      font-size: 0.9rem;
    }}
    .search::placeholder {{ color: var(--text-muted); }}
    .search:focus {{ outline: none; border-color: var(--accent); }}
    .gh-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 16px;
      border-radius: var(--radius);
      background: var(--blue);
      color: #fff;
      font-weight: 600;
      font-size: 0.875rem;
      text-decoration: none;
      white-space: nowrap;
      transition: background 0.15s;
    }}
    .gh-btn:hover {{ background: var(--blue-hover); }}
    .repo-btn {{ margin-left: auto; background: #24292f; }}
    .repo-btn:hover {{ background: #32383f; }}
    .dl-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      margin-left: 0;
      padding: 7px 16px;
      border-radius: var(--radius);
      background: var(--accent);
      color: #fff;
      font-weight: 600;
      font-size: 0.875rem;
      text-decoration: none;
      white-space: nowrap;
      transition: background 0.15s;
    }}
    .dl-btn:hover {{ background: var(--accent-hover); }}
    .anim-toggle {{
      padding: 7px 12px;
      border-radius: var(--radius);
      border: 1px solid var(--border);
      background: transparent;
      color: var(--text-muted);
      font-size: 0.8rem;
      cursor: pointer;
      white-space: nowrap;
      transition: color 0.15s, border-color 0.15s;
    }}
    .anim-toggle:hover {{ color: var(--text); border-color: var(--card-hover-border); }}
    .anim-toggle.paused {{ color: var(--text-muted); }}

    /* Grid */
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 20px;
      padding: 24px;
      max-width: 1600px;
      margin: 0 auto;
    }}
    .no-results {{
      grid-column: 1 / -1;
      text-align: center;
      color: var(--text-muted);
      padding: 60px 0;
      font-size: 1rem;
    }}

    /* Card */
    .card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: border-color 0.15s;
    }}
    .card:hover {{ border-color: var(--card-hover-border); }}

    /* Carousel */
    .carousel {{
      position: relative;
      width: 100%;
      aspect-ratio: 4/3;
      background: var(--carousel-bg);
      overflow: hidden;
    }}
    .carousel-placeholder {{ background: var(--carousel-placeholder-bg); }}
    .carousel-img {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: contain;
      opacity: 0;
      transition: opacity 0.6s ease;
    }}
    .carousel-img.active {{ opacity: 1; }}
    body.animations-paused .carousel-img {{ transition: none; }}
    .carousel-dots {{
      position: absolute;
      bottom: 6px;
      left: 0;
      right: 0;
      display: flex;
      justify-content: center;
      gap: 5px;
    }}
    .dot {{
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--dot);
      transition: background 0.3s, transform 0.15s;
      cursor: pointer;
    }}
    .dot:hover {{ background: var(--dot-hover); transform: scale(1.4); }}
    .dot.active {{ background: var(--dot-active); transform: scale(1.3); }}
    .card-body {{
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      flex: 1;
    }}
    .card-name {{
      font-size: 1rem;
      font-weight: 600;
      line-height: 1.3;
    }}
    .card-author {{
      font-size: 0.8rem;
      color: var(--text-muted);
    }}
    .card-info {{
      font-size: 0.8rem;
      color: var(--text-muted);
      font-style: italic;
    }}

    /* Swatches */
    .swatches {{
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      margin-top: 2px;
    }}
    .swatch {{
      width: 20px;
      height: 20px;
      border-radius: 3px;
      border: 1px solid var(--swatch-border);
      cursor: default;
      flex-shrink: 0;
    }}

    .card-actions {{
      margin-top: auto;
      padding-top: 4px;
      display: flex;
      gap: 6px;
    }}
    .ss-btn, .dl-theme-btn {{
      flex: 1;
      padding: 7px;
      border-radius: var(--radius);
      border: 1px solid var(--border);
      background: transparent;
      color: var(--text);
      font-size: 0.8rem;
      cursor: pointer;
      text-align: center;
      text-decoration: none;
      transition: background 0.15s, border-color 0.15s;
    }}
    .ss-btn:hover:not([disabled]), .dl-theme-btn:hover {{ background: var(--btn-hover-bg); border-color: var(--card-hover-border); }}
    .ss-btn[disabled] {{ opacity: 0.4; cursor: default; }}
    .dl-theme-btn {{ border-color: var(--dl-theme-border); color: var(--dl-theme-color); }}
    .dl-theme-btn:hover {{ border-color: var(--accent-hover) !important; }}

    /* Lightbox */
    .lb-overlay {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.85);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      flex-direction: column;
    }}
    .lb-overlay.active {{ display: flex; }}
    .lb-header {{
      width: 100%;
      max-width: 900px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 12px;
    }}
    .lb-title {{ font-size: 0.95rem; font-weight: 600; color: var(--lb-fg); }}
    .lb-close {{
      background: none;
      border: none;
      color: var(--lb-fg);
      font-size: 1.5rem;
      cursor: pointer;
      line-height: 1;
      padding: 4px 8px;
    }}
    .lb-img-wrap {{
      width: 100%;
      max-width: 900px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 8px;
    }}
    .lb-img {{
      max-width: 100%;
      max-height: 70vh;
      border-radius: var(--radius);
      display: block;
    }}
    .lb-nav {{
      display: flex;
      gap: 12px;
      margin-top: 12px;
      align-items: center;
    }}
    .lb-nav button {{
      background: var(--lb-btn-bg);
      border: 1px solid var(--lb-btn-border);
      color: var(--lb-fg);
      padding: 6px 16px;
      border-radius: var(--radius);
      cursor: pointer;
      font-size: 0.85rem;
    }}
    .lb-nav button:disabled {{ opacity: 0.3; cursor: default; }}
    .lb-counter {{ color: var(--lb-fg-muted); font-size: 0.85rem; }}
  </style>
</head>
<body>
  <header class="site-header">
    <div class="site-title">EdgeTX Theme Gallery<span id="count-label">{count} themes</span></div>
    <input class="search" type="search" id="search" placeholder="Search themes…" aria-label="Search themes">
    <button class="anim-toggle" id="anim-toggle" title="Toggle carousel animations">Animations: On</button>
    <button class="anim-toggle" id="reset-btn" title="Reset all carousels to first image">Reset to Logos</button>
    <button class="anim-toggle" id="theme-toggle" title="Toggle light/dark mode">Theme: Dark</button>
    <a class="gh-btn repo-btn" href="https://github.com/EdgeTX/themes" target="_blank" rel="noopener"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" width="16" fill="currentColor"><path d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.26-1.23-.55-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"/></svg>GitHub Repo</a>
    <a class="gh-btn" href="https://github.com/EdgeTX/themes/blob/main/CONTRIBUTING.md#submitting-your-theme" target="_blank" rel="noopener"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" width="16" fill="currentColor"><path d="M2.75 14A1.75 1.75 0 0 1 1 12.25v-2.5a.75.75 0 0 1 1.5 0v2.5c0 .138.112.25.25.25h10.5a.25.25 0 0 0 .25-.25v-2.5a.75.75 0 0 1 1.5 0v2.5A1.75 1.75 0 0 1 13.25 14Z"/><path d="M11.78 5.22a.749.749 0 0 1-1.06 1.06L8.75 4.31v5.44a.75.75 0 0 1-1.5 0V4.31L5.28 6.28a.749.749 0 1 1-1.06-1.06l3.25-3.25a.749.749 0 0 1 1.06 0l3.25 3.25Z"/></svg>Submit Theme</a>
    <a class="dl-btn" href="{DOWNLOAD_ALL_URL}" download><svg aria-hidden="true" height="16" viewBox="0 0 16 16" width="16" fill="currentColor"><path d="M2.75 14A1.75 1.75 0 0 1 1 12.25v-2.5a.75.75 0 0 1 1.5 0v2.5c0 .138.112.25.25.25h10.5a.25.25 0 0 0 .25-.25v-2.5a.75.75 0 0 1 1.5 0v2.5A1.75 1.75 0 0 1 13.25 14Z"/><path d="M7.25 7.689V2a.75.75 0 0 1 1.5 0v5.689l1.97-1.97a.749.749 0 1 1 1.06 1.06l-3.25 3.25a.749.749 0 0 1-1.06 0L4.22 6.779a.749.749 0 1 1 1.06-1.06l1.97 1.97Z"/></svg>Download All Themes</a>
  </header>

  <main class="grid" id="grid">
    {cards}
    <div class="no-results" id="no-results" style="display:none">No themes match your search.</div>
  </main>

  <!-- Lightbox -->
  <div class="lb-overlay" id="lb" role="dialog" aria-modal="true">
    <div class="lb-header">
      <span class="lb-title" id="lb-title"></span>
      <button class="lb-close" onclick="closeLightbox()" aria-label="Close">&times;</button>
    </div>
    <div class="lb-img-wrap">
      <img class="lb-img" id="lb-img" src="" alt="">
    </div>
    <nav class="lb-nav">
      <button id="lb-prev" onclick="lbStep(-1)">&#8592; Prev</button>
      <span class="lb-counter" id="lb-counter"></span>
      <button id="lb-next" onclick="lbStep(1)">Next &#8594;</button>
    </nav>
  </div>

  <script>
    // Search
    const searchEl = document.getElementById('search');
    const cards = Array.from(document.querySelectorAll('.card'));
    const noResults = document.getElementById('no-results');
    const countLabel = document.getElementById('count-label');
    const total = cards.length;

    searchEl.addEventListener('input', () => {{
      const q = searchEl.value.toLowerCase().trim();
      let visible = 0;
      cards.forEach(c => {{
        const match = !q || c.dataset.name.includes(q) || c.dataset.author.includes(q);
        c.style.display = match ? '' : 'none';
        if (match) visible++;
      }});
      noResults.style.display = visible === 0 ? '' : 'none';
      countLabel.textContent = q ? `${{visible}} of ${{total}} themes` : `${{total}} themes`;
    }});

    // Carousels
    const INTERVAL = 3500;
    let globalTimers = []; // cleared by stopCarousels / resetCarousels
    const carouselEls = Array.from(document.querySelectorAll('.carousel[data-count]'));

    // Animation toggle — declared early so initCarousels() can read animPaused
    const animBtn = document.getElementById('anim-toggle');
    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let animPaused = localStorage.getItem('anim-paused') === 'true' || prefersReduced;

    function advanceEl(el) {{
      const imgs = el.querySelectorAll('.carousel-img');
      const dots = el.querySelectorAll('.dot');
      const s = el._cs;
      const next = (s.idx + 1) % imgs.length;
      imgs[s.idx].classList.remove('active');
      imgs[next].classList.add('active');
      if (dots.length) {{
        dots[s.idx].classList.remove('active');
        dots[next].classList.add('active');
      }}
      s.idx = next;
    }}

    function startOne(el, delay) {{
      const t = setTimeout(() => {{
        const iv = setInterval(() => advanceEl(el), INTERVAL);
        el._cs.interval = iv;
        globalTimers.push(iv);
      }}, delay);
      globalTimers.push(t);
    }}

    function startCarousels() {{
      carouselEls.forEach((el, i) => {{
        if (el.querySelectorAll('.carousel-img').length < 2) return;
        startOne(el, i * (INTERVAL / Math.max(carouselEls.length, 1)));
      }});
    }}

    function stopCarousels() {{
      globalTimers.forEach(clearTimeout);
      globalTimers = [];
      carouselEls.forEach(el => {{ if (el._cs) el._cs.interval = null; }});
    }}

    // Jump a carousel directly to a target frame (used by dot clicks)
    function jumpTo(el, targetIdx) {{
      const imgs = el.querySelectorAll('.carousel-img');
      const dots = el.querySelectorAll('.dot');
      const s = el._cs;
      if (s.interval) {{ clearInterval(s.interval); s.interval = null; }}
      imgs[s.idx].classList.remove('active');
      imgs[targetIdx].classList.add('active');
      if (dots.length) {{
        dots[s.idx].classList.remove('active');
        dots[targetIdx].classList.add('active');
      }}
      s.idx = targetIdx;
      if (!animPaused) {{
        const iv = setInterval(() => advanceEl(el), INTERVAL);
        s.interval = iv;
        globalTimers.push(iv);
      }}
    }}

    // Initialise per-carousel state and wire up dot click handlers
    carouselEls.forEach(el => {{
      const imgs = el.querySelectorAll('.carousel-img');
      if (imgs.length < 2) return;
      el._cs = {{ idx: 0, interval: null }};
      el.querySelectorAll('.dot').forEach((dot, dotIdx) => {{
        dot.addEventListener('click', () => jumpTo(el, dotIdx));
      }});
    }});

    function applyAnimState() {{
      document.body.classList.toggle('animations-paused', animPaused);
      animBtn.textContent = animPaused ? 'Animations: Off' : 'Animations: On';
      animBtn.classList.toggle('paused', animPaused);
      if (animPaused) stopCarousels(); else startCarousels();
    }}

    function resetCarousels() {{
      stopCarousels();
      carouselEls.forEach(el => {{
        if (!el._cs) return;
        el.querySelectorAll('.carousel-img').forEach((img, i) => img.classList.toggle('active', i === 0));
        el.querySelectorAll('.dot').forEach((dot, i) => dot.classList.toggle('active', i === 0));
        el._cs.idx = 0;
      }});
      if (!animPaused) startCarousels();
    }}

    document.getElementById('reset-btn').addEventListener('click', resetCarousels);

    animBtn.addEventListener('click', () => {{
      animPaused = !animPaused;
      localStorage.setItem('anim-paused', animPaused);
      applyAnimState();
    }});

    applyAnimState();

    // Theme toggle
    const themeBtn = document.getElementById('theme-toggle');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const savedTheme = localStorage.getItem('theme');
    let isDark = savedTheme ? savedTheme === 'dark' : prefersDark;

    function applyTheme(dark) {{
      document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
      themeBtn.textContent = dark ? 'Theme: Dark' : 'Theme: Light';
      isDark = dark;
      localStorage.setItem('theme', dark ? 'dark' : 'light');
    }}

    applyTheme(isDark);
    themeBtn.addEventListener('click', () => applyTheme(!isDark));

    // Lightbox
    let lbImages = [], lbIdx = 0;

    function openLightbox(images, name) {{
      lbImages = images;
      lbIdx = 0;
      document.getElementById('lb-title').textContent = name;
      renderLb();
      document.getElementById('lb').classList.add('active');
      document.addEventListener('keydown', lbKey);
    }}

    function closeLightbox() {{
      document.getElementById('lb').classList.remove('active');
      document.removeEventListener('keydown', lbKey);
    }}

    function renderLb() {{
      document.getElementById('lb-img').src = lbImages[lbIdx];
      document.getElementById('lb-img').alt = `Screenshot ${{lbIdx + 1}}`;
      document.getElementById('lb-counter').textContent = `${{lbIdx + 1}} / ${{lbImages.length}}`;
      document.getElementById('lb-prev').disabled = lbIdx === 0;
      document.getElementById('lb-next').disabled = lbIdx === lbImages.length - 1;
    }}

    function lbStep(dir) {{
      lbIdx = Math.max(0, Math.min(lbImages.length - 1, lbIdx + dir));
      renderLb();
    }}

    function lbKey(e) {{
      if (e.key === 'ArrowLeft') lbStep(-1);
      else if (e.key === 'ArrowRight') lbStep(1);
      else if (e.key === 'Escape') closeLightbox();
    }}

    document.getElementById('lb').addEventListener('click', e => {{
      if (e.target === e.currentTarget) closeLightbox();
    }});
  </script>
</body>
</html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate EdgeTX theme gallery site")
    parser.add_argument("--themes-dir", default="THEMES", help="Path to THEMES directory")
    parser.add_argument("--output-dir", default="site", help="Output directory")
    args = parser.parse_args()

    themes_dir = Path(args.themes_dir)
    output_dir = Path(args.output_dir)
    out_themes = output_dir / "themes"

    if not themes_dir.is_dir():
        print(f"Error: themes directory not found: {themes_dir}", file=sys.stderr)
        sys.exit(1)

    themes = []
    for d in sorted(themes_dir.iterdir()):
        if not d.is_dir():
            continue
        theme = load_theme(d)
        if theme is None:
            continue
        themes.append(theme)
        copy_images(theme, d, out_themes)

    themes.sort(key=lambda t: t["name"].lower())

    output_dir.mkdir(parents=True, exist_ok=True)
    index_path = output_dir / "index.html"
    index_path.write_text(render_page(themes), encoding="utf-8")

    print(f"Generated {len(themes)} theme cards → {index_path}")


if __name__ == "__main__":
    main()
