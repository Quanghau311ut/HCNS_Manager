from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from app.models.audit import log
from app.modules.meetings.model import MeetingModel

blueprint = Blueprint("module_meetings", __name__)
model = MeetingModel()


@blueprint.get("/")
def listing():
    return render_template("modules/meetings/index.html", bookings=model.bookings(), rooms=model.rooms())


@blueprint.post("/book")
def book():
    title = request.form.get("title", "").strip()
    room_id, start, end = request.form.get("room_id", ""), request.form.get("start_date", ""), request.form.get("end_date", "")
    if not title or not room_id or not start or not end or end <= start:
        flash("Vui lòng nhập đủ thông tin và kiểm tra thời gian đặt phòng.", "error")
    else:
        created = model.create_booking_if_available(title, request.form.get("detail", ""), start, end, room_id, g.user["title"], g.user["id"])
        if not created:
            flash("Phòng đã có lịch trong khoảng thời gian này.", "error")
        else:
            log("Đặt phòng", title)
            flash("Yêu cầu đặt phòng đã gửi, đang chờ administrator duyệt.", "success")
    return redirect(url_for("module_meetings.listing"))


@blueprint.post("/<int:booking_id>/status")
def update_status(booking_id):
    status = request.form.get("status")
    if status not in ("Đã duyệt", "Đã hủy", "Từ chối"):
        flash("Trạng thái không hợp lệ.", "error")
    else:
        model.set_status(booking_id, status)
        log("Đổi trạng thái lịch họp", f"#{booking_id}: {status}")
        flash("Đã cập nhật lịch họp.", "success")
    return redirect(url_for("module_meetings.listing"))
