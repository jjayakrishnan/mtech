/**
 * theme-audit.js — Playwright audit for theme.css consistency
 *
 * For every page on the local server:
 *   1. Confirms theme.css is loaded
 *   2. Checks CSS variables resolve from theme.css (not hardcoded)
 *   3. Captures key computed colors (bg, text, navy header, gold accent)
 *   4. Checks dark-mode toggle exists and works
 *   5. Flags hardcoded color properties that bypass CSS variables
 *   6. Checks structural template elements (header, sidebar/nav, footer-nav)
 *
 * Output: JSON array of findings to stdout, summary to stderr.
 */

const { chromium } = require('/Users/jayakrishnanj/.npm/_npx/e41f203b7505f1fb/node_modules/playwright');

const BASE = 'http://localhost:3000';

// All pages to audit (relative to BASE)
const PAGES = [
  '/',
  '/viewer',
  '/study-plans/aci',
  '/study-plans/drl',
  '/study-plans/nlp',
  '/study-plans/seml',
  '/semester2/ACI/',
  '/semester2/DRL/',
  '/semester2/NLP/',
  '/semester2/SEML/',
  '/semester2/ACI/0001-agents-peas-environments',
  '/semester2/ACI/0002-search-algorithms',
  '/semester2/ACI/0003-heuristics',
  '/semester2/ACI/0004-local-search',
  '/semester2/ACI/0005-evolutionary-algorithms',
  '/semester2/ACI/0006-neat-nas',
  '/semester2/ACI/0007-adversarial-search',
  '/semester2/ACI/0008-alpha-beta-mcts',
  '/semester2/ACI/exam-study-guide',
  '/semester2/ACI/exercise-bank',
  '/semester2/DRL/0001-rl-framework',
  '/semester2/DRL/0002-mab-vs-mdp',
  '/semester2/DRL/0003-value-iteration',
  '/semester2/DRL/0004-mab-action-value-methods',
  '/semester2/DRL/0005-incremental-updates-ucb',
  '/semester2/DRL/0006-finite-mdp',
  '/semester2/DRL/0007-bellman-equations',
  '/semester2/DRL/0008-dynamic-programming',
  '/semester2/DRL/0009-monte-carlo-methods',
  '/semester2/DRL/DRL-exam-study-guide',
  '/semester2/DRL/try-it-yourself',
  '/semester2/NLP/0001-intro-preprocessing',
  '/semester2/NLP/0002-language-models-ngrams',
  '/semester2/NLP/0003-vector-semantics',
  '/semester2/NLP/0004-word2vec-embeddings',
  '/semester2/NLP/0005-neural-language-models',
  '/semester2/NLP/0006-pos-tagging-hmm',
  '/semester2/NLP/NLP-exam-study-guide',
  '/semester2/SEML/',
  '/semester2/SEML/session1-foundations/lecture',
  '/semester2/SEML/session2-ml-production/lecture',
  '/semester2/SEML/session3-requirements/lecture',
  '/semester2/SEML/session4-architecture/lecture',
  '/semester2/SEML/session5-patterns/lecture',
  '/semester2/SEML/session6-design-patterns/lecture',
  '/semester2/SEML/session7-agentic-ai/lecture',
];

// Expected light-mode computed colors from theme.css
const EXPECTED = {
  bodyBg: 'rgb(250, 250, 248)',   // #fafaf8
  bodyText: 'rgb(26, 26, 26)',    // #1a1a1a  (some files use #222/#2c2c2c — flag those)
  navyBg: 'rgb(26, 39, 68)',      // #1a2744
};

// Exam guide pages intentionally keep their own :root palette — skip variable audits
const EXAM_GUIDES = new Set([
  '/semester2/ACI/exam-study-guide',
  '/semester2/DRL/DRL-exam-study-guide',
  '/semester2/NLP/NLP-exam-study-guide',
  '/semester2/DRL/exam-study-guide',
  '/semester2/NLP/exam-study-guide',
]);

async function auditPage(page, url) {
  const issues = [];
  const fullUrl = BASE + url;
  const isExamGuide = EXAM_GUIDES.has(url);

  try {
    await page.goto(fullUrl, { waitUntil: 'domcontentloaded', timeout: 15000 });
  } catch (e) {
    return [{ url, severity: 'error', type: 'load_failed', detail: e.message }];
  }

  // 1. theme.css linked?
  const hasThemeLink = await page.evaluate(() => {
    return [...document.querySelectorAll('link[rel="stylesheet"]')]
      .some(l => l.href.includes('theme.css'));
  });
  if (!hasThemeLink) {
    issues.push({ url, severity: 'critical', type: 'no_theme_link', detail: 'theme.css not linked' });
  }

  // 2. Inline :root redefining color tokens (should only have layout tokens)
  const inlineRootVars = await page.evaluate(() => {
    const colorTokens = ['--bg','--surface','--navy','--gold','--green','--accent',
      '--text','--text-muted','--border','--card-bg','--tag-bg'];
    const styles = [...document.querySelectorAll('style')];
    const found = [];
    for (const s of styles) {
      const text = s.textContent;
      const rootMatch = text.match(/:root\s*\{([^}]*)\}/s);
      if (rootMatch) {
        const block = rootMatch[1];
        for (const token of colorTokens) {
          if (block.includes(token + ':') || block.includes(token + ' :')) {
            found.push(token);
          }
        }
      }
    }
    return found;
  });
  if (!isExamGuide && inlineRootVars.length > 0) {
    issues.push({ url, severity: 'high', type: 'inline_root_color_tokens',
      detail: `Inline :root still defines color tokens: ${inlineRootVars.join(', ')}` });
  }

  // 3. Body background color — should be #fafaf8
  const bodyBg = await page.evaluate(() =>
    getComputedStyle(document.body).backgroundColor);
  if (!isExamGuide && bodyBg !== EXPECTED.bodyBg) {
    issues.push({ url, severity: 'medium', type: 'body_bg_mismatch',
      detail: `body bg = ${bodyBg}, expected ${EXPECTED.bodyBg}` });
  }

  // 4. Header element (look for .hdr or header or nav with dark navy bg)
  const headerBg = await page.evaluate(() => {
    const hdr = document.querySelector('.hdr, .header, header, [class*=hdr], [class*=header]');
    if (!hdr) return null;
    return getComputedStyle(hdr).backgroundColor;
  });
  if (!isExamGuide && headerBg && headerBg !== 'rgba(0, 0, 0, 0)' && headerBg !== EXPECTED.navyBg) {
    // Only flag if it's clearly not navy
    const isNavyish = headerBg.includes('26, 39') || headerBg.includes('15, 26') ||
                      headerBg.includes('30, 58') || headerBg.includes('33, 53');
    if (!isNavyish) {
      issues.push({ url, severity: 'medium', type: 'header_bg_not_navy',
        detail: `header bg = ${headerBg}` });
    }
  }

  // 5. Dark mode toggle present?
  const hasToggle = await page.evaluate(() => {
    return !!(document.querySelector('.theme-toggle') ||
              document.querySelector('[onclick*="toggleTheme"]') ||
              document.querySelector('[onclick*="toggle"]'));
  });
  if (!isExamGuide && !hasToggle) {
    issues.push({ url, severity: 'medium', type: 'no_dark_toggle',
      detail: 'No dark mode toggle button found' });
  }

  // 6. Dark mode works — set data-theme=dark, wait for transition, check bg changed
  if (!isExamGuide && (hasToggle || hasThemeLink)) {
    await page.evaluate(() => document.documentElement.setAttribute('data-theme', 'dark'));
    await page.waitForTimeout(500); // wait for CSS transitions to complete
    const darkBg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
    // Reset to light
    await page.evaluate(() => document.documentElement.setAttribute('data-theme', 'light'));
    if (darkBg === EXPECTED.bodyBg || darkBg === 'rgb(255, 255, 255)') {
      issues.push({ url, severity: 'high', type: 'dark_mode_broken',
        detail: `Setting data-theme=dark did not change body bg (still ${darkBg})` });
    }
  }

  // 7. Template structure check — lesson pages should have .hdr + sidebar + main
  const isLesson = url.match(/\/0\d{3}-|\/lecture$/);
  if (isLesson) {
    const structure = await page.evaluate(() => ({
      hasHdr: !!document.querySelector('.hdr, .header, header, #header, #toolbar, [id*=header]'),
      hasSidebar: !!document.querySelector('nav.sidebar, nav.sb, .sidebar, aside, #sbNav, #sidebar, nav[id]'),
      hasMain: !!document.querySelector('main, .main, #main, .content, .wrap > *:last-child'),
      hasNextPrev: !!document.querySelector('.nextnav, .prev-next, .lesson-nav, .hdr .nav, .nav-footer, [class*=nav] a[href*="000"], footer a[href*=".html"]') || document.querySelectorAll('a[href*=".html"]').length > 3,
    }));
    if (!structure.hasHdr)
      issues.push({ url, severity: 'medium', type: 'missing_hdr', detail: 'No .hdr element' });
    if (!structure.hasSidebar)
      issues.push({ url, severity: 'medium', type: 'missing_sidebar', detail: 'No sidebar/nav element' });
    if (!structure.hasMain)
      issues.push({ url, severity: 'low', type: 'missing_main', detail: 'No main content element' });
    if (!structure.hasNextPrev)
      issues.push({ url, severity: 'low', type: 'missing_nextnav', detail: 'No prev/next lesson nav' });
  }

  // 8. Check for hardcoded bgcolor in style attributes (inline styles)
  const inlineColorCount = await page.evaluate(() => {
    const all = document.querySelectorAll('[style*="background"], [style*="color"]');
    return all.length;
  });
  if (inlineColorCount > 50) {
    issues.push({ url, severity: 'low', type: 'many_inline_styles',
      detail: `${inlineColorCount} elements with inline color/bg styles` });
  }

  return issues;
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  page.setViewportSize({ width: 1280, height: 800 });

  const allIssues = [];
  const seen = new Set();

  for (const url of PAGES) {
    if (seen.has(url)) continue;
    seen.add(url);
    const issues = await auditPage(page, url);
    allIssues.push(...issues);
    const marker = issues.length === 0 ? '✓' :
      issues.some(i => i.severity === 'critical') ? '✗' :
      issues.some(i => i.severity === 'high') ? '⚠' : '~';
    process.stderr.write(`${marker} ${url}  (${issues.length} issues)\n`);
  }

  await browser.close();

  // Print JSON results
  process.stdout.write(JSON.stringify(allIssues, null, 2) + '\n');

  // Summary
  const bySeverity = { critical: 0, high: 0, medium: 0, low: 0 };
  for (const i of allIssues) bySeverity[i.severity] = (bySeverity[i.severity] || 0) + 1;
  process.stderr.write(`\nSummary: ${allIssues.length} issues — ` +
    `critical:${bySeverity.critical} high:${bySeverity.high} ` +
    `medium:${bySeverity.medium} low:${bySeverity.low}\n`);
})();
