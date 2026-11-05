"""Small DB-API layer supporting SQL Server and local SQLite development."""
import os
import sqlite3
from contextlib import contextmanager
from flask import current_app


def _sqlite_path():
    return os.getenv("SQLITE_PATH", os.path.join(current_app.instance_path, "hcns_manager.db"))


def _connect():
    if os.getenv("DB_ENGINE", "sqlite").lower() == "sqlserver":
        try:
            import pyodbc
        except ImportError as exc:
            raise RuntimeError("Cài pyodbc và ODBC Driver 18 for SQL Server để kết nối SQL Server.") from exc
        server = os.getenv("DB_SERVER", r"192.168.1.69\QA-204")
        database = os.getenv("DB_NAME", "HCNS_Manager")
        driver = os.getenv("DB_ODBC_DRIVER", "ODBC Driver 18 for SQL Server")
        if os.getenv("DB_USER"):
            auth = f"UID={os.environ['DB_USER']};PWD={os.environ.get('DB_PASSWORD', '')};"
        else:
            auth = "Trusted_Connection=yes;"
        conn = pyodbc.connect(
            f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};{auth}"
            f"Encrypt={os.getenv('DB_ENCRYPT', 'yes')};TrustServerCertificate={os.getenv('DB_TRUST_CERT', 'yes')};",
            autocommit=False,
        )
        return conn, True
    os.makedirs(os.path.dirname(os.path.abspath(_sqlite_path())), exist_ok=True)
    conn = sqlite3.connect(_sqlite_path())
    conn.row_factory = sqlite3.Row
    return conn, False


@contextmanager
def connection():
    conn, sqlserver = _connect()
    try:
        yield conn, sqlserver
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def rows(sql, params=()):
    with connection() as (conn, _):
        cur = conn.cursor()
        cur.execute(sql, params)
        fetched = cur.fetchall()
        if not fetched:
            return []
        if isinstance(fetched[0], sqlite3.Row):
            return [dict(row) for row in fetched]
        names = [column[0] for column in cur.description]
        return [dict(zip(names, row)) for row in fetched]


def execute(sql, params=()):
    with connection() as (conn, _):
        cur = conn.cursor()
        cur.execute(sql, params)
        return getattr(cur, "lastrowid", None)


def init_db():
    os.makedirs(current_app.instance_path, exist_ok=True)
    with connection() as (conn, sqlserver):
        cur = conn.cursor()
        for table in TABLES:
            if sqlserver:
                cur.execute(f"IF OBJECT_ID(N'dbo.{table}', N'U') IS NULL CREATE TABLE dbo.{table} (id INT IDENTITY(1,1) PRIMARY KEY, title NVARCHAR(200) NOT NULL, detail NVARCHAR(MAX) NULL, status NVARCHAR(40) NOT NULL DEFAULT N'Mới', start_date NVARCHAR(20) NULL, end_date NVARCHAR(20) NULL, owner NVARCHAR(120) NULL, user_id INT NULL, created_at DATETIME2 NOT NULL DEFAULT SYSDATETIME())")
                cur.execute(f"IF COL_LENGTH('dbo.{table}','user_id') IS NULL ALTER TABLE dbo.{table} ADD user_id INT NULL")
            else:
                cur.execute(f"CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, detail TEXT, status TEXT NOT NULL DEFAULT 'Mới', start_date TEXT, end_date TEXT, owner TEXT, user_id INTEGER, created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
                columns = [row[1] for row in cur.execute(f"PRAGMA table_info({table})").fetchall()]
                if "user_id" not in columns:
                    cur.execute(f"ALTER TABLE {table} ADD COLUMN user_id INTEGER")
        if sqlserver:
            cur.execute("IF COL_LENGTH('dbo.users','username') IS NULL ALTER TABLE dbo.users ADD username NVARCHAR(80) NULL")
            cur.execute("IF COL_LENGTH('dbo.users','password_hash') IS NULL ALTER TABLE dbo.users ADD password_hash NVARCHAR(255) NULL")
            cur.execute("IF COL_LENGTH('dbo.users','role') IS NULL ALTER TABLE dbo.users ADD role NVARCHAR(50) NOT NULL CONSTRAINT DF_users_role DEFAULT N'user'")
            cur.execute("IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name='UX_users_username' AND object_id=OBJECT_ID('dbo.users')) CREATE UNIQUE INDEX UX_users_username ON dbo.users(username) WHERE username IS NOT NULL")
        else:
            columns = [row[1] for row in cur.execute("PRAGMA table_info(users)").fetchall()]
            if "username" not in columns:
                cur.execute("ALTER TABLE users ADD COLUMN username TEXT")
            if "password_hash" not in columns:
                cur.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
            if "role" not in columns:
                cur.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'user'")
            cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS UX_users_username ON users(username) WHERE username IS NOT NULL")
        if sqlserver:
            cur.execute("IF OBJECT_ID(N'dbo.meeting_rooms', N'U') IS NULL CREATE TABLE dbo.meeting_rooms (id INT IDENTITY(1,1) PRIMARY KEY, name NVARCHAR(150) NOT NULL, capacity INT NOT NULL DEFAULT 1, equipment NVARCHAR(500) NULL, status NVARCHAR(30) NOT NULL DEFAULT N'Hoạt động')")
            cur.execute("IF OBJECT_ID(N'dbo.audit_logs', N'U') IS NULL CREATE TABLE dbo.audit_logs (id INT IDENTITY(1,1) PRIMARY KEY, actor NVARCHAR(120), action NVARCHAR(200), target NVARCHAR(200), created_at DATETIME2 DEFAULT SYSDATETIME())")
            cur.execute("IF COL_LENGTH('dbo.meeting_bookings','requester') IS NULL ALTER TABLE dbo.meeting_bookings ADD requester NVARCHAR(120) NULL")
        else:
            cur.execute("CREATE TABLE IF NOT EXISTS meeting_rooms (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, capacity INTEGER DEFAULT 1, equipment TEXT, status TEXT DEFAULT 'Hoạt động')")
            cur.execute("CREATE TABLE IF NOT EXISTS audit_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, actor TEXT, action TEXT, target TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
            columns = [row[1] for row in cur.execute("PRAGMA table_info(meeting_bookings)").fetchall()]
            if "requester" not in columns:
                cur.execute("ALTER TABLE meeting_bookings ADD COLUMN requester TEXT")
        if not sqlserver:
            cur.execute("INSERT OR IGNORE INTO meeting_rooms (id,name,capacity,equipment,status) VALUES (1,'Phòng họp lớn',20,'Màn hình, camera','Hoạt động'),(2,'Phòng họp nhỏ',8,'Màn hình','Hoạt động'),(3,'Phòng đào tạo',30,'Máy chiếu, bảng','Hoạt động')")


TABLES = ["employees", "attendance", "leave_requests", "recruitment", "training", "payroll", "documents", "meeting_bookings", "reports", "notifications", "users"]
