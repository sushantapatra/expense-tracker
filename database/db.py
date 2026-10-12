import os
import sqlite3
from datetime import date

from werkzeug.security import generate_password_hash

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "expense_tracker.db")

CATEGORIES = [
    "Food",
    "Transport",
    "Bills",
    "Health",
    "Entertainment",
    "Shopping",
    "Other",
]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT NOT NULL,
                email         TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at    TEXT DEFAULT (datetime('now'))
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL REFERENCES users(id),
                amount      REAL NOT NULL,
                category    TEXT NOT NULL,
                date        TEXT NOT NULL,
                description TEXT,
                created_at  TEXT DEFAULT (datetime('now'))
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def get_user_by_email(email):
    conn = get_db()
    try:
        return conn.execute("SELECT id, name, email, password_hash FROM users WHERE email = ?", (email,)).fetchone()
    finally:
        conn.close()


def create_user(name, email, password):
    conn = get_db()
    try:
        password_hash = generate_password_hash(password)
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_user_by_id(user_id):
    conn = get_db()
    try:
        return conn.execute(
            "SELECT id, name, email, created_at FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
    finally:
        conn.close()


def get_expense_summary(user_id):
    conn = get_db()
    try:
        totals = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) AS total_spent, COUNT(*) AS transaction_count "
            "FROM expenses WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        top = conn.execute(
            "SELECT category FROM expenses WHERE user_id = ? "
            "GROUP BY category ORDER BY SUM(amount) DESC LIMIT 1",
            (user_id,),
        ).fetchone()
        return {
            "total_spent": totals["total_spent"],
            "transaction_count": totals["transaction_count"],
            "top_category": top["category"] if top else None,
        }
    finally:
        conn.close()


def get_recent_expenses(user_id, limit=10):
    conn = get_db()
    try:
        return conn.execute(
            "SELECT date, description, category, amount FROM expenses "
            "WHERE user_id = ? ORDER BY date DESC, id DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
    finally:
        conn.close()


def get_category_breakdown(user_id):
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT category AS name, SUM(amount) AS total FROM expenses "
            "WHERE user_id = ? GROUP BY category ORDER BY total DESC",
            (user_id,),
        ).fetchall()
    finally:
        conn.close()

    grand_total = sum(row["total"] for row in rows)
    categories = []
    for row in rows:
        # Round to the nearest 5% (minimum 5) to match the w-* classes in profile.css
        percent = max(5, round(row["total"] / grand_total * 100 / 5) * 5) if grand_total else 0
        categories.append({"name": row["name"], "total": row["total"], "percent": percent})
    return categories


def seed_db():
    conn = get_db()
    try:
        if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
            return

        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
        )
        user_id = cursor.lastrowid

        today = date.today()
        samples = [
            (1, 12.50, "Food", "Lunch at cafe"),
            (2, 3.20, "Transport", "Bus fare"),
            (3, 85.00, "Bills", "Electricity bill"),
            (4, 24.99, "Health", "Pharmacy"),
            (5, 15.00, "Entertainment", "Movie ticket"),
            (6, 59.90, "Shopping", "New t-shirt"),
            (7, 10.00, "Other", "Miscellaneous"),
            (8, 41.75, "Food", "Groceries"),
        ]
        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) "
            "VALUES (?, ?, ?, ?, ?)",
            [
                (user_id, amount, category, today.replace(day=day).isoformat(), desc)
                for day, amount, category, desc in samples
            ],
        )
        conn.commit()
    finally:
        conn.close()
