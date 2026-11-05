import os
from datetime import date
from dotenv import load_dotenv
from flask import Flask
from app.controllers.dashboard import dashboard_bp
from app.controllers.modules import modules_bp
from app.controllers.meetings import meetings_bp
from app.controllers.system import system_bp
from app.models.database import init_db


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
    app.register_blueprint(modules_bp, url_prefix="/module")
    app.register_blueprint(meetings_bp, url_prefix="/meetings")
    app.register_blueprint(system_bp, url_prefix="/system")
    with app.app_context():
        init_db()
    return app
