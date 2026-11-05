from flask import Blueprint, render_template
from app.models.database import rows
from app.models.modules import MODULES

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/")
def index():
    stats = []
    for key, item in MODULES.items():
        try:
            total = rows(f"SELECT COUNT(*) AS total FROM {key}")[0]["total"]
        except Exception:
            total = 0
        stats.append({"key": key, "name": item["name"], "total": total, "icon": item["icon"]})
    recent = rows("SELECT TOP 8 id, actor, action, target, created_at FROM audit_logs ORDER BY id DESC") if __import__('os').getenv("DB_ENGINE", "sqlite").lower() == "sqlserver" else rows("SELECT id, actor, action, target, created_at FROM audit_logs ORDER BY id DESC LIMIT 8")
    return render_template("dashboard.html", stats=stats, recent=recent)
