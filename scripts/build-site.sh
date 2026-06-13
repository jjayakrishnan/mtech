#!/bin/bash
set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITE="$REPO_ROOT/site"

echo "Building site from lessons..."

# DRL lessons
rm -rf "$SITE/semester2/DRL/0"*.html
cp "$REPO_ROOT/semester2/DRL/lessons/"*.html "$SITE/semester2/DRL/"
echo "  DRL: $(ls "$SITE/semester2/DRL/"0*.html 2>/dev/null | wc -l | tr -d ' ') lessons"

# SEML lessons (has subdirectories)
rm -rf "$SITE/semester2/SEML"
mkdir -p "$SITE/semester2/SEML"
cp -R "$REPO_ROOT/semester2/SEML/lessons/"* "$SITE/semester2/SEML/"
echo "  SEML: copied"

echo "Done. Site ready at: $SITE"
echo "Run 'vercel' or push to deploy."
