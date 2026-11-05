from app.models.database import execute, rows


class MeetingModel:
    def rooms(self):
        return rows("SELECT id, name, capacity, equipment, status FROM meeting_rooms ORDER BY name")

    def bookings(self):
        import os
        sql = "SELECT b.id, b.title, b.detail, b.status, b.start_date, b.end_date, b.owner, b.requester, r.name AS room FROM meeting_bookings b LEFT JOIN meeting_rooms r ON r.id = TRY_CONVERT(INT, b.owner) ORDER BY b.start_date DESC"
        if os.getenv("DB_ENGINE", "sqlite").lower() != "sqlserver":
            sql = "SELECT b.id, b.title, b.detail, b.status, b.start_date, b.end_date, b.owner, b.requester, r.name AS room FROM meeting_bookings b LEFT JOIN meeting_rooms r ON r.id = CAST(b.owner AS INTEGER) ORDER BY b.start_date DESC"
        return rows(sql)

    def has_conflict(self, room_id, start, end):
        return bool(rows("SELECT id FROM meeting_bookings WHERE owner=? AND status NOT IN ('Đã hủy','Từ chối') AND start_date < ? AND end_date > ?", (room_id, end, start)))

    def create_booking(self, title, detail, status, start, end, room_id, requester):
        execute("INSERT INTO meeting_bookings (title, detail, status, start_date, end_date, owner, requester) VALUES (?, ?, ?, ?, ?, ?, ?)", (title, detail, status, start, end, room_id, requester))

    def set_status(self, booking_id, status):
        execute("UPDATE meeting_bookings SET status=? WHERE id=?", (status, booking_id))
