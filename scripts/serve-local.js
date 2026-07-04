#!/usr/bin/env node
// Local dev server for site/ — mirrors Vercel cleanUrls + trailingSlash:false
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = parseInt(process.argv[2] || '3000', 10);
const SITE = path.resolve(__dirname, '../site');

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css':  'text/css',
  '.js':   'text/javascript',
  '.json': 'application/json',
  '.pdf':  'application/pdf',
  '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg':  'image/svg+xml',
  '.ico':  'image/x-icon',
  '.woff2':'font/woff2',
  '.woff': 'font/woff',
  '.ttf':  'font/ttf',
};

function resolve(urlPath) {
  // Strip query string and decode
  const clean = decodeURIComponent(urlPath.split('?')[0]);
  const base = path.join(SITE, clean);

  // 1. Exact file
  if (fs.existsSync(base) && fs.statSync(base).isFile()) return base;
  // 2. cleanUrls: append .html
  const html = base + '.html';
  if (fs.existsSync(html)) return html;
  // 3. Directory index
  const idx = path.join(base, 'index.html');
  if (fs.existsSync(idx)) return idx;

  return null;
}

const server = http.createServer((req, res) => {
  const filePath = resolve(req.url);

  if (!filePath) {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('404 Not Found: ' + req.url);
    console.log('404', req.url);
    return;
  }

  const ext = path.extname(filePath).toLowerCase();
  const mime = MIME[ext] || 'application/octet-stream';

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(500, { 'Content-Type': 'text/plain' });
      res.end('500 Read error');
      return;
    }
    res.writeHead(200, { 'Content-Type': mime });
    res.end(data);
    console.log('200', req.url, '->', path.relative(SITE, filePath));
  });
});

server.listen(PORT, () => {
  console.log(`\nJK Learn — local server`);
  console.log(`  Serving: ${SITE}`);
  console.log(`  Open:    http://localhost:${PORT}\n`);
  console.log('Ctrl+C to stop.\n');
});
