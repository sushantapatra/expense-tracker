# Spec: Backend Route for Profile Page

## Overview

Step 5 replaces the hardcoded data in the Step 4 profile page with real data from the SQLite database. The `/profile` route will look up the logged-in user by the `user_id` stored in the session and fetch that user's details, summary stats, recent transactions and category breakdown. Each query lives in `database/db.py` and the route only calls those helpers and renders the template. This is the first step where the app reads user-specific data, and it establishes the pattern (session user → scoped queries → template) that the expense routes in Steps 7–9 will reuse.

## Depends on

- Step 1: Database setup (`users` and `expenses` tables exist)
- Step 2: Registration (users can be created)
- Step 3: Login + Logout (session holds `user_id`)
- Step 4: Profile page (`templates/profile.html`, `static/css/profile.css`, and the auth-guarded `/profile` route). Step 4 currently lives on `feature/profile-page` and is **not yet merged to `main`**. Merge it before implementing this step, otherwise the template and CSS this spec modifies will not exist on this branch.

## Routes

- `GET /profile` — render the profile page with the logged-in user's data from the database (replaces the static context from Step 4) — logged-in only (redirect to `/login` if no `user_id` in session)

No new routes.

## Database changes

No schema changes. The existing `users` (`id`, `name`, `email`, `created_at`) and `expenses` (`user_id`, `amount`, `category`, `date`, `description`) tables are sufficient.

New read-only helper functions in `database/db.py`. Every query is scoped by `user_id` and uses `?` placeholders:

- `get_user_by_id(user_id)` — returns `id`, `name`, `email`, `created_at` for one user, or `None`. Must not return `password_hash`.
- `get_expense_summary(user_id)` — returns `total_spent` (sum of amounts, `0` if none), `transaction_count`, and `top_category` (category with the highest total, `None` if none).
- `get_recent_expenses(user_id, limit=10)` — returns the user's most recent expenses ordered by `date DESC, id DESC`.
- `get_category_breakdown(user_id)` — returns per-category totals for the user, ordered by total descending. Each row includes the category and its share of total spend as a percentage.

## Templates

- **Create:** none
- **Modify:** `templates/profile.html` — replace hardcoded values with template variables from the route context. Keep the existing four sections and their CSS classes. Add empty-state messages for a user with no expenses (no transaction rows, no categories). Category badges use a CSS class per category, not inline colour.

## Files to change

- `database/db.py` — add `get_user_by_id`, `get_expense_summary`, `get_recent_expenses`, `get_category_breakdown`
- `app.py` — replace the Step 4 hardcoded context in `profile()` with calls to the db helpers. Remove the `PROFILE_USER`, `PROFILE_STATS`, `PROFILE_TRANSACTIONS` and `PROFILE_CATEGORIES` constants. If `get_user_by_id` returns `None` (user deleted while session is active), call `session.clear()` and redirect to `login`.
- `templates/profile.html` — bind to real data; add empty states
- `static/css/profile.css` — only if a new category badge class or empty-state style is needed. Use existing CSS variables.

## Files to create

No new files.

## New dependencies

No new dependencies. Use `sqlite3` via `get_db()` (already in use).

## Rules for implementation

- No SQLAlchemy or ORMs — raw `sqlite3` through `get_db()` only
- Parameterised queries only (`?` placeholders). Never f-string or `%`-format SQL, including for the `ORDER BY` or `LIMIT` values
- All DB queries live in `database/db.py`, never in `app.py`
- Route `profile()` has one job: read `session["user_id"]`, call the helpers, render the template
- Every query that returns expense data must filter by the session's `user_id`. Never accept a user id from the query string or form
- Never select or pass `password_hash` to the template
- Use `abort()` for HTTP errors, not bare strings
- Passwords hashed with werkzeug (no changes to auth in this step)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- No inline styles
- Use `url_for()` for all internal links
- Format amounts in the template with two decimal places
- Dates shown as given by the database (ISO `YYYY-MM-DD`) or formatted consistently in the template; do not format dates in SQL

## Definition of done

- [ ] Visiting `/profile` while logged out redirects to `/login` (no DB query runs)
- [ ] Visiting `/profile` while logged in returns HTTP 200
- [ ] The user info card shows the logged-in user's real name and email (log in as `demo@spendly.com` / `demo123` and confirm the values match the `users` row)
- [ ] The "member since" date comes from the user's `created_at` value
- [ ] The summary stats show the correct total spent, transaction count and top category for the logged-in user, matching a manual `SELECT` in `expense_tracker.db`
- [ ] The transaction table shows that user's most recent expenses (up to 10), newest first, with date, description, category and amount
- [ ] Logging in as a second user (e.g. one created via `/register` with no expenses) shows that user's own data only, and the empty-state messages appear (no transactions, zero stats, no categories)
- [ ] The category breakdown shows each category's total and percentage for that user only
- [ ] Changing the session `user_id` to a non-existent id (or deleting the user row) clears the session and redirects to `/login` without a 500 error
- [ ] Password hashes never appear in the rendered HTML (view page source and confirm)
- [ ] No hex colour values in `profile.html` — only CSS variables
- [ ] No SQL is written in `app.py` (`grep -n "SELECT" app.py` returns nothing)
- [ ] `python app.py` starts with no errors and `/profile` loads without a traceback in the console
