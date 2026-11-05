from app.modules.common.controller import create_module_blueprint
from app.modules.users.model import UserModel

blueprint = create_module_blueprint("users", UserModel)
