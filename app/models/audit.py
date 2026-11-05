from flask import g, has_request_context
from app.models.database import execute


def log(action, target, actor=None):
    if actor is None:
        actor = g.user["title"] if has_request_context() and getattr(g, "user", None) else "Hệ thống"
    execute("INSERT INTO audit_logs (actor, action, target) VALUES (?, ?, ?)", (actor, action, target))
