import os
from datetime import date
from dotenv import load_dotenv
from flask import Flask
from app.controllers.dashboard import dashboard_bp
from app.controllers.system import system_bp
from app.models.database import init_db
from app.modules import BLUEPRINTS


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", "change-this-before-deployment"),
        DEBUG=os.getenv("FLASK_DEBUG", "0") == "1",
    )
    @app.context_processor
    def inject_date():
        return {"today": date.today().strftime("%d/%m/%Y")}
    app.register_blueprint(dashboard_bp)
    for blueprint in BLUEPRINTS:
        key = blueprint.name.removeprefix("module_")
        app.register_blueprint(blueprint, url_prefix=f"/module/{key}")
    app.register_blueprint(system_bp, url_prefix="/system")
    with app.app_context():
        init_db()
    return app
