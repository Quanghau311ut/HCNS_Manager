from app.modules.common.controller import create_module_blueprint
from app.modules.training.model import TrainingModel

blueprint = create_module_blueprint("training", TrainingModel)
