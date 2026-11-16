# Building the site

The pages share one header, menu and footer, so they are generated rather than edited one by one.

- `source-index.html` holds the approved wording for every section (it was the single-page homepage).
- `build_site.py` cuts those sections into separate pages and wraps each in the shared header and footer.

To change wording, edit `source-index.html` (or the small pages inside `build_site.py`), then run from the repo root:

    python3 tools/build_site.py tools/source-index.html .

Keep the site free of inline `<script>`, `style=""` and third-party files: Cloudflare sends a strict
Content-Security-Policy and Cross-Origin-Embedder-Policy, and anything inline or external is blocked.
