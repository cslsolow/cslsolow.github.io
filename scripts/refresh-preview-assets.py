#!/usr/bin/env python3
"""Version local page and asset URLs together so browsers cannot mix releases."""
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
import hashlib
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = ('index.html', 'colors.html')
ASSETS = ('theme-init.js', 'app.js', 'language.js', 'styles.css', 'colors.js', 'colors.css',
          'assets/avatar.png', 'assets/favicon.svg')
TRACKED = set(PAGES + ASSETS)
ATTRIBUTE = re.compile(r'\b(src|href)="([^"]+)"')


def rewrite_urls(source, version=None):
    def replace(match):
        name, original = match.groups()
        url = urlsplit(html.unescape(original))
        if url.scheme or url.netloc or url.path not in TRACKED:
            return match.group(0)
        query = [(key, value) for key, value in parse_qsl(url.query, keep_blank_values=True)
                 if key != 'v']
        if version:
            query.append(('v', version))
        value = urlunsplit((url.scheme, url.netloc, url.path,
                           urlencode(query), url.fragment))
        return f'{name}="{html.escape(value, quote=True)}"'
    return ATTRIBUTE.sub(replace, source)


canonical_pages = {name: rewrite_urls((ROOT / name).read_text()) for name in PAGES}
digest = hashlib.sha256()
for name in sorted(TRACKED):
    content = canonical_pages[name].encode() if name in canonical_pages else (ROOT / name).read_bytes()
    digest.update(name.encode() + b'\0' + content + b'\0')
version = digest.hexdigest()[:12]
for name, source in canonical_pages.items():
    (ROOT / name).write_text(rewrite_urls(source, version))
(ROOT / 'asset-version.json').write_text(json.dumps({
    'version': version,
    'new_colors_url': f'colors.html?set=new&v={version}',
    'homepage_url': f'index.html?v={version}'
}, indent=2) + '\n')
print(version)
