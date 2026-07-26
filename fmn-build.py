#!/usr/bin/env python3
"""Build the deployable single-file Family Movie Night app.

The source is split into fmn/*.js so edits stay surgical, but the deployed
artifact is one self-contained index.html — no extra requests, nothing that
can go stale against a cached shell, and a single file to back up.

    python3 fmn-build.py [OUT_DIR]

Defaults to /workspace/family-movie-night. Also rewrites the manifest and
icon filenames to their deployed names.
"""
import re
import sys
import pathlib

SRC = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/workspace/family-movie-night')

html = (SRC / 'family-movie-night.html').read_text()

# the script tags, in the order the browser would have loaded them
tags = re.findall(r'<script src="(fmn/[\w.]+\.js)(?:\?v=\d+)?"></script>', html)
if not tags:
    sys.exit('no fmn/*.js script tags found — has the shell changed?')

parts = []
for rel in tags:
    body = (SRC / rel).read_text().rstrip('\n')
    parts.append('/* ===== %s ===== */\n%s' % (rel, body))
bundle = '<script>\n' + '\n\n'.join(parts) + '\n</script>'

# replace the whole run of script tags (plus the comment above them) with the bundle
block = re.search(
    r'(?:<!--[^\n]*-->\n)?(?:<script src="fmn/[\w.]+\.js(?:\?v=\d+)?"></script>\n?)+',
    html)
html = html[:block.start()] + bundle + html[block.end():]

# deployed asset names differ from the dev copy
html = html.replace('family-movie-night.webmanifest', 'manifest.webmanifest')
html = html.replace('fmn-icon.svg', 'icon.svg')

OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'index.html').write_text(html)

lines = html.count('\n') + 1
print('built %s — %d lines, %d scripts inlined' % (OUT / 'index.html', lines, len(tags)))
for t in tags:
    print('  ', t)
