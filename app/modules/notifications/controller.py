from app.modules.common.controller import create_module_blueprint
from app.modules.notifications.model import NotificationModel

blueprint = create_module_blueprint("notifications", NotificationModel)
