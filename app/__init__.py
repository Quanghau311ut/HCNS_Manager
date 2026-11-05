import os
from datetime import date
from dotenv import load_dotenv
from flask import Flask
from app.controllers.dashboard import dashboard_bp
from app.controllers.system import system_bp
from app.models.database import init_db
from app.modules import BLUEPRINTS
from app.controllers.auth import auth_bp
from app.auth import can_book_meetings, is_admin, register_auth


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY") or os.urandom(32),
        DEBUG=os.getenv("FLASK_DEBUG", "0") == "1",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.getenv("SESSION_COOKIE_SECURE", "0") == "1",
    )
    @app.context_processor
    def inject_date():
        return {"today": date.today().strftime("%d/%m/%Y")}
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)
    for blueprint in BLUEPRINTS:
        key = blueprint.name.removeprefix("module_")
        app.register_blueprint(blueprint, url_prefix=f"/module/{key}")
    app.register_blueprint(system_bp, url_prefix="/system")
    register_auth(app)
    @app.context_processor
    def inject_permissions():
        return {"is_admin": is_admin(), "can_book": can_book_meetings()}
    with app.app_context():
        init_db()
    return app
