# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Spendly — a Flask expense tracker built as a step-by-step teaching project. Much of the backend is intentionally unimplemented; placeholder routes and stubs are labelled with the step ("Step 3", "Step 7", …) in which they are meant to be filled in.

## Commands

```
python -m venv venv && venv\Scripts\activate   # Windows; venv/ is gitignored
pip install -r requirements.txt
python app.py                                   # dev server on http://localhost:5001 (debug=True)
pytest                                          # pytest + pytest-flask are installed; no tests exist yet
pytest path/to/test_file.py::test_name          # single test
```

## Architecture

```
spendly/
├── app.py
│   └── Single Flask app (port 5001, debug=True)
│       ├── ✓ GET  /              (landing page)
│       ├── ✓ GET  /register       (form)
│       ├── ✓ GET  /login          (form)
│       ├── ✓ GET  /terms          (static page)
│       ├── ✓ GET  /privacy        (static page)
│       ├── ✗ POST /register       (auth stub)
│       ├── ✗ POST /login          (auth stub)
│       ├── ✗ GET  /logout         (placeholder)
│       ├── ✗ GET  /profile        (placeholder)
│       ├── ✗ GET  /expenses/add   (placeholder)
│       ├── ✗ POST /expenses/add   (placeholder)
│       ├── ✗ GET  /expenses/<id>/edit   (placeholder)
│       ├── ✗ POST /expenses/<id>/edit   (placeholder)
│       └── ✗ POST /expenses/<id>/delete (placeholder)
│
├── database/
│   ├── __init__.py
│   └── db.py (stub — to implement)
│       ├── get_db()     → SQLite conn w/ row_factory + foreign keys
│       ├── init_db()    → CREATE TABLE IF NOT EXISTS
│       └── seed_db()    → populate test data
│       └── expense_tracker.db (gitignored)
│
├── templates/
│   ├── base.html        (shared layout)
│   │   ├── navbar (Spendly ◈, nav links)
│   │   ├── footer (Terms/Privacy links)
│   │   └── blocks: title, head, content, scripts
│   ├── landing.html
│   ├── register.html
│   ├── login.html
│   ├── terms.html
│   └── privacy.html
│
├── static/
│   ├── css/
│   │   └── style.css (531 lines, custom design system)
│   │       ├── CSS vars: --ink, --paper, --accent, --danger, --border
│   │       ├── Fonts: DM Serif Display, DM Sans
│   │       ├── Layouts: navbar (sticky), hero (2-col grid), cards (3-col)
│   │       ├── Responsive: 900px, 600px breakpoints
│   │       └── Note: Reuse existing classes; avoid inline styles
│   └── js/
│       └── main.js (empty)
│
└── config/
    ├── requirements.txt
    └── .gitignore (venv/, *.db, __pycache__, .env, etc.)
```

## Where things belongs

- New Routes -> `app.py` only, no blueprints
- DB logic -> `database/db.py` only, never inline in routes
- New Pages -> new `.html` file extending `base.html`
- Page-specific styles -> new `.css` file, not inline `<style></style>` tags

## Code style

- Python: PEP 8, snake_case for all variables and functions
- Templates: Jinja2 with `url_for()` for every internal link - never hardcoded URLs
- Route functions: one responsibility only - fetch data, render template, done
- DB queries : always use parameterized queries (`?` placeholders) - never f-strings in SQL
- Error handling: Use `abort()` for HTTP errors, not bare `return "error string"`

## Tech Constraints

- **Flask only** - no FastAPI, no Djanfo, no other web framework
- **SQLite only** - no PostgreSQL, no SQLAlchemy ORM, no external DB
- **Vanilla JS only\*** -no React, no JQuery, no npm packages
- **No pip packages** - work within `requirements.txt` as is unless explicitly told otherwise

## Workflow notes

- `prompt.txt` holds the user's scratch prompts for past tasks (modified, uncommitted); it is not part of the app.
- Commit messages follow the `area: description` style (e.g. `landing: add Privacy Policy page and route`).
