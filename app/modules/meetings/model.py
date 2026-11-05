from app.models.database import connection, execute, rows


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

    def create_booking_if_available(self, title, detail, start, end, room_id, requester, user_id):
        with connection() as (conn, sqlserver):
            cur = conn.cursor()
            if sqlserver:
                cur.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
            else:
                cur.execute("BEGIN IMMEDIATE")
            cur.execute("SELECT id FROM meeting_bookings WHERE owner=? AND status NOT IN ('Đã hủy','Từ chối') AND start_date < ? AND end_date > ?", (room_id, end, start))
            if cur.fetchall():
                return False
            cur.execute("INSERT INTO meeting_bookings (title, detail, status, start_date, end_date, owner, requester, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (title, detail, "Chờ duyệt", start, end, room_id, requester, user_id))
            return True

    def set_status(self, booking_id, status):
        execute("UPDATE meeting_bookings SET status=? WHERE id=?", (status, booking_id))
