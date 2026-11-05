from app.modules.common.controller import create_module_blueprint
from app.modules.reports.model import ReportModel

blueprint = create_module_blueprint("reports", ReportModel)
