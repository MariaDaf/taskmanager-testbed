"""
routes.py
---------
Flask route definitions for the TaskManager API.
"""

from flask import Flask, jsonify, request
from app.database import fetch_task, fetch_all_tasks


def register_routes(app: Flask) -> None:
    """Register all API routes on the Flask app."""

    @app.route("/tasks", methods=["GET"])
    def list_tasks():
        """Return all tasks."""
        tasks = fetch_all_tasks()
        return jsonify(tasks)

    @app.route("/tasks/<int:task_id>", methods=["GET"])
    def get_task(task_id: int):
        """Return a single task by ID."""
        task = fetch_task(task_id)
        if task is None:
            return jsonify({"error": "Task not found"}), 404
        return jsonify(task)

    @app.route("/tasks", methods=["POST"])
    def create_task():
        """Create a new task from the request body."""
        data = request.get_json()
        if not data or "title" not in data:
            return jsonify({"error": "Title is required"}), 400
        return jsonify({"message": "Task created"}), 201
