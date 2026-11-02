"""Validate language coverage, unchanged examples, switch links, assets and search."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

import yaml

root = Path(__file__).resolve().parents[1]
docs, site = root / 'docs', root / 'site'
errors = []
source_pages = [p for p in docs.rglob('*.md')
                if not p.name.endswith('.en.md') and 'template' not in p.name]
for source in source_pages:
    english = source.with_name(source.stem + '.en.md')
    if not english.exists():
        errors.append(f'Missing English page: {source.relative_to(docs)}')
        continue
    a, b = source.read_text(), english.read_text()
    if re.findall(r'```.*?```', a, re.S) != re.findall(r'```.*?```', b, re.S):
        errors.append(f'Code examples differ: {source.relative_to(docs)}')
    if re.search(r'[\u4e00-\u9fff]', re.sub(r'```.*?```', '', b, flags=re.S)):
        errors.append(f'Untranslated English prose: {english.relative_to(docs)}')
    ma = yaml.safe_load(a.split('---', 2)[1]) if a.startswith('---') else {}
    mb = yaml.safe_load(b.split('---', 2)[1]) if b.startswith('---') else {}
    if ma.get('updated') != mb.get('updated'):
        errors.append(f'Verification dates differ: {source.relative_to(docs)}')
    if source.parent.name == '03_Operators':
        paths = lambda text: set(re.findall(r'/v1/[a-z_]+/[a-z_0-9]+', text))
        if paths(a) != paths(b):
            errors.append(f'RPC route coverage differs: {source.name}')


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path, self.language, self.switches = path, None, {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.language = attrs.get('lang')
        if tag == 'a' and 'hreflang' in attrs:
            self.switches[attrs['hreflang']] = attrs['href']
        for key in ('href', 'src'):
            value = attrs.get(key)
            if not value:
                continue
            url = urlsplit(value)
            if url.scheme or url.netloc or not url.path or url.path.startswith('/'):
                continue
            target = (self.path.parent / unquote(url.path)).resolve()
            if not target.is_relative_to(site.resolve()) or not target.exists():
                errors.append(f'Missing rendered asset/link: {self.path.relative_to(site)} -> {value}')


pages = list(site.rglob('*.html'))
for path in pages:
    if path.name == '404.html':
        continue
    page = Page(path)
    text = path.read_text()
    page.feed(text)
    relative = path.relative_to(site).as_posix()
    is_english = relative.startswith('en/')
    if page.language != ('en' if is_english else 'zh'):
        errors.append(f'Wrong HTML language: {relative}')
    canonical = relative[3:] if is_english else relative
    for language, target in [('zh', canonical), ('en', 'en/' + canonical)]:
        href = page.switches.get(language)
        if href is None:
            errors.append(f'Missing {language} switch: {relative}')
            continue
        switch_path = unquote(urlsplit(href).path)
        if switch_path.startswith('/'):
            prefix = urlsplit(yaml.safe_load((root / 'mkdocs.yml').read_text())['site_url']).path
            result = (site / switch_path.removeprefix(prefix)).resolve()
        else:
            result = (path.parent / switch_path).resolve()
        if result.is_dir():
            result /= 'index.html'
        if result != (site / target).resolve():
            errors.append(f'Switch loses current page: {relative} -> {href}')
    config_match = re.search(r'<script id="__config"[^>]*>(.*?)</script>', text, re.S)
    settings = json.loads(config_match[1])
    expected_root = site / ('en' if is_english else '')
    if (path.parent / settings['base']).resolve() != expected_root.resolve():
        errors.append(f'Wrong search base: {relative}')

for lang, index_path, locale_root in [
    ('zh', site / 'search/search_index.json', site),
    ('en', site / 'en/search/search_index.json', site / 'en'),
]:
    index = json.loads(index_path.read_text())
    if not index['docs']:
        errors.append(f'Empty {lang} search index')
    for entry in index['docs']:
        location = unquote(urlsplit(entry['location']).path)
        if location.startswith('en/'):
            errors.append(f'Cross-language search entry in {lang}: {location}')
        target = locale_root / location
        if target.is_dir():
            target /= 'index.html'
        if not target.exists():
            errors.append(f'Broken {lang} search entry: {location}')
    if lang == 'en' and any(re.search(r'[\u4e00-\u9fff]', e['title']) for e in index['docs']):
        errors.append('Chinese titles leaked into English search')

print(f'Checked {len(source_pages)} translation pairs and {len(pages)} rendered HTML files.')
for error in errors:
    print(error)
if errors:
    raise SystemExit(1)
print('PASS: language coverage, code/RPC parity, current-page switches, assets, and locale search')
