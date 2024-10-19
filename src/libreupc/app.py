from flask import Flask, Response, render_template, request

from ._version import __version__
from .archives import archives_blueprint
from .auth import Users, auth_blueprint
from .extensions import db, login_manager, migrate, socketio
from .helpers import ResponseHelper, bash, database


@login_manager.user_loader
def load_user(user_id):
    return database.get_by_id(Users, int(user_id))


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    socketio.init_app(app)

    @app.context_processor
    def utility_processor():
        return {
            "version": __version__,
            "dev_repo_path": "/tmp/borgdrone",
        }

    @app.before_request
    def before_request():
        if request.endpoint != "static":
            # if not request.headers.get("Content-Type"):
            #     logger.debug(request.headers, "red")

            hx_request = request.headers.get("HX-Request", False)
            frag_redirect = request.headers.get("BD-HX-Location", False)

            ResponseHelper.request_method = request.method
            ResponseHelper.endpoint = request.endpoint
            ResponseHelper.hx_request = hx_request
            ResponseHelper.frag_redirect = frag_redirect

    @app.after_request
    def after_request(response: Response) -> Response:
        # logger.debug(response.headers, "yellow")
        return response

    with app.app_context():

        db.create_all()
        init_db_data(app)
        app.register_blueprint(auth_blueprint, url_prefix="/auth")
        app.register_blueprint(bundles_blueprint, url_prefix="/bundles")
        app.register_blueprint(repositories_blueprint, url_prefix="/repositories")
        app.register_blueprint(archives_blueprint, url_prefix="/archives")
        app.register_blueprint(dashboard_blueprint, url_prefix="/")
        app.register_blueprint(settings_blueprint, url_prefix="/settings")
        app.register_blueprint(logs_blueprint, url_prefix="/logs")

        from .logging.config import configure_logging

        configure_logging()

        from .logging import logger

        logger.debug("Borgdrone Started", "yellow")

        return app


def init_db_data(app: Flask):
    if not database.get_by_id(Users, 1):
        Users().create(app.config["DEFAULT_USER"], app.config["DEFAULT_PASSWORD"])
        # SettingsManager().create(user_id=user.id)
