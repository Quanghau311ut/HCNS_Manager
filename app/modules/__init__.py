"""Feature modules. Each feature owns its Model, View and Controller."""
from app.modules.employees.controller import blueprint as employees
from app.modules.attendance.controller import blueprint as attendance
from app.modules.leave_requests.controller import blueprint as leave_requests
from app.modules.recruitment.controller import blueprint as recruitment
from app.modules.training.controller import blueprint as training
from app.modules.payroll.controller import blueprint as payroll
from app.modules.documents.controller import blueprint as documents
from app.modules.reports.controller import blueprint as reports
from app.modules.notifications.controller import blueprint as notifications
from app.modules.users.controller import blueprint as users
from app.modules.meetings.controller import blueprint as meetings

BLUEPRINTS = [employees, attendance, leave_requests, recruitment, training,
              payroll, documents, reports, notifications, users, meetings]
