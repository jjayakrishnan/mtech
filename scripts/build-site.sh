#!/bin/bash
set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITE="$REPO_ROOT/site"

echo "Building site from lessons..."

# DRL lessons + handouts
rm -rf "$SITE/semester2/DRL/0"*.html
cp "$REPO_ROOT/semester2/DRL/lessons/"*.html "$SITE/semester2/DRL/" 2>/dev/null || true
mkdir -p "$SITE/semester2/DRL/handouts"
cp "$REPO_ROOT/semester2/DRL/lessons/handouts/"*.pdf "$SITE/semester2/DRL/handouts/" 2>/dev/null || true
echo "  DRL: $(ls "$SITE/semester2/DRL/"0*.html 2>/dev/null | wc -l | tr -d ' ') lessons, $(ls "$SITE/semester2/DRL/handouts/"*.pdf 2>/dev/null | wc -l | tr -d ' ') handout PDFs"

# ACI lessons
rm -rf "$SITE/semester2/ACI"
mkdir -p "$SITE/semester2/ACI"
cp "$REPO_ROOT/semester2/ACI/lessons/"*.html "$SITE/semester2/ACI/"
echo "  ACI: $(ls "$SITE/semester2/ACI/"0*.html 2>/dev/null | wc -l | tr -d ' ') lessons"

# NLP lessons + handouts
rm -rf "$SITE/semester2/NLP"
mkdir -p "$SITE/semester2/NLP/handouts"
cp "$REPO_ROOT/semester2/NLP/lessons/"*.html "$SITE/semester2/NLP/" 2>/dev/null || true
cp "$REPO_ROOT/semester2/NLP/lessons/handouts/"*.html "$SITE/semester2/NLP/handouts/" 2>/dev/null || true
cp "$REPO_ROOT/semester2/NLP/lessons/handouts/"*.pdf "$SITE/semester2/NLP/handouts/" 2>/dev/null || true
echo "  NLP: $(ls "$SITE/semester2/NLP/"0*.html 2>/dev/null | wc -l | tr -d ' ') lessons, $(ls "$SITE/semester2/NLP/handouts/"*.pdf 2>/dev/null | wc -l | tr -d ' ') handout PDFs"

# SEML lessons (has subdirectories) — copy HTML + PDF, exclude .tex and LaTeX artifacts
rm -rf "$SITE/semester2/SEML"
mkdir -p "$SITE/semester2/SEML"
cp "$REPO_ROOT/semester2/SEML/lessons/index.html" "$SITE/semester2/SEML/"
for session in "$REPO_ROOT/semester2/SEML/lessons"/session*/; do
  name=$(basename "$session")
  mkdir -p "$SITE/semester2/SEML/$name"
  cp "$session"*.html "$SITE/semester2/SEML/$name/" 2>/dev/null || true
  cp "$session"*.pdf "$SITE/semester2/SEML/$name/" 2>/dev/null || true
done
echo "  SEML: $(ls -d "$SITE/semester2/SEML"/session*/ 2>/dev/null | wc -l | tr -d ' ') sessions"

echo "Done. Site ready at: $SITE"
echo "Run 'vercel' or push to deploy."
