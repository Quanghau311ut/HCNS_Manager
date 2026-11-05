from app.modules.common.model import ModuleModel
from app.models.database import execute, rows

class UserModel(ModuleModel):
    table = "users"

    def list(self, user_id=None):
        return rows("SELECT id, title, detail, status, start_date, end_date, owner, user_id, created_at FROM users WHERE username IS NULL ORDER BY id DESC")

    def update(self, record_id, values, user_id=None, assigned_user_id=None, update_assignment=False):
        execute("UPDATE users SET title=?, detail=?, status=?, start_date=?, end_date=?, owner=? WHERE id=? AND username IS NULL", (*values, record_id))

    def delete(self, record_id, user_id=None):
        execute("DELETE FROM users WHERE id=? AND username IS NULL", (record_id,))
