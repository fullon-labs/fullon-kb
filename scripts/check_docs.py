"""Check public Markdown links and shell syntax without contacting chain services."""
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
docs = root / 'docs'
errors = []
blocks = 0
files = list(docs.rglob('*.md'))
for page in files:
    text = page.read_text()
    # C++ attributes such as [[eosio::action]] are valid inside code examples.
    prose = re.sub(r'```.*?```', '', text, flags=re.S)
    if '[[' in prose:
        errors.append(f'{page.relative_to(root)}: unsupported wiki link')
    for block in re.findall(r'```(?:cpp|c\+\+)\n(.*?)```', text, re.S):
        if re.search(r'\[eosio::(?:contract|action)\b[^\n]*\]\([^\n]*\.md\)', block):
            errors.append(f'{page.relative_to(root)}: C++ attribute corrupted into a Markdown link')
    for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', prose):
        if '://' in target or target.startswith(('#', 'mailto:')):
            continue
        path = (page.parent / target.split('#')[0]).resolve()
        if not path.is_relative_to(docs.resolve()) or not path.exists():
            errors.append(f'{page.relative_to(root)}: missing/nonpublic link {target}')
    for block in re.findall(r'```(?:bash|sh)\n(.*?)```', text, re.S):
        blocks += 1
        result = subprocess.run(['bash', '-n'], input=block, text=True, capture_output=True)
        if result.returncode:
            errors.append(f'{page.relative_to(root)}: {result.stderr.strip()}')
print(f'Checked {len(files)} public Markdown files and {blocks} shell examples.')
for error in errors:
    print(error, file=sys.stderr)
if errors:
    sys.exit(1)
print('PASS: public relative links and shell syntax')
