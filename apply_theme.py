#!/usr/bin/env python3
"""
apply_theme.py — One-shot CSS theming refactor for the MTech portal.

What it does:
  1. Creates site/theme.css with canonical design tokens.
  2. Walks every HTML file in site/ and semester2/*/lessons/.
  3. Injects <link rel="stylesheet" href="...theme.css"> into <head>.
  4. Strips inline :root{} and [data-theme="dark"]{} variable blocks.
  5. Group E (exam guides): link-only, keeps :root intact.
  6. Group D (SEML lectures): keeps layout-only residual :root tokens.
  7. Group C (DRL lessons): adds dark-mode toggle button + script.
  8. Normalises localStorage key 'aci-theme' → 'theme' everywhere.
  9. Mirrors every semester2 edit to site/ (ADR-003).
"""

import os, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).parent
SITE = ROOT / "site"
SEM2 = ROOT / "semester2"

# ── theme.css content ──────────────────────────────────────────────────────
THEME_CSS = """\
/* ============================================================
   theme.css — Canonical design tokens for the MTech portal
   ACI light theme is the reference.  Change colours here only.
   ============================================================ */

:root {
  /* Backgrounds */
  --bg:         #fafaf8;
  --surface:    #ffffff;
  --sidebar-bg: #f0f0ed;
  --code-bg:    #f4f4f0;
  --card-bg:    #ffffff;
  --card-border:#dddddd;

  /* Text */
  --text:       #1a1a1a;
  --text-muted: #555555;

  /* Brand */
  --navy:   #1a2744;
  --gold:   #e8a020;
  --green:  #27ae60;
  --accent: #c0392b;

  /* Structural */
  --border:      #d4d4d4;
  --card-shadow: 0 2px 6px rgba(0,0,0,0.06);
  --card-hover:  0 4px 12px rgba(0,0,0,0.10);

  /* Tags */
  --tag-bg:   #edf1fb;
  --tag-text: #1a2744;

  /* Semantic tints (callout / alert boxes) */
  --tint-success: #e8f5e9;
  --tint-warning: #fff3cd;
  --tint-danger:  #fdecea;
  --tint-info:    #e8f0fe;
  --tint-formula: #fff8e1;
  --tint-try:     #f1f8e9;

  /* Dialect aliases — keep older variable names working */
  --muted:  var(--text-muted);   /* DRL/NLP lessons */
  --ink:    var(--text);         /* SEML lectures    */
  --panel:  var(--card-bg);
  --panel2: var(--code-bg);
  --line:   var(--card-border);
  --bg2:    var(--sidebar-bg);
  --cyan:   var(--gold);
  --violet: var(--accent);
  --amber:  var(--gold);
}

[data-theme="dark"] {
  --bg:         #0f1419;
  --surface:    #1a2332;
  --sidebar-bg: #16162b;
  --code-bg:    #2a2a4a;
  --card-bg:    #242442;
  --card-border:#3a3a5c;

  --text:       #e8e6e3;
  --text-muted: #a0a0a0;

  --navy:   #1e3a5f;
  --gold:   #d4a017;
  --green:  #2ecc71;
  --accent: #e74c3c;

  --border:      #2d3748;
  --card-shadow: 0 2px 6px rgba(0,0,0,0.30);
  --card-hover:  0 4px 12px rgba(0,0,0,0.50);

  --tag-bg:   #1e3a5f;
  --tag-text: #e8e6e3;

  --tint-success: #1a3a2a;
  --tint-warning: #3a2e00;
  --tint-danger:  #3a0a0a;
  --tint-info:    #1a2744;
  --tint-formula: #2a2200;
  --tint-try:     #1a2e1a;
}
"""

# ── Dark-mode toggle CSS (injected into DRL lesson <style> blocks) ─────────
TOGGLE_CSS = """
    /* ── Dark-mode toggle (added by apply_theme.py) ── */
    .theme-toggle {
      position: absolute; top: 1rem; right: 4rem;
      background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.25);
      color: #fff; padding: .35rem .8rem; border-radius: 6px;
      cursor: pointer; font-size: .82rem; font-family: inherit; z-index: 102;
    }
"""

# ── Dark-mode toggle script (injected before </body> in DRL lessons) ───────
TOGGLE_SCRIPT = """
<script>
/* Dark-mode toggle — added by apply_theme.py */
function toggleTheme(){
  var n=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark';
  document.documentElement.setAttribute('data-theme',n);
  localStorage.setItem('theme',n);
  document.querySelector('.theme-toggle').textContent=n==='dark'?'☀ Light':'☾ Dark';
}
(function(){
  var s=localStorage.getItem('theme')||(window.matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');
  document.documentElement.setAttribute('data-theme',s);
})();
</script>
"""

# ── Helpers ────────────────────────────────────────────────────────────────

def site_path_for(src: Path) -> Path:
    """Return the site/ path that corresponds to a semester2 source file."""
    if str(src).startswith(str(SITE)):
        return src
    rel = src.relative_to(SEM2)
    parts = list(rel.parts)
    if "lessons" in parts:
        parts.remove("lessons")
    return SITE / "semester2" / Path(*parts)


def rel_theme_path(html_path: Path) -> str:
    """Return the relative href from html_path's site/ location to site/theme.css."""
    effective = site_path_for(html_path)
    depth = len(effective.relative_to(SITE).parts) - 1
    return ("../" * depth) + "theme.css"


def strip_root_block(html: str, keep_layout_tokens=False) -> str:
    """
    Remove :root { ... } and [data-theme="dark"] { ... } CSS variable blocks
    from inline <style>.  When keep_layout_tokens=True (SEML lectures) we
    keep --r, --mono, --sidebar, --dim inside a residual :root{}.
    """
    LAYOUT_PROPS = {"--r", "--mono", "--sidebar", "--dim"}

    def remove_block(text, pattern):
        """Remove all CSS blocks matching `pattern { ... }` (handles nesting)."""
        result = []
        i = 0
        for m in re.finditer(pattern, text):
            result.append(text[i:m.start()])
            # find matching closing brace
            depth = 0
            j = m.start()
            found_open = False
            while j < len(text):
                if text[j] == '{':
                    depth += 1
                    found_open = True
                elif text[j] == '}':
                    depth -= 1
                    if found_open and depth == 0:
                        i = j + 1
                        break
                j += 1
            else:
                i = j
        result.append(text[i:])
        return "".join(result)

    if keep_layout_tokens:
        # Extract layout tokens from :root before stripping
        layout_lines = []
        for m in re.finditer(r':root\s*\{', html):
            start = m.start()
            depth, j, found_open = 0, start, False
            while j < len(html):
                if html[j] == '{':
                    depth += 1; found_open = True
                elif html[j] == '}':
                    depth -= 1
                    if found_open and depth == 0:
                        block = html[m.end():j]
                        for line in block.splitlines():
                            stripped = line.strip()
                            if any(stripped.startswith(p) for p in LAYOUT_PROPS):
                                layout_lines.append("  " + stripped)
                        break
                j += 1

        html = remove_block(html, r':root\s*\{')
        html = remove_block(html, r'\[data-theme=["\']dark["\']\]\s*\{')

        if layout_lines:
            residual = "\n    :root {\n" + "\n".join(layout_lines) + "\n    }\n"
            html = html.replace("</style>", residual + "  </style>", 1)
    else:
        html = remove_block(html, r':root\s*\{')
        html = remove_block(html, r'\[data-theme=["\']dark["\']\]\s*\{')

    # Clean up blank lines left behind inside <style>
    html = re.sub(r'(<style[^>]*>)\n(\s*\n)+', r'\1\n', html)
    return html


def inject_link(html: str, href: str) -> str:
    """Inject <link rel="stylesheet"> as first child of <head> (once only)."""
    link_tag = f'  <link rel="stylesheet" href="{href}">\n'
    if 'theme.css' in html:
        # Already has a link — update the href in case depth changed
        html = re.sub(
            r'<link\s+rel=["\']stylesheet["\']\s+href=["\'][^"\']*theme\.css["\']>',
            link_tag.strip(),
            html
        )
        return html
    return re.sub(r'(<head[^>]*>\n?)', r'\1' + link_tag, html, count=1)


def add_data_theme(html: str) -> str:
    """Add data-theme="light" to <html> tag if not already present."""
    if 'data-theme' not in html:
        html = re.sub(r'<html\b', '<html data-theme="light"', html, count=1)
    return html


def inject_drl_toggle(html: str) -> str:
    """Add theme toggle button to .hdr div and wire up JS in DRL lesson files."""
    # Skip if already done
    if 'theme-toggle' in html:
        return html

    # Add CSS into <style> block
    html = html.replace('</style>', TOGGLE_CSS + '  </style>', 1)

    # Add button inside .hdr — place after the sb-toggle button if present
    if 'sb-toggle' in html:
        html = re.sub(
            r'(<button class="sb-toggle")',
            r'<button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle dark mode">&#9790; Dark</button>\n  \1',
            html, count=1
        )
    else:
        # Fallback: insert before closing </div> of .hdr block
        html = re.sub(
            r'(</div>\s*(?=\n<div class="sb-overlay"|<div class="wrap"))',
            r'  <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle dark mode">&#9790; Dark</button>\n\1',
            html, count=1
        )

    # Add script before </body>
    html = html.replace('</body>', TOGGLE_SCRIPT + '\n</body>', 1)
    return html


def normalise_storage_key(html: str) -> str:
    """Replace localStorage key 'aci-theme' with 'theme'."""
    return html.replace("'aci-theme'", "'theme'").replace('"aci-theme"', '"theme"')


# ── Group classification ───────────────────────────────────────────────────

# These files keep their :root intact (link-only)
EXAM_GUIDE_NAMES = {
    "exam-study-guide.html",
    "DRL-exam-study-guide.html",
    "NLP-exam-study-guide.html",
    "ACI-exam-study-guide.html",
}

def classify(path: Path):
    """Return processing group for an HTML file."""
    parts = path.parts
    name = path.name

    # SEML session lecture files (deep: session*/lecture.html)
    if "SEML" in parts and "session" in path.parent.name and name == "lecture.html":
        return "seml_lecture"

    # DRL lesson files (0001-0009)
    if ("DRL" in parts) and re.match(r'000\d-', name):
        return "drl_lesson"

    # Exam guides — link only, keep :root
    if name in EXAM_GUIDE_NAMES:
        return "exam_guide"

    # Everything else: full surgery
    return "standard"


# ── Main processing ────────────────────────────────────────────────────────

def process_file(path: Path):
    html = path.read_text(encoding="utf-8")
    original = html
    group = classify(path)
    href = rel_theme_path(path)

    # Always inject link
    html = inject_link(html, href)

    if group == "exam_guide":
        # Link only — leave :root untouched
        pass

    elif group == "seml_lecture":
        html = add_data_theme(html)
        html = strip_root_block(html, keep_layout_tokens=True)
        html = normalise_storage_key(html)

    elif group == "drl_lesson":
        html = add_data_theme(html)
        html = strip_root_block(html, keep_layout_tokens=False)
        html = inject_drl_toggle(html)
        html = normalise_storage_key(html)

    else:  # standard
        html = add_data_theme(html)
        html = strip_root_block(html, keep_layout_tokens=False)
        html = normalise_storage_key(html)

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def mirror_to_site(src: Path):
    """Copy a semester2 lesson file to its site/ counterpart (ADR-003)."""
    # semester2/ACI/lessons/foo.html → site/semester2/ACI/foo.html
    # semester2/SEML/lessons/session1-foundations/lecture.html
    #   → site/semester2/SEML/session1-foundations/lecture.html
    try:
        rel = src.relative_to(SEM2)
    except ValueError:
        return  # not under semester2, skip

    parts = list(rel.parts)
    # Remove "lessons" segment if present
    if "lessons" in parts:
        parts.remove("lessons")

    dest = SITE / "semester2" / Path(*parts)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def collect_html_files():
    """Yield all HTML files to process (site/ direct files + semester2 lessons)."""
    # site/ root files and subdirs (excluding semester2 — those come from sources)
    for f in SITE.glob("*.html"):
        yield f
    for f in (SITE / "study-plans").glob("*.html"):
        yield f

    # semester2 lesson sources (these get processed then mirrored to site/)
    for subject_dir in SEM2.iterdir():
        if not subject_dir.is_dir():
            continue
        lessons_dir = subject_dir / "lessons"
        if not lessons_dir.exists():
            continue
        for f in lessons_dir.rglob("*.html"):
            yield f

    # subject index files in semester2 root (index.html per subject)
    for subject_dir in SEM2.iterdir():
        idx = subject_dir / "index.html"
        if idx.exists():
            yield idx

    # Any remaining HTML files already in site/semester2/ (stale copies not
    # mirrored from a semester2/lessons/ source — e.g. old exam guides)
    for f in (SITE / "semester2").rglob("*.html"):
        yield f


# ── Entry point ────────────────────────────────────────────────────────────

def main():
    # 1. Write theme.css
    theme_path = SITE / "theme.css"
    theme_path.write_text(THEME_CSS, encoding="utf-8")
    print(f"  created  {theme_path.relative_to(ROOT)}")

    # 2. Process HTML files
    changed = []
    skipped = []

    seen = set()
    for html_file in sorted(collect_html_files()):
        if html_file in seen or not html_file.exists():
            continue
        seen.add(html_file)
        modified = process_file(html_file)
        rel = html_file.relative_to(ROOT)
        if modified:
            changed.append(rel)
            print(f"  updated  {rel}")
            # Mirror semester2 sources to site/
            if str(html_file).startswith(str(SEM2)):
                mirror_to_site(html_file)
        else:
            skipped.append(rel)

    # 3. Summary
    print(f"\n{'─'*55}")
    print(f"  theme.css created: {theme_path.relative_to(ROOT)}")
    print(f"  HTML files updated: {len(changed)}")
    print(f"  HTML files unchanged: {len(skipped)}")

    if skipped:
        print("\n  Unchanged (already up-to-date or no match):")
        for p in skipped:
            print(f"    {p}")

    # 4. Quick smoke-check
    print("\n  Smoke-check — files still missing theme.css link:")
    missing = []
    for f in SITE.rglob("*.html"):
        if 'theme.css' not in f.read_text(encoding="utf-8"):
            missing.append(f.relative_to(ROOT))
    if missing:
        for p in missing:
            print(f"    MISSING  {p}")
        sys.exit(1)
    else:
        print("    none — all clear")


if __name__ == "__main__":
    main()
