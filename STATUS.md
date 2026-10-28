# STATUS

## What was built

A beginner manual and static HTML site on low-energy and ADHD-friendly daily routines, created and published by **Asdale Dynamics, LLC** (Indiana, formed October 2026). No build step, no dependencies, no secrets, no personal data. Local-first: open `site/index.html` in any browser.

**Contents**
- `LICENSE` — MIT License, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC`
- `README.md` — project overview with table of contents, usage, golden rules, credit, license
- `verify.py` — automated verification script (HTML structure, internal links, license/credit, no workflows, no secrets)
- `docs/` — beginner manual in Markdown:
  - `00-read-me-first.md` — welcome, who it's for, golden rules
  - `01-one-task-at-a-time.md` — picking one task at a time
  - `02-gentle-schedules.md` — gentle, bendable schedules with sample day
  - `03-rest-without-guilt.md` — rest as part of the routine
  - `04-energy-tracking.md` — 1–5 energy scale and tracking sheet
  - `05-low-energy-task-list.md` — tiny self-care, home, movement, rest tasks
  - `06-printable-routine-cards.md` — card text and printing instructions
- `site/` — static HTML version, open in any browser or host anywhere:
  - `site/index.html` — full guide with all sections, navigation, interactive energy tracker
  - `site/cards.html` — printable routine cards (One Task Today, Gentle Schedule, Energy Tracker, Rest Permission, Low-Energy Tasks, Notes) with print CSS
  - `site/style.css` — shared warm, soft design
  - `site/script.js` — energy-tracker suggestions and reduced-motion-safe page reveals

## How to run it

Open `site/index.html` in any web browser. No server, no install, no internet needed.

Optional local preview:
```
cd site
python3 -m http.server 8000
# then open http://localhost:8000
```

To print the routine cards, open `site/cards.html`, press Ctrl+P (Cmd+P), enable background graphics, and cut along the card borders.

Run verification:
```
python3 verify.py
```

## Verification results

- `python3 verify.py`: PASSED — all checks ok
- HTML parse check (Python html.parser): `site/index.html` OK, `site/cards.html` OK — no unclosed or mismatched tags
- Internal links: all anchors (`#one-task`, `#gentle-schedules`, `#rest`, `#energy`, `#task-list`) and files (`style.css`, `script.js`, `cards.html`, `../LICENSE`, `index.html`) resolve
- Local serve test: `python3 -m http.server 18766` returned HTTP 200 for `/`, `/cards.html`, `/style.css`, `/script.js`; server stopped after test
- Copyright line `Copyright (c) 2026 Asdale Dynamics, LLC` present in `LICENSE` exactly; Asdale Dynamics, LLC credited in `README.md`, `site/index.html`, `site/cards.html`, and every `docs/` file
- No `.github/workflows` files; no secrets, API keys, or personal data in any file
- Git: initialized, committed as Dylan Asdale <dylanasdale@users.noreply.github.com>, plain commit messages, no co-author trailers, not pushed, no remote created

## Bugs fixed in this review

- `site/script.js`: previously set reveal elements to `opacity: 0` and relied on IntersectionObserver to show them. If IntersectionObserver was unavailable, content stayed invisible. Fixed so elements stay visible by default and the reveal class is only added when IntersectionObserver is available.
- `verify.py`: anchor-link regex required a word boundary after the closing quote, which never matched. Fixed to match `id="target"` directly.

## Known gaps

- The manual exists in both Markdown (`docs/`) and HTML (`site/index.html`); if one is edited, the other may drift. No automated sync.
- `site/script.js` energy tracker is a simple average suggestion, not medical advice (stated in guide).
- Print layout tested via browser print CSS only; physical printer output not verified in this environment.
- No search, dark mode, or multi-language support — intentionally out of scope for this beginner-first release.
