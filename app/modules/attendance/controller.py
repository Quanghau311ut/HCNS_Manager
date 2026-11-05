from app.modules.common.controller import create_module_blueprint
from app.modules.attendance.model import AttendanceModel

blueprint = create_module_blueprint("attendance", AttendanceModel)
