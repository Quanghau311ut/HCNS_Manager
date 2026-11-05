from app.models.database import execute


def log(action, target, actor="Quản trị viên"):
    execute("INSERT INTO audit_logs (actor, action, target) VALUES (?, ?, ?)", (actor, action, target))
