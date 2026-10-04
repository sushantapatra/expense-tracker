import os
import re
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

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


@app.route("/login")
def login():
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
    return "Logout — coming in Step 3"


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


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
