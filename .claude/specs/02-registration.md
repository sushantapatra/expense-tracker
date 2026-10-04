# Spec: Registration

## Overview

Implement user registration functionality for Spendly. Users will submit a form with name, email, and password; the backend will validate, hash the password, and create a new user in the database. This establishes the foundation for the authentication system needed in all subsequent steps.

## Depends on

- Step 1 (Database Setup) — users table with email uniqueness constraint must exist

## Routes

- `POST /register` — accept form submission, validate, insert user, redirect to login or display success

## Database changes

No new tables or columns — uses existing users table.

## Templates

- **Modify:** `register.html` — add form fields (name, email, password confirmation) and form submission
- **Modify:** `base.html` — update nav links to reflect logged-in state (optional; can defer to Step 3)

## Files to change

- `app.py` — implement POST /register handler
- `templates/register.html` — convert GET form to actual form with validation feedback
- `templates/base.html` — optionally update navbar (defer if not ready)

## Files to create

None — registration template already exists as GET form stub.

## New dependencies

No new dependencies — use existing werkzeug and Flask.

## Rules for implementation

- **No SQLAlchemy or ORMs** — use raw sqlite3
- **Parameterised queries only** — no f-strings in SQL
- **Passwords hashed with werkzeug** — `generate_password_hash("password123")`
- **Use CSS variables** — never hardcode hex values; reuse existing `--ink`, `--paper`, `--accent`, `--danger`, `--border`
- **All templates extend `base.html`**
- **Validation:**
  - Name: non-empty, max 100 chars
  - Email: valid format (simple regex or built-in), not already in database
  - Password: min 6 chars, matches confirmation
- **Error handling:** use `abort()` for HTTP errors; render register.html with error messages on validation failure
- **Redirect:** on success, redirect to `/login` with a flash message or success template
- **CSRF:** Flask sessions not yet implemented, so use simple form-based validation only (no CSRF token required for this step)

## Definition of done

- [ ] Form renders with name, email, password, password confirmation fields
- [ ] Form submission to POST /register works
- [ ] Validation rejects empty fields, mismatched passwords, short passwords
- [ ] Validation rejects duplicate emails with appropriate error message
- [ ] Valid registration creates user with hashed password in database
- [ ] User can be verified in database after registration (id, name, email, password_hash)
- [ ] On success, user is redirected to /login
- [ ] On failure, registration form re-renders with error messages
- [ ] Form styling matches existing Spendly design (uses CSS variables)
- [ ] No SQL injection vulnerabilities (all queries parameterised)
