from flask import Blueprint, render_template
from app.models.database import rows

system_bp = Blueprint("system", __name__)


@system_bp.get("/audit")
def audit():
    import os
    logs = rows("SELECT TOP 200 id, actor, action, target, created_at FROM audit_logs ORDER BY id DESC") if os.getenv("DB_ENGINE", "sqlite").lower() == "sqlserver" else rows("SELECT id, actor, action, target, created_at FROM audit_logs ORDER BY id DESC LIMIT 200")
    return render_template("audit.html", logs=logs)
