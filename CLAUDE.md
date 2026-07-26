# screening-room

Two apps live in this repo:

- **Screening Room** — `index.html`, Chris's movie-tracking app
- **Family Movie Night** — `family-movie-night.html` + `fmn/*.js`, the Ortiz
  family's Friday-night memory book. **Read `FAMILY-MOVIE-NIGHT.md` before
  touching it** — architecture, data model, and the specific bugs that have
  recurred.

The `family-app-standards` skill governs all work here. Load it before
building, fixing, or deploying anything.

## Non-negotiables

- Single-file deliverable, inline CSS/JS, no build step, no framework, no npm.
  Family Movie Night splits its source into `fmn/*.js` for maintainability, but
  `fmn-build.py` inlines them back into one file for deploy.
- All DOM via `createElement`/`appendChild`, all events via `addEventListener`.
  Never `onclick=` attributes, never `innerHTML` with user data.
- Never `alert()`, `confirm()`, or `prompt()` — they behave badly in mobile
  Safari. Use the app's own modal.
- Mobile Safari is the primary target: 44px minimum tap targets, no
  hover-dependent UI, test at 390px.
- All dates through the Arizona helpers (`AZ.today()`, `AZ.addDays`, …). Never
  `toISOString().split('T')[0]` for "today" — it drifts to UTC.
- localStorage is the source of truth; Gist sync uses safe merge with
  tombstones. Never blind-overwrite on save.
- Secrets (Gist token, API keys) live in localStorage, entered via the
  Settings UI. **Never** hardcode one — these repos are public.

## Workflow

1. Restate scope and get approval before writing code.
2. Make surgical, section-scoped edits. Never rewrite a working file to change
   one feature.
3. Run the smoke test
   (`~/.claude/skills/family-app-standards/references/smoke-test.md`) before
   calling anything done — including the hygiene greps.
4. Test the **built** file, not just the source.
5. Ask before deploying. Never push to Pages without explicit go-ahead.

## Deploying Family Movie Night

```bash
python3 fmn-build.py                 # → ../family-movie-night/index.html
```

Then commit and push in the `ortizzle/family-movie-night` repo (branch `main`).
Pages lags about a minute and mobile Safari caches hard — verify with a
cache-busting query string.

## The family

Chris and Kat (parents), Sedona (12), River (9). Movie night is Friday. Picks
rotate Chris → Kat → Sedona → River. Arizona, so `America/Phoenix`, no DST.
