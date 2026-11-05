from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.models.database import execute, rows
from app.models.audit import log

meetings_bp = Blueprint("meetings", __name__)


@meetings_bp.get("/")
def index():
    bookings = rows("SELECT b.id, b.title, b.detail, b.status, b.start_date, b.end_date, b.owner, b.requester, r.name AS room FROM meeting_bookings b LEFT JOIN meeting_rooms r ON r.id = TRY_CONVERT(INT, b.owner) ORDER BY b.start_date DESC") if __import__('os').getenv("DB_ENGINE", "sqlite").lower() == "sqlserver" else rows("SELECT b.id, b.title, b.detail, b.status, b.start_date, b.end_date, b.owner, b.requester, r.name AS room FROM meeting_bookings b LEFT JOIN meeting_rooms r ON r.id = CAST(b.owner AS INTEGER) ORDER BY b.start_date DESC")
    rooms = rows("SELECT id, name, capacity, equipment, status FROM meeting_rooms ORDER BY name")
    return render_template("meetings.html", bookings=bookings, rooms=rooms)


@meetings_bp.post("/book")
def book():
    title = request.form.get("title", "").strip()
    room_id = request.form.get("room_id", "")
    start = request.form.get("start_date", "")
    end = request.form.get("end_date", "")
    if not title or not room_id or not start or not end or end <= start:
        flash("Vui lòng nhập đủ thông tin và kiểm tra thời gian đặt phòng.", "error")
        return redirect(url_for("meetings.index"))
    clash = rows("SELECT id FROM meeting_bookings WHERE owner=? AND status NOT IN ('Đã hủy','Từ chối') AND start_date < ? AND end_date > ?", (room_id, end, start))
    if clash:
        flash("Phòng đã có lịch trong khoảng thời gian này.", "error")
        return redirect(url_for("meetings.index"))
    execute("INSERT INTO meeting_bookings (title, detail, status, start_date, end_date, owner, requester) VALUES (?, ?, ?, ?, ?, ?, ?)", (title, request.form.get("detail", ""), "Chờ duyệt", start, end, room_id, request.form.get("requester", "").strip()))
    log("Đặt phòng", title)
    flash("Yêu cầu đặt phòng đã gửi, đang chờ duyệt.", "success")
    return redirect(url_for("meetings.index"))


@meetings_bp.post("/<int:booking_id>/status")
def update_status(booking_id):
    status = request.form.get("status")
    if status not in ("Đã duyệt", "Đã hủy", "Từ chối"):
        flash("Trạng thái không hợp lệ.", "error")
        return redirect(url_for("meetings.index"))
    execute("UPDATE meeting_bookings SET status=? WHERE id=?", (status, booking_id))
    log("Đổi trạng thái lịch họp", f"#{booking_id}: {status}")
    flash("Đã cập nhật lịch họp.", "success")
    return redirect(url_for("meetings.index"))
