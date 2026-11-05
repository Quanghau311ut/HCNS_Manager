from app.modules.common.controller import create_module_blueprint
from app.modules.leave_requests.model import LeaveRequestModel

blueprint = create_module_blueprint("leave_requests", LeaveRequestModel)
