import os
import re
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash

from database.db import get_db, init_db, seed_db, get_user_by_email, create_user

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or len(name) > 100:
            return render_template(
                "register.html",
                error="Name must be between 1 and 100 characters",
                name=name,
                email=email,
            ), 400

        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            return render_template(
                "register.html",
                error="Please enter a valid email address",
                name=name,
                email=email,
            ), 400

        if len(password) < 6:
            return render_template(
                "register.html",
                error="Password must be at least 6 characters",
                name=name,
                email=email,
            ), 400

        if password != confirm_password:
            return render_template(
                "register.html",
                error="Passwords do not match",
                name=name,
                email=email,
            ), 400

        if get_user_by_email(email):
            return render_template(
                "register.html",
                error="Email already registered",
                name=name,
                email=email,
            ), 400

        try:
            create_user(name, email, password)
            flash("Account created. Please sign in.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return render_template(
                "register.html",
                error="Email already registered",
                name=name,
                email=email,
            ), 400

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = get_user_by_email(email)

        if not user or not check_password_hash(user["password_hash"], password):
            return render_template(
                "login.html",
                error="Invalid email or password",
                email=email,
            ), 400

        session.clear()
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        return redirect(url_for("profile"))

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.")
    return redirect(url_for("landing"))


# Hardcoded profile data — replaced with DB queries in Step 5.
# Widths are rounded to the nearest 5% (minimum 5) to match the w-* classes in profile.css.
PROFILE_USER = {
    "name": "Demo User",
    "email": "demo@spendly.com",
    "member_since": "January 2026",
    "initials": "DU",
}

PROFILE_STATS = {
    "total_spent": "167.44",
    "transaction_count": 5,
    "top_category": "Bills",
}

PROFILE_TRANSACTIONS = [
    {"date": "2026-10-09", "description": "Lunch at cafe", "category": "Food", "amount": "12.50"},
    {"date": "2026-10-07", "description": "Bus fare", "category": "Transport", "amount": "3.20"},
    {"date": "2026-10-05", "description": "Electricity bill", "category": "Bills", "amount": "85.00"},
    {"date": "2026-10-03", "description": "Pharmacy", "category": "Health", "amount": "24.99"},
    {"date": "2026-10-01", "description": "Groceries", "category": "Food", "amount": "41.75"},
]

PROFILE_CATEGORIES = [
    {"name": "Bills", "total": "85.00", "percent": 50},
    {"name": "Food", "total": "54.25", "percent": 30},
    {"name": "Health", "total": "24.99", "percent": 15},
    {"name": "Transport", "total": "3.20", "percent": 5},
]


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    return render_template(
        "profile.html",
        user=PROFILE_USER,
        stats=PROFILE_STATS,
        transactions=PROFILE_TRANSACTIONS,
        categories=PROFILE_CATEGORIES,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
