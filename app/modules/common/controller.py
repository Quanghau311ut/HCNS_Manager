import csv
import io
from flask import Blueprint, abort, flash, g, make_response, redirect, render_template, request, url_for
from app.auth import is_admin
from app.models.audit import log
from app.models.database import rows
from app.models.modules import MODULES, STATUS_OPTIONS


def create_module_blueprint(key, model_class):
    blueprint = Blueprint(f"module_{key}", __name__)
    model = model_class()
    meta = MODULES[key]

    @blueprint.get("/")
    def listing():
        user_id = None if is_admin() or key not in ("attendance", "leave_requests") else g.user["id"]
        return render_template(f"modules/{key}/index.html", key=key, meta=meta, records=model.list(user_id), statuses=STATUS_OPTIONS,
                               can_write=is_admin() or key == "leave_requests", accounts=rows("SELECT id, title, username FROM users WHERE username IS NOT NULL ORDER BY title") if is_admin() and key == "attendance" else [])

    @blueprint.post("/save")
    def save():
        if key == "attendance" and not is_admin():
            abort(403)
        record_id = request.form.get("id", "").strip()
        if key == "leave_requests" and not is_admin() and record_id:
            abort(403)
        status = request.form.get("status", "Mới") if is_admin() else "Chờ duyệt"
        values = (request.form.get("title", "").strip(), request.form.get("detail", "").strip(), status, request.form.get("start_date") or None, request.form.get("end_date") or None, request.form.get("owner", "").strip())
        if not values[0]:
            flash("Vui lòng nhập tiêu đề hoặc tên đối tượng.", "error")
            return redirect(url_for(f"module_{key}.listing"))
        if record_id:
            scope_user_id = g.user["id"] if not is_admin() and key == "leave_requests" else None
            update_assignment = key == "attendance" and is_admin()
            assigned_user_id = request.form.get("user_id") or None if update_assignment else None
            model.update(record_id, values, scope_user_id, assigned_user_id, update_assignment)
            log("Cập nhật", f"{key} #{record_id}")
            flash("Đã cập nhật thông tin.", "success")
        else:
            assigned_user_id = g.user["id"] if not is_admin() and key == "leave_requests" else None
            if key == "attendance" and is_admin():
                assigned_user_id = request.form.get("user_id") or None
            model.create(values, assigned_user_id)
            log("Thêm mới", f"{key}: {values[0]}")
            flash("Đã tạo mục mới.", "success")
        return redirect(url_for(f"module_{key}.listing"))

    @blueprint.post("/<int:record_id>/delete")
    def delete(record_id):
        if not is_admin():
            abort(403)
        scope_user_id = g.user["id"] if not is_admin() and key == "leave_requests" else None
        model.delete(record_id, scope_user_id)
        log("Xóa", f"{key} #{record_id}")
        flash("Đã xóa mục.", "success")
        return redirect(url_for(f"module_{key}.listing"))

    @blueprint.get("/export.csv")
    def export_csv():
        output = io.StringIO()
        output.write("\ufeff")
        columns = ["id", "title", "detail", "status", "start_date", "end_date", "owner", "user_id", "created_at"]
        writer = csv.DictWriter(output, fieldnames=columns)
        writer.writeheader()
        user_id = None if is_admin() or key not in ("attendance", "leave_requests") else g.user["id"]
        writer.writerows(model.export(user_id))
        response = make_response(output.getvalue())
        response.headers["Content-Type"] = "text/csv; charset=utf-8"
        response.headers["Content-Disposition"] = f"attachment; filename={key}.csv"
        return response

    return blueprint
