"""
test_database.py
----------------
Tests for the database module.
"""

from app.database import fetch_task, fetch_all_tasks


def test_fetch_task_returns_none_for_missing():
    result = fetch_task(99999)
    assert result is None


def test_fetch_all_tasks_returns_list():
    result = fetch_all_tasks()
    assert isinstance(result, list)
