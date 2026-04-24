"""Production entrypoint: gunicorn wsgi:app -b 127.0.0.1:8000 --threads 4"""
from app import app

__all__ = ["app"]
