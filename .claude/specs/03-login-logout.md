# Spec: Login and Logout

## Overview

Step 3 implements user login and logout functionality. Users will be able to authenticate with their registered email and password, maintain a session, and securely log out. This completes the authentication flow started in Step 2 (registration) and sets the foundation for protecting routes that require logged-in users (Steps 4+).

## Depends on

- Step 1: Database setup (users table with password_hash)
- Step 2: Registration (users can create accounts)

## Routes

- `POST /login` — Authenticate user with email/password, create session, redirect to profile (or home if not yet implemented)
- `GET /logout` — Clear session and redirect to landing page

## Database changes

No new tables or columns needed. The `users` table created in Step 1 already has `password_hash` and `id` fields required for login.

## Templates

- **Modify:** `templates/login.html` — Add form with email/password fields (GET /login already renders this; POST handler will process it)
- **No new templates** — Logout is a redirect-only action with no template

## Files to change

- `app.py` — Implement `POST /login` and `GET /logout` routes
- `database/db.py` — Add `get_user_by_email_with_password()` function to fetch user with password_hash for comparison
- `templates/login.html` — Ensure form has action, method, and CSRF protection (if Flask-WTF available; otherwise use manual token if needed)
- `templates/base.html` — Add logout link in navbar (visible only when logged in)

## Files to create

No new files.

## New dependencies

No new dependencies. Use Flask's built-in `session` object and `werkzeug.security.check_password_hash()` (already imported).

## Rules for implementation

- Use Flask's `session` object to store `user_id` on successful login
- Use `werkzeug.security.check_password_hash()` to verify passwords — never compare plain text
- Parameterized queries only (`?` placeholders) in all DB calls
- Redirect after POST (no direct rendering of success)
- On logout, clear the session and redirect to landing page
- Login form must have email/password inputs with appropriate names and types
- Navbar must show logout link only when `session.get('user_id')` is set
- All templates extend `base.html`
- Use `url_for()` for all internal links
- Flash messages for errors (invalid email/password combo, already logged in, etc.)

## Definition of done

- [ ] `POST /login` accepts email and password, validates credentials, and creates a session
- [ ] Invalid email/password shows an error message and re-renders the login form
- [ ] On successful login, user is redirected to profile page (Step 4) or landing page
- [ ] `GET /logout` clears the session and redirects to landing page
- [ ] Navbar shows "Logout" link when user is logged in
- [ ] Navbar hides "Login" and "Register" links when user is logged in
- [ ] Navbar shows "Login" and "Register" links when user is logged out
- [ ] Flash messages display correctly (both errors and success messages)
- [ ] Login/logout work end-to-end in the running app
