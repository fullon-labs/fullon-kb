"""Keep Material search within the reader's selected language."""
import json
from html import escape
import os
from pathlib import Path
import re

from mkdocs.plugins import event_priority


@event_priority(-200)
def on_post_page(output, page, config):
    # Relative destinations preserve the locale and GitHub Pages project prefix.
    if destination := page.meta.get('redirect_to'):
        destination = escape(destination, quote=True)
        output = re.sub(r'<link[^>]+rel="canonical"[^>]*>', '', output)
        redirect = (f'<meta http-equiv="refresh" content="0; url={destination}">'
                    f'<link rel="canonical" href="{destination}">'
                    '<meta name="robots" content="noindex">')
        output = output.replace('</head>', redirect + '</head>', 1)
    if config.plugins['i18n'].current_language != 'en':
        return output
    # Material loads search/search_index.json relative to __config.base.
    # Keep its worker URL unchanged, but make English use the English index.
    pattern = r'(<script id="__config"[^>]*>)(.*?)(</script>)'
    def localize(match):
        settings = json.loads(match.group(2))
        settings['base'] = os.path.relpath('en', Path(page.file.dest_uri).parent).replace(os.sep, '/')
        return match.group(1) + json.dumps(settings, ensure_ascii=True) + match.group(3)
    return re.sub(pattern, localize, output, count=1, flags=re.S)


@event_priority(-200)
def on_post_build(config):
    # The i18n plugin recursively builds both locales and finally merges search.
    # Run once after that outer build, not after its nested English build.
    if config.plugins['i18n'].building:
        return
    site = Path(config.site_dir)
    index = site / 'search/search_index.json'
    data = json.loads(index.read_text())
    english = dict(data)
    english['config'] = dict(data['config'], lang=['en'])
    english['docs'] = [dict(item, location=item['location'][3:])
                       for item in data['docs'] if item['location'].startswith('en/')]
    chinese = dict(data)
    chinese['docs'] = [item for item in data['docs'] if not item['location'].startswith('en/')]
    index.write_text(json.dumps(chinese, ensure_ascii=False))
    target = site / 'en/search/search_index.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(english, ensure_ascii=False))
