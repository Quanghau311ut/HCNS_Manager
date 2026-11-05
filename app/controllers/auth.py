from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.auth import create_user, username_exists, user_count
from app.models.database import rows

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        result = rows("SELECT id, password_hash, role FROM users WHERE username=?", (username,))
        if result and result[0]["password_hash"] and check_password_hash(result[0]["password_hash"], password):
            session.clear()
            session["user_id"] = result[0]["id"]
            destination = request.args.get("next") or url_for("dashboard.index")
            if not destination.startswith("/") or destination.startswith("//"):
                destination = url_for("dashboard.index")
            return redirect(destination)
        flash("Tên đăng nhập hoặc mật khẩu không đúng.", "error")
    return render_template("login.html", setup_available=user_count() == 0)


@auth_bp.route("/setup", methods=["GET", "POST"])
def setup():
    if user_count() > 0:
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        display_name = request.form.get("display_name", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        if not display_name or not username or len(password) < 12:
            flash("Nhập đầy đủ thông tin; mật khẩu cần ít nhất 12 ký tự.", "error")
        elif password != confirm:
            flash("Mật khẩu xác nhận chưa khớp.", "error")
        elif username_exists(username):
            flash("Tên đăng nhập này đã được sử dụng.", "error")
        else:
            create_user(display_name, username, generate_password_hash(password), "administrator")
            flash("Đã tạo tài khoản administrator. Hãy đăng nhập.", "success")
            return redirect(url_for("auth.login"))
    return render_template("setup.html")


@auth_bp.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
