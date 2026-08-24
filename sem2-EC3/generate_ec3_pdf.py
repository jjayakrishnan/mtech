#!/usr/bin/env python3
"""
ACI EC3 Study Notes — BITS Pilani 2-in-1 Portrait PDF Generator
Modules 4, 5, 6 · S1-2026-27
"""

from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
import math

# ─── Page & brand constants ───────────────────────────────────
W, H = A4          # 595.28 × 841.89 pts
SH   = H / 2      # Slide height (half page) ≈ 420.94

GOLD  = colors.HexColor('#E8A020')
BLUE  = colors.HexColor('#5B9BD5')
RED   = colors.HexColor('#C0392B')
NAVY  = colors.HexColor('#1C3A6B')
WHITE = colors.white
TEXT  = colors.HexColor('#1a1a2e')
MUTED = colors.HexColor('#666666')
GT    = colors.HexColor('#FFFBE6')   # gold tint
BT    = colors.HexColor('#EEF4FF')   # blue tint
GRT   = colors.HexColor('#F0FFF4')   # green tint
RT    = colors.HexColor('#FFF0F0')   # red tint
FGRAY = colors.HexColor('#F5F7FA')   # header bg

WATERMARK = "S1-2026-27  Work Integrated Learning Programmes  "
FOOTER_R  = "BITS Pilani, Pilani Campus"
OUT_FILE  = "/Users/jayakrishnanj/mtech/sem2-EC3/ACI-EC3-StudyNotes.pdf"


# ─── Chrome helpers ───────────────────────────────────────────

def wm(c, y0):
    """Draw diagonal watermark across slide."""
    c.saveState()
    c.translate(0, y0)
    c.rotate(33)
    c.setFont('Helvetica', 7)
    c.setFillColor(colors.Color(0, 0, 0, alpha=0.065))
    tw = c.stringWidth(WATERMARK, 'Helvetica', 7)
    for row in range(-4, 20):
        for col in range(-1, 5):
            c.drawString(col * tw - 10, row * 44, WATERMARK)
    c.restoreState()


def logo(c, y0):
    """Draw innovate/achieve/lead logo, top-right."""
    bw, bh, gap = 42, 14, 1
    x = W - 8 - (bw + gap) * 3
    yt = y0 + SH - 8
    for label, clr in [('innovate', GOLD), ('achieve', BLUE), ('lead', RED)]:
        c.setFillColor(clr)
        c.rect(x, yt - bh, bw, bh, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 5.5)
        lw = c.stringWidth(label, 'Helvetica-Bold', 5.5)
        c.drawString(x + (bw - lw) / 2, yt - bh + 4, label)
        x += bw + gap


def cbar(c, y, full=True):
    """Draw 3-colour bar (gold 35% | blue 45% | red 20%)."""
    c.setFillColor(GOLD);  c.rect(0,       y, W*0.35, 3, fill=1, stroke=0)
    c.setFillColor(BLUE);  c.rect(W*0.35,  y, W*0.45, 3, fill=1, stroke=0)
    c.setFillColor(RED);   c.rect(W*0.80,  y, W*0.20, 3, fill=1, stroke=0)


def header(c, y0, title, badge=None):
    c.setFillColor(FGRAY)
    c.rect(0, y0 + SH - 53, W, 53, fill=1, stroke=0)
    c.setFillColor(NAVY); c.setFont('Helvetica-Bold', 12.5)
    c.drawString(12, y0 + SH - 31, title)
    if badge:
        bw = c.stringWidth(badge, 'Helvetica-Bold', 7) + 12
        c.setFillColor(NAVY)
        c.roundRect(W - bw - 130, y0 + SH - 47, bw, 14, 3, fill=1, stroke=0)
        c.setFillColor(WHITE); c.setFont('Helvetica-Bold', 7)
        c.drawString(W - bw - 124, y0 + SH - 40, badge)
    cbar(c, y0 + SH - 56)
    logo(c, y0)


def footer(c, y0, pn):
    cbar(c, y0 + 19)
    c.setFont('Helvetica-Bold', 9); c.setFillColor(TEXT)
    c.drawRightString(W - 8, y0 + 6, str(pn))
    c.setFont('Helvetica', 7); c.setFillColor(MUTED)
    c.drawRightString(W - 22, y0 + 6, FOOTER_R)


def chrome(c, y0, title, pn, badge=None):
    """Full slide chrome: white bg + watermark + header + footer."""
    c.setFillColor(WHITE); c.rect(0, y0, W, SH, fill=1, stroke=0)
    # thin separator line between slides
    c.setStrokeColor(colors.HexColor('#DDDDDD')); c.setLineWidth(0.5)
    c.line(0, y0 + SH, W, y0 + SH)
    wm(c, y0)
    header(c, y0, title, badge)
    footer(c, y0, pn)


# Content area y-range inside a slide at y0
# y_top = y0 + SH - 60   y_bot = y0 + 26
def cb(y0):
    return 12, y0 + 26, W - 12, y0 + SH - 62


# ─── Micro text helpers ───────────────────────────────────────

def sh(c, x, y, txt, sz=10):
    """Section heading with gold underline."""
    c.setFont('Helvetica-Bold', sz); c.setFillColor(NAVY)
    c.drawString(x, y, txt)
    tw = c.stringWidth(txt, 'Helvetica-Bold', sz)
    c.setStrokeColor(GOLD); c.setLineWidth(1.2)
    c.line(x, y - 2, x + tw + 15, y - 2)
    return y - sz * 1.75


def bul(c, x, y, txt, ind=0, bold=False, sz=8.5, col=None, mw=None):
    """Wrapped bullet point. Returns new y."""
    col = col or TEXT
    fn  = 'Helvetica-Bold' if bold else 'Helvetica'
    bx  = x + ind * 14
    sym = '▸' if ind > 0 else '•'
    c.setFont(fn, sz); c.setFillColor(col)
    bw = c.stringWidth(sym + ' ', fn, sz)
    c.drawString(bx, y, sym + ' ')
    avail = (mw or (W - bx - 16)) - bw
    words = txt.split()
    line, tx = '', bx + bw
    for w in words:
        t2 = (line + ' ' + w).strip()
        if c.stringWidth(t2, fn, sz) <= avail:
            line = t2
        else:
            c.drawString(tx, y, line); y -= sz * 1.38
            tx, line = bx + bw + 3, w
    if line:
        c.drawString(tx, y, line); y -= sz * 1.38
    return y


def txt(c, x, y, t, fn='Helvetica', sz=8.5, col=None, mw=None):
    col = col or TEXT
    c.setFont(fn, sz); c.setFillColor(col)
    if not mw:
        c.drawString(x, y, t); return y - sz * 1.35
    words = t.split(); line = ''
    for w in words:
        t2 = (line + ' ' + w).strip()
        if c.stringWidth(t2, fn, sz) <= mw:
            line = t2
        else:
            c.drawString(x, y, line); y -= sz * 1.35; line = w
    if line: c.drawString(x, y, line); y -= sz * 1.35
    return y


def box(c, x, y, w, lines, bg, border=None, label=None, sz=8):
    """Rounded callout box. lines = list of (font, text) or str."""
    border = border or NAVY
    h = (len(lines) * (sz + 2.5)) + (16 if label else 10)
    c.setFillColor(bg); c.setStrokeColor(border); c.setLineWidth(0.6)
    c.roundRect(x, y - h, w, h, 4, fill=1, stroke=1)
    if label:
        c.setFont('Helvetica-Bold', 6.5); c.setFillColor(border)
        c.drawString(x + 6, y - 9, label)
    ty = y - (16 if label else 8)
    for line in lines:
        if isinstance(line, tuple):
            fn, tx_str = line
        else:
            fn, tx_str = 'Helvetica', line
        c.setFont(fn, sz); c.setFillColor(TEXT)
        c.drawString(x + 7, ty, tx_str); ty -= sz + 2.5
    return y - h - 5


def tbl(c, x, y, data, widths, rh=12, header_bg=NAVY):
    """Simple table. Returns new y."""
    t = Table(data, colWidths=widths, rowHeights=rh)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), header_bg),
        ('TEXTCOLOR',  (0, 0), (-1, 0), WHITE),
        ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0, 0), (-1,-1), 7.5),
        ('FONTNAME',   (0, 1), (-1,-1), 'Helvetica'),
        ('TEXTCOLOR',  (0, 1), (-1,-1), TEXT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, colors.HexColor('#F0F4FF')]),
        ('GRID',       (0, 0), (-1,-1), 0.4, colors.HexColor('#CCCCCC')),
        ('VALIGN',     (0, 0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING',(0, 0), (-1,-1), 4),
        ('RIGHTPADDING',(0, 0), (-1,-1), 4),
        ('TOPPADDING', (0, 0), (-1,-1), 2),
        ('BOTTOMPADDING',(0, 0), (-1,-1), 2),
    ]))
    _, th = t.wrapOn(c, sum(widths), 999)
    t.drawOn(c, x, y - th)
    return y - th - 6


def tbl_highlight(c, x, y, data, widths, hi_rows=(), rh=12):
    """Table with highlighted rows."""
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR',  (0, 0), (-1, 0), WHITE),
        ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0, 0), (-1,-1), 7.5),
        ('FONTNAME',   (0, 1), (-1,-1), 'Helvetica'),
        ('TEXTCOLOR',  (0, 1), (-1,-1), TEXT),
        ('GRID',       (0, 0), (-1,-1), 0.4, colors.HexColor('#CCCCCC')),
        ('VALIGN',     (0, 0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING',(0, 0), (-1,-1), 4),
        ('RIGHTPADDING',(0, 0), (-1,-1), 4),
        ('TOPPADDING', (0, 0), (-1,-1), 2),
        ('BOTTOMPADDING',(0, 0), (-1,-1), 2),
    ]
    for r in hi_rows:
        style_cmds.append(('BACKGROUND', (0, r), (-1, r), colors.HexColor('#D4EDDA')))
    t = Table(data, colWidths=widths, rowHeights=rh)
    t.setStyle(TableStyle(style_cmds))
    _, th = t.wrapOn(c, sum(widths), 999)
    t.drawOn(c, x, y - th)
    return y - th - 6


# ─── Cover slide ──────────────────────────────────────────────

def slide_cover(c, y0, pn):
    c.setFillColor(NAVY); c.rect(0, y0, W, SH, fill=1, stroke=0)
    c.setStrokeColor(colors.HexColor('#DDDDDD')); c.setLineWidth(0.5)
    c.line(0, y0 + SH, W, y0 + SH)
    wm(c, y0)
    c.setFillColor(WHITE); c.setFont('Helvetica-Bold', 21)
    c.drawCentredString(W/2, y0 + SH - 80, 'Advanced Computing for AI')
    cbar(c, y0 + SH - 93)
    c.setFont('Helvetica-Bold', 15); c.setFillColor(GOLD)
    c.drawCentredString(W/2, y0 + SH - 120, 'EC3  Comprehensive Exam  —  Study Notes')
    c.setFont('Helvetica', 8.5); c.setFillColor(colors.HexColor('#B8C8E8'))
    mods = [
        'Module 4: Knowledge Representation & Logic  (CS9–CS10)',
        'Module 5: Multi-Agent Decision Making & Game Theory  (CS14)',
        'Module 6: Probabilistic Reasoning & HMM  (CS11–CS12)',
        'Module 7: Ethics & XAI  (CS13)',
    ]
    for i, m in enumerate(mods):
        c.drawCentredString(W/2, y0 + SH - 158 - i * 15, m)
    cbar(c, y0 + SH - 234)
    c.setFont('Helvetica', 7.5); c.setFillColor(WHITE)
    info = [
        'Prof. Parthasarathy P.D.  |  AIMLCZG557 / AECLZG557',
        'BITS Pilani WILP  ·  S1-2026-27  ·  Open Book Exam',
        'Exclusions: Dynamic Bayesian Networks  ·  Prolog programs',
    ]
    for i, l in enumerate(info):
        c.drawCentredString(W/2, y0 + SH - 254 - i * 12, l)
    logo(c, y0)
    footer(c, y0, pn)


# ─── Slide render functions ───────────────────────────────────

def s_module_title(c, y0, pn, mod_num, title, sub, topics):
    """Module divider slide."""
    c.setFillColor(colors.HexColor('#EEF4FF')); c.rect(0, y0, W, SH, fill=1, stroke=0)
    c.setStrokeColor(colors.HexColor('#DDDDDD')); c.setLineWidth(0.5)
    c.line(0, y0 + SH, W, y0 + SH)
    wm(c, y0)
    # Left accent bar
    c.setFillColor(GOLD); c.rect(0, y0, 8, SH, fill=1, stroke=0)
    # Module badge
    c.setFillColor(NAVY); c.roundRect(20, y0 + SH - 70, 80, 26, 6, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(60, y0 + SH - 53, f'Module {mod_num}')
    # Title
    c.setFillColor(NAVY); c.setFont('Helvetica-Bold', 18)
    c.drawString(20, y0 + SH - 110, title)
    # Subtitle
    c.setFont('Helvetica', 9); c.setFillColor(MUTED)
    c.drawString(20, y0 + SH - 128, sub)
    cbar(c, y0 + SH - 135)
    # Topics
    c.setFont('Helvetica-Bold', 8); c.setFillColor(NAVY)
    c.drawString(20, y0 + SH - 158, 'Topics Covered:')
    ty = y0 + SH - 176
    for top in topics:
        c.setFont('Helvetica', 8); c.setFillColor(TEXT)
        c.drawString(30, ty, '▸  ' + top); ty -= 14
    # Slide reference
    logo(c, y0)
    footer(c, y0, pn)


def s_kb_agents(c, y0, pn):
    chrome(c, y0, 'KB Agents: The Tell–Ask Cycle', pn, 'Module 4')
    _, yb, _, yt = cb(y0)
    y = yt - 2
    y = sh(c, 14, y, 'What is a Knowledge-Based Agent?')
    y = bul(c, 14, y, 'Maintains a Knowledge Base (KB) — a set of sentences about the world')
    y = bul(c, 14, y, 'TELL: add new information to the KB   (STORE in KB)')
    y = bul(c, 14, y, 'ASK: query the KB for what is true   (RETRIEVE from KB)')
    y = bul(c, 14, y, 'INFER: deduce new facts from existing KB sentences')
    y -= 6
    y = sh(c, 14, y, 'Wumpus World — PEAS', sz=9.5)
    y = tbl(c, 14, y,
        [['Component', 'Description'],
         ['Performance', '+1000 gold, −1000 death, −1/step, −10/arrow'],
         ['Environment', '4×4 grid: hidden pits, wumpus, gold; partially observable'],
         ['Actuators', 'Move Forward, Turn Left/Right, Grab, Shoot, Climb'],
         ['Sensors',   '[Stench, Breeze, Glitter, Bump, Scream] — local percepts']],
        [70, W - 14 - 70 - 14], rh=13)
    y -= 4
    y = sh(c, 14, y, 'Wumpus Inference Example', sz=9)
    y = bul(c, 14, y, 'Percept [None,None,…] at [1,1]  →  No pit in [1,2] or [2,1]')
    y = bul(c, 14, y, 'Percept [Stench,…] at [1,1]  →  Wumpus in [1,2] or [2,1]')
    y = bul(c, 14, y, 'Breeze at [2,1]  →  Pit in [2,2] or [3,1]')


def s_prop_logic(c, y0, pn):
    chrome(c, y0, 'Propositional Logic: Syntax & Semantics', pn, 'Module 4')
    _, yb, _, yt = cb(y0)
    y = yt - 2
    y = sh(c, 14, y, 'Propositional Syntax')
    y = bul(c, 14, y, 'Atoms: P, Q, R  (can be True or False)', bold=True)
    y = bul(c, 14, y, 'Connectives:  ¬ (NOT)  ∧ (AND)  ∨ (OR)  → (IMPLIES)  ↔ (IFF)')
    y = bul(c, 14, y, 'Literal: atom or its negation  |  Clause: disjunction of literals')
    y -= 6
    y = sh(c, 14, y, 'Key Logical Equivalences  (must memorize)', sz=9.5)
    y = tbl(c, 14, y,
        [['Equivalence', 'Form', 'Name'],
         ['α → β', '≡  ¬α ∨ β', 'Implication Elim.'],
         ['α ↔ β', '≡  (α→β) ∧ (β→α)', 'Biconditional Elim.'],
         ['¬(α ∧ β)', '≡  ¬α ∨ ¬β', "De Morgan's AND"],
         ['¬(α ∨ β)', '≡  ¬α ∧ ¬β', "De Morgan's OR"],
         ['¬¬α', '≡  α', 'Double Negation'],
         ['α → β', '≡  ¬β → ¬α', 'Contrapositive']],
        [120, 160, 120], rh=12)
    y -= 4
    y = sh(c, 14, y, 'Entailment', sz=9)
    y = bul(c, 14, y, 'KB ⊨ α  means: in every model where KB is true, α is also true')
    y = bul(c, 14, y, 'Test: enumerate all truth assignments; if KB true → α must be true')
    box(c, 14, y, W-28,
        ['EXAM TIP: Entailment is "necessary truth", not just "happens to be true"'],
        RT, RED, '⚠ Trap')


def s_cnf(c, y0, pn):
    chrome(c, y0, 'CNF Conversion: 4-Step Algorithm', pn, 'Module 4')
    _, yb, _, yt = cb(y0)
    y = yt - 2
    y = sh(c, 14, y, 'Conjunctive Normal Form (CNF)')
    y = bul(c, 14, y, 'CNF = conjunction (AND) of clauses, each clause = disjunction (OR) of literals')
    y = bul(c, 14, y, 'Required for Resolution algorithm — every KB sentence must be in CNF')
    y -= 4
    y = sh(c, 14, y, '4-Step CNF Conversion Algorithm', sz=9.5)
    steps = [
        ['Step', 'Rule', 'Example'],
        ['1. Elim ↔', 'α ↔ β  →  (α→β) ∧ (β→α)', 'A↔B → (A→B)∧(B→A)'],
        ['2. Elim →', 'α → β  →  ¬α ∨ β', '(A→B) → (¬A∨B)'],
        ['3. Move ¬ in', 'De Morgan: ¬(α∧β)→¬α∨¬β', '¬(A∧B) → ¬A∨¬B'],
        ['4. Distribute ∨', 'α∨(β∧γ)→(α∨β)∧(α∨γ)', 'A∨(B∧C)→(A∨B)∧(A∨C)'],
    ]
    y = tbl(c, 14, y, steps, [55, 200, 150], rh=13)
    y -= 4
    y = sh(c, 14, y, 'Worked Example: Convert  (A → B) ∧ ¬(B ∨ C)', sz=9)
    y = bul(c, 14, y, 'Step 1 (no ↔ present, skip)')
    y = bul(c, 14, y, 'Step 2: (¬A ∨ B) ∧ ¬(B ∨ C)')
    y = bul(c, 14, y, 'Step 3: (¬A ∨ B) ∧ (¬B ∧ ¬C)')
    y = bul(c, 14, y, 'Step 4: already in CNF  →  {¬A,B}  ∧  {¬B}  ∧  {¬C}')
    box(c, 14, y, W-28,
        ['Step 4 (distributing ∨ over ∧) is the most error-prone — double-check carefully'],
        RT, RED, '⚠ Trap')


def s_resolution(c, y0, pn):
    chrome(c, y0, 'Resolution Rule & Proof by Refutation', pn, 'Module 4')
    _, yb, _, yt = cb(y0)
    y = yt - 2
    y = sh(c, 14, y, 'The Resolution Rule')
    y = bul(c, 14, y, 'If  P ∨ Q  and  ¬P ∨ R  then resolve to  Q ∨ R  (cancel complementary P, ¬P)', bold=True)
    y = bul(c, 14, y, 'Unit resolution: If  P  and  ¬P ∨ Q  then  Q  (Modus Ponens)')
    y -= 4
    y = sh(c, 14, y, 'Resolution Refutation (Proof by Contradiction)', sz=9.5)
    y = bul(c, 14, y, '1.  Negate goal: to prove α from KB, add ¬α to KB')
    y = bul(c, 14, y, '2.  Convert all sentences to CNF')
    y = bul(c, 14, y, '3.  Apply resolution until empty clause □ or no new clauses')
    y = bul(c, 14, y, '4.  If □ reached  →  KB ⊨ α  ✓  (contradiction means goal is proved)')
    y -= 6
    y = sh(c, 14, y, 'Trace Example: Prove Q from {P→Q, P}', sz=9)
    y = tbl_highlight(c, 14, y,
        [['Step', 'Clause 1', 'Clause 2', 'Resolvent', 'Notes'],
         ['1', '{¬P, Q}', '{P}', '{Q}', 'Unit res. → Q proved'],
         ['2', '{¬Q}  (negated goal)', '{Q}', '□  (empty!)', 'Contradiction → proved']],
        [28, 100, 120, 80, 120], hi_rows=(2,), rh=13)
    box(c, 14, y - 2, W-28,
        ['Empty clause □ = contradiction = goal proved.  If no new clause can be derived → not provable'],
        GT, GOLD, '★ Key Rule')


def s_fol(c, y0, pn):
    chrome(c, y0, 'First-Order Logic: Syntax & Quantifiers', pn, 'Module 4')
    _, yb, _, yt = cb(y0)
    y = yt - 2
    y = sh(c, 14, y, 'FOL Vocabulary')
    y = tbl(c, 14, y,
        [['Element', 'Description', 'Examples'],
         ['Constants', 'Specific named objects', 'John, Pilani, 3'],
         ['Variables', 'Range over objects', 'x, y, z'],
         ['Functions', 'Maps objects → object', 'LeftLeg(x), Father(y)'],
         ['Predicates', 'Maps objects → T/F', 'King(x), Loves(x,y)'],
         ['Quantifiers', 'Universal ∀, Existential ∃', '∀x King(x), ∃x Crown(x)']],
        [70, 200, 150], rh=12)
    y -= 4
    y = sh(c, 14, y, 'Quantifier Examples', sz=9.5)
    y = bul(c, 14, y, '∀x  King(x) → Person(x)   meaning: "All kings are people"')
    y = bul(c, 14, y, '∃x  Crown(x) ∧ OnHead(x, John)   meaning: "Something is a crown on John"')
    y = bul(c, 14, y, '∀x ∀y  Loves(x, y)   meaning: "Everyone loves everyone"')
    y -= 4
    y = sh(c, 14, y, 'English → FOL Conversions', sz=9)
    y = bul(c, 14, y, '"No dog bites John"   →   ¬∃x  Dog(x) ∧ Bites(x, John)')
    y = bul(c, 14, y, '"Every student passes some exam"   →   ∀s ∃e  Student(s) → Passes(s,e)')
    box(c, 14, y - 2, W-28,
        ['∀ with → is standard for "all", ∃ with ∧ is standard for "there exists"',
         'Do not mix: ∀x P(x)∧Q(x) ≠ ∀x P(x)→Q(x)  (the ∧ form is usually wrong)'],
        RT, RED, '⚠ Common Trap')


def s_chaining(c, y0, pn):
    chrome(c, y0, 'Forward & Backward Chaining', pn, 'Module 4')
    _, yb, _, yt = cb(y0)
    y = yt - 2
    y = sh(c, 14, y, 'Forward Chaining (Data-Driven, BFS)')
    y = bul(c, 14, y, 'Start from known facts, fire rules whose premises are satisfied')
    y = bul(c, 14, y, 'Repeat until goal is derived or no new fact can be inferred')
    y = bul(c, 14, y, 'Complete for Horn clause KBs  |  Used in: expert systems, databases')
    y -= 4
    y = sh(c, 14, y, 'Backward Chaining (Goal-Driven, DFS)', sz=9.5)
    y = bul(c, 14, y, 'Start from goal, work backward to find supporting facts')
    y = bul(c, 14, y, 'Efficient when goal space is small  |  Used in: Prolog, theorem proving')
    y -= 4
    y = sh(c, 14, y, 'Example KB: Animal Rules', sz=9)
    y = tbl(c, 14, y,
        [['Rule / Fact', 'Content'],
         ['R1', 'Feathers(x) → Bird(x)'],
         ['R2', 'Fly(x) ∧ Feathers(x) → CanFly(x)'],
         ['Fact', 'Feathers(tweety) = True,  Fly(tweety) = True'],
         ['Query', 'CanFly(tweety)?']],
        [30, W - 30 - 28], rh=13)
    y = bul(c, 14, y, 'FC trace: Feathers(tweety)→ Bird(tweety) via R1; Fly+Feathers → CanFly ✓')
    y = bul(c, 14, y, 'BC trace: CanFly? ← need Fly ∧ Feathers ← both in KB ✓')
    box(c, 14, y - 2, W-28,
        ['Both give same result for Horn clauses; FC is sound&complete; BC is sound&complete too'],
        BT, BLUE, 'ℹ Note')


def s_prob_fundamentals(c, y0, pn):
    chrome(c, y0, 'Probability Fundamentals', pn, 'Module 6')
    _, yb, _, yt = cb(y0)
    y = yt - 2
    y = sh(c, 14, y, 'Core Probability Rules')
    y = tbl(c, 14, y,
        [['Rule', 'Formula', 'Meaning'],
         ['Sum Rule', 'P(A) = Σ P(A,B=b)', 'Marginalize out B'],
         ['Product Rule', 'P(A,B) = P(A|B)·P(B)', 'Joint = conditional × marginal'],
         ["Bayes' Theorem", 'P(H|E) = P(E|H)·P(H)/P(E)', 'Update belief given evidence'],
         ['Chain Rule', 'P(A,B,C) = P(A|B,C)·P(B|C)·P(C)', 'Expand joint over n vars']],
        [80, 190, 145], rh=13)
    y -= 4
    y = sh(c, 14, y, "Bayes' Theorem — Components", sz=9.5)
    y = bul(c, 14, y, 'P(H|E): posterior — belief in H given evidence E', bold=True)
    y = bul(c, 14, y, 'P(E|H): likelihood — probability of evidence if H is true')
    y = bul(c, 14, y, 'P(H): prior — initial belief in H before evidence')
    y = bul(c, 14, y, 'P(E): normalisation constant — P(E) = Σ_h P(E|H=h)·P(H=h)')
    y -= 4
    y = sh(c, 14, y, 'Conditional Independence', sz=9)
    y = bul(c, 14, y, 'A ⊥ B | C  means: given C, knowing A gives no info about B')
    y = bul(c, 14, y, 'Key: P(A|B,C) = P(A|C)  when A ⊥ B | C')
    box(c, 14, y - 2, W-28,
        ["Normalise using α (alpha): P(X|e) = α · P(X, e)  where α = 1/P(e)"],
        GT, GOLD, '★ Trick')


def s_bayes_net(c, y0, pn):
    chrome(c, y0, 'Bayesian Networks: Structure & CPTs', pn, 'Module 6')
    _, yb, _, yt = cb(y0)
    y = yt - 2
    y = sh(c, 14, y, 'What is a Bayesian Network?')
    y = bul(c, 14, y, 'Directed Acyclic Graph (DAG): nodes = random variables, edges = direct causation')
    y = bul(c, 14, y, 'Each node X has a CPT: P(X | Parents(X))')
    y = bul(c, 14, y, 'Joint distribution: P(X1,…,Xn) = ∏ P(Xi | Parents(Xi))')
    y -= 4
    y = sh(c, 14, y, 'Toothache–Cavity–Catch Network', sz=9.5)
    y = tbl(c, 14, y,
        [['Variable', 'Parents', 'CPT (sample values)'],
         ['Cavity (C)', 'None', 'P(C=T) = 0.1'],
         ['Toothache (T)', 'Cavity', 'P(T=T|C=T)=0.6, P(T=T|C=F)=0.05'],
         ['Catch (X)', 'Cavity', 'P(X=T|C=T)=0.9, P(X=T|C=F)=0.02']],
        [100, 80, W - 100 - 80 - 28], rh=13)
    y -= 4
    y = sh(c, 14, y, 'Inference by Enumeration', sz=9)
    y = bul(c, 14, y, 'P(Cavity|Toothache=T) = α · Σ_{catch} P(C,Toothache=T,catch)')
    y = bul(c, 14, y, '= α · [P(C)·P(T=T|C)·Σ P(catch|C)]')
    y = bul(c, 14, y, 'Result: P(C=T|T=T) ≈ 0.545  |  P(C=F|T=T) ≈ 0.455')
    box(c, 14, y - 2, W-28,
        ['Dynamic BNs are EXCLUDED from EC3 — only static BNs (fixed time-slice CPTs)'],
        RT, RED, '⚠ EC3 Exclusion')


def s_hmm(c, y0, pn):
    chrome(c, y0, 'Hidden Markov Models (HMM)', pn, 'Module 6')
    _, yb, _, yt = cb(y0)
    y = yt - 2
    y = sh(c, 14, y, 'HMM Structure')
    y = bul(c, 14, y, 'Hidden states X1,X2,…: not directly observable')
    y = bul(c, 14, y, 'Observations O1,O2,…: observed evidence (emissions)')
    y = bul(c, 14, y, 'Transition matrix A: P(Xt | Xt-1)  — how states evolve')
    y = bul(c, 14, y, 'Emission matrix B: P(Ot | Xt)  — how observations are generated')
    y = bul(c, 14, y, 'Initial dist π: P(X1)  — starting state probabilities')
    y -= 4
    y = sh(c, 14, y, 'Weather–Pressure Example', sz=9.5)
    y = tbl(c, 14, y,
        [['', 'Sunny (next)', 'Rainy (next)'],
         ['Sunny (now)', '0.8', '0.2'],
         ['Rainy (now)', '0.4', '0.6']],
        [90, 120, 120], rh=13)
    y -= 4
    y = tbl(c, 14, y,
        [['State', 'P(High pressure)', 'P(Low pressure)'],
         ['Sunny', '0.9', '0.1'],
         ['Rainy', '0.2', '0.8']],
        [90, 120, 120], rh=13)
    y -= 2
    y = sh(c, 14, y, 'HMM Tasks', sz=9)
    y = bul(c, 14, y, 'Filtering (FPA): P(Xt | O1:t)  — most likely current state given obs so far')
    y = bul(c, 14, y, 'Smoothing: P(Xk | O1:T) k<T  — refine past state estimate with future obs')
    y = bul(c, 14, y, 'Decoding (Viterbi): most likely STATE SEQUENCE given observations')


def s_viterbi(c, y0, pn):
    chrome(c, y0, 'Viterbi Algorithm', pn, 'Module 6')
    _, yb, _, yt = cb(y0)
    y = yt - 2
    y = sh(c, 14, y, 'Viterbi: Most Likely State Sequence')
    y = bul(c, 14, y, 'Goal: find argmax P(X1,X2,…,Xn | O1:n)', bold=True)
    y = bul(c, 14, y, 'Initialise: δ1(j) = π(j) · b_j(O1)  — prob of best path ending in state j at t=1')
    y = bul(c, 14, y, 'Recurse: δt(j) = max_i [δt-1(i) · a_ij] · b_j(Ot)')
    y = bul(c, 14, y, 'Backtrack: ψt(j) = argmax_i [δt-1(i) · a_ij]  — which previous state was best')
    y -= 4
    y = sh(c, 14, y, 'Viterbi Trace: Observations = [High, Low]  (Weather HMM)', sz=9.5)
    y = tbl_highlight(c, 14, y,
        [['t', 'State j', 'δt(j)', 'ψt(j)', 'Computation'],
         ['1', 'Sunny', '0.360', '—', 'π(S)·P(High|S)=0.4·0.9'],
         ['1', 'Rainy', '0.040', '—', 'π(R)·P(High|R)=0.2·0.2'],
         ['2', 'Sunny', '0.026', 'Sunny', 'max(0.36·0.8, 0.04·0.4)·P(Low|S)=0.288·0.1'],
         ['2', 'Rainy', '0.189', 'Sunny', 'max(0.36·0.2, 0.04·0.6)·P(Low|R)=0.072·0.8 — BEST']],
        [16, 54, 56, 54, W - 16 - 54 - 56 - 54 - 28], hi_rows=(4,), rh=12)
    y = bul(c, 14, y, 'Best path: backtrack from δ2 max (Rainy) → ψ2(Rainy)=Sunny  →  [Sunny, Rainy]')
    box(c, 14, y - 2, W-28,
        ['Viterbi uses MAX not SUM; FPA (filtering) uses SUM.  Viterbi = MAX·PRODUCT path'],
        GT, GOLD, '★ Key Difference')


def s_fpa(c, y0, pn):
    chrome(c, y0, 'Forward Algorithm (Filtering / FPA)', pn, 'Module 6')
    _, yb, _, yt = cb(y0)
    y = yt - 2
    y = sh(c, 14, y, 'Forward Probability Algorithm')
    y = bul(c, 14, y, 'Computes α_t(j) = P(O1:t, Xt=j)  — joint prob of obs AND being in state j', bold=True)
    y = bul(c, 14, y, 'Initialise: α1(j) = π(j) · b_j(O1)')
    y = bul(c, 14, y, 'Recurse:   α_t(j) = b_j(Ot) · Σ_i [ α_t-1(i) · a_ij ]')
    y = bul(c, 14, y, 'Output: P(Xt=j | O1:t) = α_t(j) / Σ_k α_t(k)  (normalise)')
    y -= 4
    y = sh(c, 14, y, 'FPA Trace: Observations = [High, Low]', sz=9.5)
    y = tbl_highlight(c, 14, y,
        [['t', 'State j', 'α_t(j)', 'Computation'],
         ['1', 'Sunny', '0.360', 'π(S)·P(High|S) = 0.4 × 0.9'],
         ['1', 'Rainy', '0.040', 'π(R)·P(High|R) = 0.2 × 0.2'],
         ['2', 'Sunny', '0.026', 'P(Low|S)·[α1(S)·A_SS + α1(R)·A_RS] = 0.1·(0.36·0.8+0.04·0.4)'],
         ['2', 'Rainy', '0.189', 'P(Low|R)·[α1(S)·A_SR + α1(R)·A_RR] = 0.8·(0.36·0.2+0.04·0.6)']],
        [16, 54, 56, W - 16 - 54 - 56 - 28], hi_rows=(3, 4), rh=12)
    y = bul(c, 14, y, 'Normalise: P(Rainy|obs) = 0.189/(0.026+0.189) = 0.879  →  most likely Rainy')
    box(c, 14, y - 2, W-28,
        ['FPA sums over all paths (total probability); Viterbi maximises over the single best path'],
        BT, BLUE, 'ℹ Compare')


def s_multiagent_intro(c, y0, pn):
    chrome(c, y0, 'Multi-Agent Environments & Game Theory', pn, 'Module 5')
    _, yb, _, yt = cb(y0)
    y = yt - 2
    y = sh(c, 14, y, 'Multi-Agent System Taxonomy')
    y = tbl(c, 14, y,
        [['Type', 'Description', 'Example'],
         ['Fully cooperative', 'All agents share same goal', 'Robot soccer team'],
         ['Fully competitive', 'Zero-sum: one wins, other loses', 'Chess, Poker'],
         ['Mixed', 'Self-interested; may cooperate', 'Market, negotiation']],
        [100, 220, 100], rh=13)
    y -= 4
    y = sh(c, 14, y, 'Key Concepts', sz=9.5)
    y = bul(c, 14, y, 'Strategy: a complete plan specifying action for every possible situation', bold=True)
    y = bul(c, 14, y, 'Pure strategy: deterministic choice  |  Mixed strategy: randomised choice')
    y = bul(c, 14, y, 'Payoff: utility an agent receives for a combination of strategies')
    y -= 4
    y = sh(c, 14, y, 'Normal Form Game', sz=9)
    y = bul(c, 14, y, 'Represent by payoff matrix: rows = Player 1 strategies, cols = Player 2')
    y = bul(c, 14, y, 'Entry (a, b): Player 1 gets a, Player 2 gets b')
    box(c, 14, y - 2, W-28,
        ['For EC3: focus on pure strategies Nash Equilibrium, dominant strategies, Shapley'],
        BT, BLUE, 'EC3 Focus')


def s_payoff_nash(c, y0, pn):
    chrome(c, y0, 'Payoff Matrices, Dominant Strategies & Nash Equilibrium', pn, 'Module 5')
    _, yb, _, yt = cb(y0)
    y = yt - 2
    y = sh(c, 14, y, "Prisoner's Dilemma — Classic Payoff Matrix")
    y = tbl_highlight(c, 14, y,
        [['', 'P2: Cooperate (C)', 'P2: Defect (D)'],
         ['P1: Cooperate (C)', '(−1, −1)', '(−3, 0)'],
         ['P1: Defect (D)', '(0, −3)', '(−2, −2)  ← NE']],
        [110, 150, 160], hi_rows=(2,), rh=14)
    y -= 2
    y = bul(c, 14, y, 'Dominant strategy for each player: Defect — regardless of other player')
    y = bul(c, 14, y, 'Nash Equilibrium at (D, D): neither player benefits by unilaterally changing')
    y -= 4
    y = sh(c, 14, y, 'Finding Nash Equilibrium (Best-Response Method)', sz=9.5)
    y = bul(c, 14, y, '1. For each column (P2 strategy), mark P1\'s best response with ★')
    y = bul(c, 14, y, '2. For each row (P1 strategy), mark P2\'s best response with ★')
    y = bul(c, 14, y, '3. Nash Equilibrium: cell where BOTH payoffs are starred  (★★)')
    y -= 4
    y = sh(c, 14, y, 'Battle of the Sexes — Multiple Nash Equilibria', sz=9)
    y = tbl_highlight(c, 14, y,
        [['', 'P2: Opera (O)', 'P2: Football (F)'],
         ['P1: Opera (O)', '(2, 1) ← NE1', '(0, 0)'],
         ['P1: Football (F)', '(0, 0)', '(1, 2) ← NE2']],
        [100, 160, 160], hi_rows=(1, 2), rh=14)
    box(c, 14, y - 2, W-28,
        ['A game can have 0, 1, or multiple pure Nash Equilibria (BoS has 2 pure NE)'],
        GT, GOLD, '★ Key Fact')


def s_ieds_shapley(c, y0, pn):
    chrome(c, y0, 'IEDS & Shapley Value', pn, 'Module 5')
    _, yb, _, yt = cb(y0)
    y = yt - 2
    y = sh(c, 14, y, 'IEDS: Iterated Elimination of Dominated Strategies')
    y = bul(c, 14, y, 'Strictly dominated: strategy s is dominated if ∃ s\' with higher payoff in ALL cases')
    y = bul(c, 14, y, 'Remove dominated strategies iteratively; surviving strategies = rationalizable')
    y = bul(c, 14, y, 'If one strategy survives per player → unique Nash Equilibrium')
    y -= 4
    y = sh(c, 14, y, 'Shapley Value — Fair Payoff in Cooperative Games', sz=9.5)
    y = bul(c, 14, y, 'Unique fair division satisfying: efficiency, symmetry, null player, linearity', bold=True)
    y = bul(c, 14, y, 'φ_i(v) = Σ_{S ⊆ N\\{i}} [|S|!(|N|-|S|-1)!/|N|!] · [v(S∪{i}) - v(S)]')
    y = bul(c, 14, y, 'Interpretation: i\'s Shapley value = average marginal contribution over all orderings')
    y -= 4
    y = sh(c, 14, y, 'Shapley Example: 3 Programmers A,B,C', sz=9)
    y = tbl_highlight(c, 14, y,
        [['Ordering', 'MC(A)', 'MC(B)', 'MC(C)'],
         ['A,B,C', '40', '20', '40'],
         ['A,C,B', '40', '20', '40'],
         ['B,A,C', '60', '0', '40'],
         ['B,C,A', '60', '0', '40'],
         ['C,A,B', '60', '0', '40'],
         ['C,B,A', '60', '0', '40'],
         ['Average φ', '56.7', '6.7', '36.7']],
        [90, 80, 80, 80], hi_rows=(7,), rh=11)
    box(c, 14, y - 2, W-28,
        ['Efficiency: φA + φB + φC = v(N)  — total value is fully distributed'],
        GT, GOLD, '★ Check')


def s_collective(c, y0, pn):
    chrome(c, y0, 'Collective Decision Making & Voting', pn, 'Module 5')
    _, yb, _, yt = cb(y0)
    y = yt - 2
    y = sh(c, 14, y, 'Social Choice: Aggregating Preferences')
    y = bul(c, 14, y, 'Given n voters each with preferences over m alternatives — how to decide?')
    y -= 4
    y = sh(c, 14, y, 'Voting Methods Comparison', sz=9.5)
    y = tbl(c, 14, y,
        [['Method', 'Rule', 'Pros / Cons'],
         ['Plurality', 'Most 1st-place votes wins', 'Simple; ignores lower prefs'],
         ['Borda Count', 'Points: m-1 for 1st, m-2 for 2nd…', 'Considers full ranking'],
         ['Condorcet', 'Wins pairwise vs all others', 'Fair; may not exist'],
         ['Veto', 'Eliminate least-liked alternatives', 'Prevents worst outcomes']],
        [65, 175, W - 65 - 175 - 28], rh=13)
    y -= 4
    y = sh(c, 14, y, 'Borda Count Worked Example', sz=9)
    y = tbl_highlight(c, 14, y,
        [['Alt', 'V1 (2,1,0)', 'V2 (2,1,0)', 'V3 (2,1,0)', 'Total'],
         ['A', '2 (1st)', '0 (3rd)', '2 (1st)', '4'],
         ['B', '1 (2nd)', '1 (2nd)', '1 (2nd)', '3'],
         ['C', '0 (3rd)', '2 (1st)', '0 (3rd)', '2'],
         ['Winner', 'A wins with 4 pts', '', '', '']],
        [40, 90, 90, 90, 60], hi_rows=(1, 4), rh=12)
    box(c, 14, y - 2, W-28,
        ["Arrow's Impossibility: no voting system satisfies ALL fairness axioms simultaneously"],
        RT, RED, '⚠ Theorem')


def s_formulas(c, y0, pn):
    chrome(c, y0, 'EC3 Key Formulas Reference', pn, 'EC3')
    _, yb, _, yt = cb(y0)
    y = yt - 2
    y = sh(c, 14, y, 'Logic & KB')
    y = bul(c, 14, y, 'Resolution: {P∨Q} ∧ {¬P∨R} → {Q∨R}  |  Empty clause □ = proved')
    y = bul(c, 14, y, 'CNF: Elim ↔ → Elim → → Move ¬ inward → Distribute ∨ over ∧')
    y -= 4
    y = sh(c, 14, y, 'Bayesian Networks', sz=9.5)
    y = bul(c, 14, y, 'Joint: P(X1…Xn) = ∏ P(Xi|Parents(Xi))')
    y = bul(c, 14, y, 'Inference: P(X|e) = α · Σ_{hidden} P(X, e, hidden)')
    y -= 4
    y = sh(c, 14, y, 'HMM Algorithms', sz=9.5)
    y = tbl(c, 14, y,
        [['Algorithm', 'Formula', 'Use'],
         ['FPA (Filter)', 'α_t(j) = b_j(Ot) · Σ_i [α_t-1(i)·a_ij]', 'P(current state | obs)'],
         ['Viterbi', 'δ_t(j) = max_i [δ_t-1(i)·a_ij] · b_j(Ot)', 'Best state sequence']],
        [85, 200, W - 85 - 200 - 28], rh=13)
    y -= 4
    y = sh(c, 14, y, 'Game Theory', sz=9.5)
    y = bul(c, 14, y, 'Nash Eq: (s*,t*) where u1(s*,t*)≥u1(s,t*) ∀s AND u2(s*,t*)≥u2(s*,t) ∀t')
    y = bul(c, 14, y, 'Shapley: φi = Σ_S [|S|!(n-|S|-1)!/n!] · [v(S∪i)−v(S)]')
    box(c, 14, y - 2, W-28,
        ['Borda score for m alternatives: 1st place = m-1 pts, 2nd = m-2, …, last = 0'],
        GT, GOLD, 'Borda')


def s_exam_tips(c, y0, pn):
    chrome(c, y0, 'EC3 Exam Strategy & High-Value Topics', pn, 'EC3')
    _, yb, _, yt = cb(y0)
    y = yt - 2
    y = sh(c, 14, y, 'EC3 Exam: Open Book — 13 Sep 2026, 1:00 PM')
    y = bul(c, 14, y, 'Covers Modules 1–7 (Modules 1–3 from main ACI portal)', bold=True)
    y = bul(c, 14, y, 'Exclusions: Dynamic Bayesian Networks, Prolog programs')
    y -= 4
    y = sh(c, 14, y, 'Priority Topics by Module', sz=9.5)
    y = tbl(c, 14, y,
        [['Module', 'High-Value Topics', 'Likely Q type'],
         ['M4: Logic', 'CNF conversion, Resolution proof, FOL quantifiers', 'Trace / Prove'],
         ['M5: Games', 'Nash Eq (find + verify), Shapley worked calc, Borda', 'Calculate'],
         ['M6: Prob', 'Viterbi step-by-step, BN CPT inference, FPA', 'Trace / Compute'],
         ['M7: Ethics', 'XAI types: LIME, SHAP, counterfactuals (post-Aug30)', 'Explain']],
        [55, 250, W - 55 - 250 - 28], rh=13)
    y -= 4
    y = sh(c, 14, y, 'Exam Traps to Avoid', sz=9)
    y = bul(c, 14, y, '❌ Forgetting to distribute ∨ over ∧ in CNF step 4')
    y = bul(c, 14, y, '❌ Confusing FPA (sum) with Viterbi (max) in HMM')
    y = bul(c, 14, y, '❌ Using ∀x P(x)∧Q(x) instead of ∀x P(x)→Q(x) in FOL')
    y = bul(c, 14, y, '❌ Missing the normalisation step in BN inference')
    y = bul(c, 14, y, '❌ Forgetting to check ALL orderings in Shapley (n! orderings)')
    box(c, 14, y - 2, W-28,
        ['Open book: prepare a 1-page formula sheet with CNF steps, Viterbi/FPA formulas, Shapley formula'],
        BT, BLUE, '📋 Open Book Tip')


# ─── Main ─────────────────────────────────────────────────────

SLIDES = [
    # pn, func, args
    ( 1, 'cover', {}),
    ( 2, 'module_title', dict(mod_num=4, title='Knowledge Representation & Logic',
        sub='KB Agents  ·  Propositional Logic  ·  CNF  ·  Resolution  ·  FOL  ·  Chaining',
        topics=['Knowledge-Based Agents & Wumpus World (CS9)',
                'Propositional Logic: Syntax, Equivalences, Entailment',
                'CNF Conversion Algorithm (4 steps)',
                'Resolution Proof by Refutation',
                'First-Order Logic: Quantifiers, Predicates',
                'Forward & Backward Chaining (CS10)'])),
    ( 3, 'kb_agents', {}),
    ( 4, 'prop_logic', {}),
    ( 5, 'cnf', {}),
    ( 6, 'resolution', {}),
    ( 7, 'fol', {}),
    ( 8, 'chaining', {}),
    ( 9, 'module_title', dict(mod_num=6, title='Probabilistic Reasoning & HMM',
        sub='Probability  ·  Bayesian Networks  ·  Markov Models  ·  HMM  ·  Viterbi',
        topics=['Probability Fundamentals & Bayes Theorem (CS11)',
                'Bayesian Networks: Structure and CPTs',
                'Inference by Enumeration',
                'Markov Models & Hidden Markov Models',
                'Forward Algorithm (FPA / Filtering)',
                'Viterbi Algorithm (CS12)'])),
    (10, 'prob_fundamentals', {}),
    (11, 'bayes_net', {}),
    (12, 'hmm', {}),
    (13, 'viterbi', {}),
    (14, 'fpa', {}),
    (15, 'module_title', dict(mod_num=5, title='Multi-Agent Decision Making',
        sub='Game Theory  ·  Nash Equilibrium  ·  Cooperative Games  ·  Shapley Value',
        topics=['Multi-Agent Environments & Normal-Form Games (CS14)',
                'Payoff Matrices, Dominant Strategies',
                "Prisoner's Dilemma & Nash Equilibrium",
                'Battle of the Sexes: Multiple Nash Equilibria',
                'IEDS: Iterated Elimination of Dominated Strategies',
                'Cooperative Games & Shapley Value',
                'Collective Decision Making: Borda, Condorcet, Veto'])),
    (16, 'multiagent_intro', {}),
    (17, 'payoff_nash', {}),
    (18, 'ieds_shapley', {}),
    (19, 'collective', {}),
    (20, 'formulas', {}),
    (21, 'exam_tips', {}),
]

SLIDE_FUNCS = {
    'cover':            slide_cover,
    'module_title':     s_module_title,
    'kb_agents':        s_kb_agents,
    'prop_logic':       s_prop_logic,
    'cnf':              s_cnf,
    'resolution':       s_resolution,
    'fol':              s_fol,
    'chaining':         s_chaining,
    'prob_fundamentals':s_prob_fundamentals,
    'bayes_net':        s_bayes_net,
    'hmm':             s_hmm,
    'viterbi':          s_viterbi,
    'fpa':             s_fpa,
    'multiagent_intro': s_multiagent_intro,
    'payoff_nash':      s_payoff_nash,
    'ieds_shapley':     s_ieds_shapley,
    'collective':       s_collective,
    'formulas':         s_formulas,
    'exam_tips':        s_exam_tips,
}


def generate():
    c = rl_canvas.Canvas(OUT_FILE, pagesize=A4)
    c.setTitle('ACI EC3 Study Notes — S1-2026-27')
    c.setAuthor('BITS Pilani WILP')
    c.setSubject('Advanced Computing for AI — Comprehensive Exam Modules 4,5,6')

    n = len(SLIDES)
    for idx in range(0, n, 2):
        # Top slide = SLIDES[idx], bottom = SLIDES[idx+1]
        for pos, si in enumerate([idx, idx + 1]):
            if si >= n:
                break
            pn, func_name, kwargs = SLIDES[si]
            y0 = SH if pos == 0 else 0   # top half or bottom half
            fn = SLIDE_FUNCS[func_name]
            if func_name == 'cover':
                slide_cover(c, y0, pn)
            elif func_name == 'module_title':
                s_module_title(c, y0, pn, **kwargs)
            else:
                fn(c, y0, pn, **kwargs)
        c.showPage()

    c.save()
    print(f'✅  Generated: {OUT_FILE}')
    print(f'   {n} slides  →  {math.ceil(n/2)} pages')


if __name__ == '__main__':
    generate()
