# Theming Guide — MTech Portal

This document defines the visual design system for all HTML lesson files in this portal.
Any new lesson, subject, or interactive page **must follow every rule here**.

---

## 1. Central theme file: `site/theme.css`

All colours live in **`site/theme.css`** and nowhere else.
To change any colour, edit that file only — every page inherits it automatically.

```
site/theme.css   ← the single source of truth for all colours
```

Every HTML file must link to it as the **first child of `<head>`**:

```html
<head>
  <link rel="stylesheet" href="../../theme.css">   <!-- depth varies, see table below -->
  ...
```

| File location | `href` value |
|---|---|
| `site/index.html`, `site/viewer.html` | `./theme.css` |
| `site/study-plans/*.html` | `../theme.css` |
| `site/semester2/{ACI,DRL,NLP,SEML}/*.html` | `../../theme.css` |
| `site/semester2/SEML/session*/lecture.html` | `../../../theme.css` |

---

## 2. CSS custom properties — use these, never raw hex

### Backgrounds

| Variable | Light value | Use for |
|---|---|---|
| `--bg` | `#fafaf8` | `body` background |
| `--surface` | `#ffffff` | Cards, modals |
| `--sidebar-bg` | `#f0f0ed` | Sidebar / nav panel |
| `--code-bg` | `#f4f4f0` | Code blocks |
| `--card-bg` | `#ffffff` | `.card` elements |
| `--card-border` | `#dddddd` | Card borders |

### Text

| Variable | Light value | Use for |
|---|---|---|
| `--text` | `#1a1a1a` | Body copy |
| `--text-muted` | `#555555` | Captions, meta |

### Brand colours

| Variable | Light value | Use for |
|---|---|---|
| `--navy` | `#1a2744` | Header bg, table headers |
| `--gold` | `#e8a020` | Accents, active links, borders |
| `--green` | `#27ae60` | Success, hover states |
| `--accent` | `#c0392b` | Danger, highlights |

### Semantic tints (callout / alert boxes)

| Variable | Light value | Use for |
|---|---|---|
| `--tint-success` | `#e8f5e9` | Green callouts, tips |
| `--tint-formula` | `#fff8e1` | Formula / yellow callouts |
| `--tint-warning` | `#fff3cd` | Warning boxes |
| `--tint-danger` | `#fdecea` | Error / examtip boxes |
| `--tint-info` | `#e8f0fe` | Info / definition boxes |
| `--tint-try` | `#f1f8e9` | "Try it yourself" boxes |

### Structural

| Variable | Use for |
|---|---|
| `--border` | Dividers, rule lines |
| `--card-shadow` | Box shadow on cards |
| `--card-hover` | Box shadow on hover |
| `--tag-bg` / `--tag-text` | Pill/badge elements |

### Dialect aliases (for compatibility with older files)

`--muted` → `--text-muted` · `--ink` → `--text` · `--panel` → `--card-bg` ·
`--panel2` → `--code-bg` · `--line` → `--card-border` · `--bg2` → `--sidebar-bg` ·
`--cyan` → `--gold` · `--violet` → `--accent` · `--amber` → `--gold`

---

## 3. Dark mode

Dark mode is toggled by setting `data-theme="dark"` on `<html>`.
`theme.css` provides all dark overrides automatically via `[data-theme="dark"] { ... }`.

### Every lesson file must have:

**1. `data-theme` attribute on `<html>`:**
```html
<html lang="en" data-theme="light">
```

**2. A toggle button** (in the header):
```html
<button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle dark mode">☾ Dark</button>
```

**3. Toggle script** (before `</body>`):
```html
<script>
function toggleTheme() {
  var n = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', n);
  localStorage.setItem('theme', n);
  document.querySelector('.theme-toggle').textContent = n === 'dark' ? '☀ Light' : '☾ Dark';
}
(function() {
  var s = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme:dark)').matches ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', s);
  document.addEventListener('DOMContentLoaded', function() {
    var btn = document.querySelector('.theme-toggle');
    if (btn) btn.textContent = s === 'dark' ? '☀ Light' : '☾ Dark';
  });
})();
</script>
```

**4. Toggle button CSS** (in `<style>`):
```css
.theme-toggle {
  position: absolute; top: 1rem; right: 4rem;
  background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.25);
  color: #fff; padding: .35rem .8rem; border-radius: 6px;
  cursor: pointer; font-size: .82rem; font-family: inherit; z-index: 102;
}
```

### localStorage key: always `'theme'`

Never use `'aci-theme'`, `'drl-theme'`, or any subject-prefixed key —
the key `'theme'` is shared across the whole portal so the user's preference persists when navigating between subjects.

### Hardcoded colours forbidden in dark mode

**Never** use inline `style="background:#f0fff4"` or similar on callout boxes — they stay light in dark mode and make text invisible. Always use a `--tint-*` variable:

```html
<!-- Wrong -->
<div class="card" style="background:#f0fff4;">

<!-- Right -->
<div class="card" style="background:var(--tint-success);">
```

---

## 4. Page template structure

Every lesson page must have this structural skeleton:

```html
<html lang="en" data-theme="light">
<head>
  <link rel="stylesheet" href="[depth]/theme.css">
  <!-- MathJax (ADR-001) -->
  <!-- page <style> block — layout only, no colour tokens -->
</head>
<body>
  <!-- 1. Full-width navy header -->
  <div class="hdr" style="background:var(--navy);color:white;...">
    <span class="tag">SUBJECT · SESSION N</span>
    <h1>Lesson Title</h1>
    <p class="sub">Subtitle</p>
    <nav class="nav"><a href="prev.html">← Prev</a> <a href="next.html">Next →</a></nav>
    <button class="theme-toggle" onclick="toggleTheme()">☾ Dark</button>
  </div>

  <!-- 2. Sidebar + main wrapper -->
  <div style="display:flex">
    <nav class="sidebar">  <!-- background:var(--sidebar-bg), width:260px -->
      <!-- section labels in var(--gold), links in var(--text) -->
    </nav>
    <main class="main">
      <!-- content -->
    </main>
  </div>

  <!-- 3. Toggle script (see Section 3) -->
</body>
</html>
```

### Sidebar rules

```css
nav.sidebar {
  width: 260px;
  flex-shrink: 0;
  background: var(--sidebar-bg);
  border-right: 1px solid var(--border);
  color: var(--text);
  padding: 2rem 1rem;
  position: sticky; top: 0; height: 100vh; overflow-y: auto;
}
nav.sidebar h4 { color: var(--gold); font-size: .68rem; letter-spacing: .12em; text-transform: uppercase; }
nav.sidebar a   { color: var(--text-muted); text-decoration: none; font-size: .85rem; }
nav.sidebar a:hover, nav.sidebar a.on { color: var(--gold); }
```

---

## 5. Subject-specific notes

### ACI (`semester2/ACI/lessons/`)
- Uses `position:fixed` sidebar with `margin-left:260px` on `.main`
- Toggle button is inside `.header-btns` div in the `.header` block
- localStorage key: `'theme'`

### DRL (`semester2/DRL/lessons/`)
- Toggle script must wrap `btn.textContent` update in `DOMContentLoaded` (button exists after parse)
- Callout box types: `.box.analogy` → `var(--tint-formula)`, `.box.examtip` → `var(--tint-danger)`, `.box.defn` → `var(--tint-info)`

### NLP (`semester2/NLP/lessons/`)
- Lessons 0001–0003 use `position:fixed` sidebar; lessons 0004–0006 use `display:flex` with sticky sidebar
- Header uses `var(--navy)` background, `white` text (not `var(--header-bg)` — that variable is undefined)

### SEML (`semester2/SEML/lessons/session*/lecture.html`)
- Uses `#sidebar` (id), `#main` (id) — not `.sidebar`/`.main` classes
- Residual `:root` block may only contain layout-only tokens: `--r`, `--mono`, `--sidebar` (the width), `--dim`
- Must NOT redefine `--sidebar-bg` or `--code-bg` in the residual `:root` — those override theme.css dark values

---

## 6. What NOT to do

| Forbidden | Use instead |
|---|---|
| `background: #f0fff4` inline | `background: var(--tint-success)` |
| `background: #fffbe6` inline | `background: var(--tint-formula)` |
| `background: #eef4ff` inline | `background: var(--tint-info)` |
| `color: #111` on `strong` | `color: var(--text)` |
| `color: white` on sidebar links | `color: var(--text-muted)` |
| Sidebar `background: var(--navy)` | `background: var(--sidebar-bg)` |
| `:root { --sidebar-bg: #f0f0ed; }` in lesson file | Remove — comes from theme.css |
| `localStorage.setItem('aci-theme', ...)` | `localStorage.setItem('theme', ...)` |
| Inline `:root {}` redefining `--bg`, `--navy`, `--gold`, etc. | Remove — comes from theme.css |

---

## 7. Audit tool

Run the Playwright audit to verify all pages pass before pushing:

```sh
node scripts/theme-audit.js
```

All pages should report `✓ (0 issues)`. The audit checks:
- `theme.css` is linked
- No inline `:root` redefining colour tokens (exam guides excluded)
- Body background matches `--bg` (`#fafaf8`)
- Dark mode toggle present and functional
- Lesson pages have header, sidebar, and main elements

---

## 8. apply_theme.py

The bulk-surgery script at `apply_theme.py` can be re-run if a new subject is added
or if files diverge from the standard. It:
- Injects the `theme.css` link into every HTML file
- Strips inline `:root` colour blocks
- Adds dark mode toggle wiring to DRL-style lessons
- Mirrors `semester2/` edits to `site/` (ADR-003)

```sh
python3 apply_theme.py
```
