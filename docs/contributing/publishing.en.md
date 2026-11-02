---
title: Maintain and publish the documentation
translation_of: contributing/publishing.md
---

# Maintain and publish the documentation

## Local preview

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-docs.txt
python scripts/check_docs.py
python scripts/check_release_baseline.py
mkdocs build --strict
mkdocs serve
```

`mkdocs.yml` configures navigation, themes, search, and languages. Edit Markdown under `docs/`, not generated `site/` output.

## GitHub Pages

1. Select **GitHub Actions** as the source in Settings → Pages.
2. Submit changes in a PR. The Documentation workflow checks links and performs a strict build.
3. Merges to `main` build/upload the Pages artifact and deploy it to `github-pages`.
4. Inspect Actions and use the URL returned by deployment.

Default URL: [fullon-labs.github.io/fullon-kb](https://fullon-labs.github.io/fullon-kb/). Deployment results establish whether publication succeeded.

## Directories

- `01_Core_Chain/`: concepts and specifications.
- `06_User_Guides/`: end-user tasks.
- `10_Developer_Guides/`: development tutorials and node introduction.
- `03_Operators/`: detailed RPC/node reference, preserving existing links.
- `04_FAQ/`: short answers and official FAQ integration.
- `contributing/`: maintenance, verification, and publishing.

Update navigation and related pages when adding content. Explicitly mark unverified parameters rather than guessing.

## Translations

Chinese uses existing `.md` files; English uses matching `.en.md` files in the same directory. Link to canonical `.md` paths in both languages; the build resolves them to the reader's language. Keep code, request fields, source revisions, and verification scope aligned. Run the bilingual coverage and rendered-site checks before publishing.
