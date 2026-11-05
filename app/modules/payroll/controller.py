from app.modules.common.controller import create_module_blueprint
from app.modules.payroll.model import PayrollModel

blueprint = create_module_blueprint("payroll", PayrollModel)
