import csv
import io
from flask import Blueprint, flash, make_response, redirect, render_template, request, url_for
from app.models.audit import log
from app.models.modules import MODULES, STATUS_OPTIONS


def create_module_blueprint(key, model_class):
    blueprint = Blueprint(f"module_{key}", __name__)
    model = model_class()
    meta = MODULES[key]

    @blueprint.get("/")
    def listing():
        return render_template(f"modules/{key}/index.html", key=key, meta=meta, records=model.list(), statuses=STATUS_OPTIONS)

    @blueprint.post("/save")
    def save():
        record_id = request.form.get("id", "").strip()
        values = (request.form.get("title", "").strip(), request.form.get("detail", "").strip(), request.form.get("status", "Mới"), request.form.get("start_date") or None, request.form.get("end_date") or None, request.form.get("owner", "").strip())
        if not values[0]:
            flash("Vui lòng nhập tiêu đề hoặc tên đối tượng.", "error")
            return redirect(url_for(f"module_{key}.listing"))
        if record_id:
            model.update(record_id, values)
            log("Cập nhật", f"{key} #{record_id}")
            flash("Đã cập nhật thông tin.", "success")
        else:
            model.create(values)
            log("Thêm mới", f"{key}: {values[0]}")
            flash("Đã tạo mục mới.", "success")
        return redirect(url_for(f"module_{key}.listing"))

    @blueprint.post("/<int:record_id>/delete")
    def delete(record_id):
        model.delete(record_id)
        log("Xóa", f"{key} #{record_id}")
        flash("Đã xóa mục.", "success")
        return redirect(url_for(f"module_{key}.listing"))

    @blueprint.get("/export.csv")
    def export_csv():
        output = io.StringIO()
        output.write("\ufeff")
        columns = ["id", "title", "detail", "status", "start_date", "end_date", "owner", "created_at"]
        writer = csv.DictWriter(output, fieldnames=columns)
        writer.writeheader()
        writer.writerows(model.export())
        response = make_response(output.getvalue())
        response.headers["Content-Type"] = "text/csv; charset=utf-8"
        response.headers["Content-Disposition"] = f"attachment; filename={key}.csv"
        return response

    return blueprint
