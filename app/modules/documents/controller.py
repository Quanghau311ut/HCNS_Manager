from app.modules.common.controller import create_module_blueprint
from app.modules.documents.model import DocumentModel

blueprint = create_module_blueprint("documents", DocumentModel)
