from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash
from app.auth import create_user, username_exists
from app.models.audit import log
from app.models.database import execute, rows

system_bp = Blueprint("system", __name__)


@system_bp.get("/audit")
def audit():
    import os
    logs = rows("SELECT TOP 200 id, actor, action, target, created_at FROM audit_logs ORDER BY id DESC") if os.getenv("DB_ENGINE", "sqlite").lower() == "sqlserver" else rows("SELECT id, actor, action, target, created_at FROM audit_logs ORDER BY id DESC LIMIT 200")
    return render_template("audit.html", logs=logs)


@system_bp.route("/accounts", methods=["GET", "POST"])
def accounts():
    allowed_roles = {"user", "to_truong", "to_pho", "truong_phong", "pho_phong", "ban_giam_doc", "administrator"}
    if request.method == "POST":
        display_name = request.form.get("display_name", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "user")
        if not display_name or not username or len(password) < 12 or role not in allowed_roles:
            flash("Thông tin chưa hợp lệ; mật khẩu cần ít nhất 12 ký tự.", "error")
        elif username_exists(username):
            flash("Tên đăng nhập này đã được sử dụng.", "error")
        else:
            create_user(display_name, username, generate_password_hash(password), role)
            log("Tạo tài khoản", f"{username} · {role}")
            flash("Đã tạo tài khoản.", "success")
            return redirect(url_for("system.accounts"))
    role_labels = {"user": "Nhân viên", "to_truong": "Tổ trưởng", "to_pho": "Tổ phó", "truong_phong": "Trưởng phòng", "pho_phong": "Phó phòng", "ban_giam_doc": "Ban giám đốc", "administrator": "Administrator"}
    accounts = rows("SELECT id, title, username, role FROM users WHERE username IS NOT NULL ORDER BY id")
    return render_template("accounts.html", accounts=accounts, role_labels=role_labels, current_user_id=g.user["id"])


@system_bp.post("/accounts/<int:account_id>/delete")
def delete_account(account_id):
    if account_id == g.user["id"]:
        flash("Không thể xóa tài khoản đang đăng nhập.", "error")
    else:
        execute("DELETE FROM users WHERE id=? AND role NOT IN ('administrator','admin')", (account_id,))
        log("Xóa tài khoản", f"#{account_id}")
        flash("Đã xóa tài khoản.", "success")
    return redirect(url_for("system.accounts"))
