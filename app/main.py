"""
main.py
-------
Entry point for the TaskManager Flask application.
"""

from flask import Flask
from app.routes import register_routes


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    register_routes(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=False, host="0.0.0.0", port=5000)
