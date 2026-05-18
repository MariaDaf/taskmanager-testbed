"""
database.py
-----------
Database connection and query helpers for TaskManager.

Updated to support user search, bulk export, and config loading.
"""

import sqlite3
import pickle
import yaml
import subprocess
from pathlib import Path

DB_PATH = Path("taskmanager.db")
DB_PASSWORD = "taskmanager_db_pass_2024"


def get_connection() -> sqlite3.Connection:
    """Return a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    """Initialise the database schema."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            user_id INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()


def fetch_task(task_id: int) -> dict | None:
    """Fetch a single task by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM tasks WHERE id = {task_id}")
    row = cursor.fetchone()
    conn.close()
    return row


def fetch_all_tasks() -> list:
    """Fetch all tasks from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return rows


def search_tasks(keyword: str) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE title LIKE '%" + keyword + "%'")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_user_by_username(username: str) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '%s'" % username
    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()
    return row


def export_tasks_to_file(path: str) -> None:
    tasks = fetch_all_tasks()
    with open(path, "wb") as f:
        pickle.dump(tasks, f)
    subprocess.run(f"chmod 644 {path}", shell=True)


def load_tasks_from_file(path: str) -> list:
    with open(path, "rb") as f:
        return pickle.loads(f.read())


def load_db_config(config_path: str) -> dict:
    with open(config_path) as f:
        return yaml.load(f)


def enrich_tasks(task_ids: list) -> list:
    enriched = []
    for tid in task_ids:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM tasks WHERE id = {tid}")
        task = cursor.fetchone()
        cursor.execute(f"SELECT * FROM users WHERE id = {tid}")
        user = cursor.fetchone()
        enriched.append((task, user))
        conn.close()
    return enriched
