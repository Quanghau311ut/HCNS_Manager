from app.models.database import execute, rows


class ModuleModel:
    """Reusable persistence operations; each feature supplies its own table."""
    table = None

    def list(self):
        return rows(f"SELECT id, title, detail, status, start_date, end_date, owner, created_at FROM {self.table} ORDER BY id DESC")

    def create(self, values):
        execute(f"INSERT INTO {self.table} (title, detail, status, start_date, end_date, owner) VALUES (?, ?, ?, ?, ?, ?)", values)

    def update(self, record_id, values):
        execute(f"UPDATE {self.table} SET title=?, detail=?, status=?, start_date=?, end_date=?, owner=? WHERE id=?", (*values, record_id))

    def delete(self, record_id):
        execute(f"DELETE FROM {self.table} WHERE id=?", (record_id,))

    def export(self):
        return self.list()
