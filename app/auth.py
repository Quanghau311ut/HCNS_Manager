from flask import abort, g, redirect, request, session, url_for

from app.models.database import execute, rows

BOOKING_ROLES = {
    "to truong", "to pho", "truong phong", "pho phong",
    "ban giam doc", "administrator", "admin",
}
USER_BLUEPRINTS = {"module_leave_requests", "module_attendance", "module_meetings"}


def is_admin(user=None):
    user = user or getattr(g, "user", None)
    return bool(user and user["role"] in ("administrator", "admin"))


def can_book_meetings(user=None):
    user = user or getattr(g, "user", None)
    if not user:
        return False
    role = user["role"].casefold().replace("đ", "d")
    import unicodedata
    role = role.replace(chr(95), chr(32))
    role = "".join(char for char in unicodedata.normalize("NFD", role) if unicodedata.category(char) != "Mn")
    return role in BOOKING_ROLES


def register_auth(app):
    @app.before_request
    def load_and_authorize_user():
        g.user = None
        user_id = session.get("user_id")
        if user_id:
            found = rows("SELECT id, title, username, role FROM users WHERE id=?", (user_id,))
            if found:
                g.user = found[0]
            else:
                session.clear()
        if request.endpoint in ("auth.login", "auth.setup", "auth.logout") or request.endpoint == "static":
            return None
        if not g.user:
            return redirect(url_for("auth.login", next=request.path))
        if is_admin():
            return None
        if request.endpoint == "dashboard.index":
            return redirect(url_for("module_leave_requests.listing"))
        if request.blueprint not in USER_BLUEPRINTS:
            abort(403)
        if request.blueprint == "module_meetings" and not can_book_meetings():
            abort(403)
        if request.blueprint == "module_attendance" and request.method != "GET":
            abort(403)
        if request.endpoint == "module_meetings.update_status":
            abort(403)
        return None


def create_user(display_name, username, password_hash, role="user"):
    execute("INSERT INTO users (title, username, password_hash, role, status) VALUES (?, ?, ?, ?, ?)",
            (display_name, username, password_hash, role, "Hoạt động"))


def user_count():
    return rows("SELECT COUNT(*) AS total FROM users WHERE username IS NOT NULL")[0]["total"]


def username_exists(username):
    return bool(rows("SELECT id FROM users WHERE username=?", (username,)))
