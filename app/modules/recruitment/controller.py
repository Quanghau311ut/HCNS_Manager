from app.modules.common.controller import create_module_blueprint
from app.modules.recruitment.model import RecruitmentModel

blueprint = create_module_blueprint("recruitment", RecruitmentModel)
