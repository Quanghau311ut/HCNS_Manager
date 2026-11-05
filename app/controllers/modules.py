import csv
import io
from flask import Blueprint, abort, flash, make_response, redirect, render_template, request, url_for
from app.models.database import execute, rows
from app.models.modules import MODULES, STATUS_OPTIONS
from app.models.audit import log

modules_bp = Blueprint("modules", __name__)


def _module(key):
    if key not in MODULES:
        abort(404)
    return MODULES[key]


@modules_bp.get("/<key>")
def listing(key):
    meta = _module(key)
    records = rows(f"SELECT id, title, detail, status, start_date, end_date, owner, created_at FROM {key} ORDER BY id DESC")
    return render_template("module.html", key=key, meta=meta, records=records, statuses=STATUS_OPTIONS)


@modules_bp.post("/<key>/save")
def save(key):
    _module(key)
    record_id = request.form.get("id", "").strip()
    values = (request.form.get("title", "").strip(), request.form.get("detail", "").strip(), request.form.get("status", "Mới"), request.form.get("start_date") or None, request.form.get("end_date") or None, request.form.get("owner", "").strip())
    if not values[0]:
        flash("Vui lòng nhập tiêu đề hoặc tên đối tượng.", "error")
        return redirect(url_for("modules.listing", key=key))
    if record_id:
        execute(f"UPDATE {key} SET title=?, detail=?, status=?, start_date=?, end_date=?, owner=? WHERE id=?", (*values, record_id))
        log("Cập nhật", f"{key} #{record_id}")
        flash("Đã cập nhật thông tin.", "success")
    else:
        execute(f"INSERT INTO {key} (title, detail, status, start_date, end_date, owner) VALUES (?, ?, ?, ?, ?, ?)", values)
        log("Thêm mới", f"{key}: {values[0]}")
        flash("Đã tạo mục mới.", "success")
    return redirect(url_for("modules.listing", key=key))


@modules_bp.post("/<key>/<int:record_id>/delete")
def delete(key, record_id):
    _module(key)
    execute(f"DELETE FROM {key} WHERE id=?", (record_id,))
    log("Xóa", f"{key} #{record_id}")
    flash("Đã xóa mục.", "success")
    return redirect(url_for("modules.listing", key=key))


@modules_bp.get("/<key>/export.csv")
def export_csv(key):
    _module(key)
    records = rows(f"SELECT id, title, detail, status, start_date, end_date, owner, created_at FROM {key} ORDER BY id DESC")
    output = io.StringIO()
    output.write("\ufeff")
    writer = csv.DictWriter(output, fieldnames=["id", "title", "detail", "status", "start_date", "end_date", "owner", "created_at"])
    writer.writeheader()
    writer.writerows(records)
    response = make_response(output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = f"attachment; filename={key}.csv"
    return response
