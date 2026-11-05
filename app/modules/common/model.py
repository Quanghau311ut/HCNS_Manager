from app.models.database import execute, rows


class ModuleModel:
    """Reusable persistence operations; each feature supplies its own table."""
    table = None

    def list(self, user_id=None):
        sql = f"SELECT id, title, detail, status, start_date, end_date, owner, user_id, created_at FROM {self.table}"
        if user_id is not None:
            sql += " WHERE user_id=?"
            return rows(sql + " ORDER BY id DESC", (user_id,))
        return rows(sql + " ORDER BY id DESC")

    def create(self, values, user_id=None):
        execute(f"INSERT INTO {self.table} (title, detail, status, start_date, end_date, owner, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (*values, user_id))

    def update(self, record_id, values, user_id=None, assigned_user_id=None, update_assignment=False):
        sql = f"UPDATE {self.table} SET title=?, detail=?, status=?, start_date=?, end_date=?, owner=? WHERE id=?"
        params = (*values, record_id)
        if update_assignment:
            sql = f"UPDATE {self.table} SET title=?, detail=?, status=?, start_date=?, end_date=?, owner=?, user_id=? WHERE id=?"
            params = (*values, assigned_user_id, record_id)
        if user_id is not None:
            sql += " AND user_id=?"
            params += (user_id,)
        execute(sql, params)

    def delete(self, record_id, user_id=None):
        sql = f"DELETE FROM {self.table} WHERE id=?"
        params = (record_id,)
        if user_id is not None:
            sql += " AND user_id=?"
            params += (user_id,)
        execute(sql, params)

    def export(self, user_id=None):
        return self.list(user_id)
