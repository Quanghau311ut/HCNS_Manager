from app.modules.common.controller import create_module_blueprint
from app.modules.employees.model import EmployeeModel

blueprint = create_module_blueprint("employees", EmployeeModel)
