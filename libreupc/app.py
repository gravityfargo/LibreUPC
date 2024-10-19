from flask import Flask, Response

from libreupc.extensions import db, migrate


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://libreupc:PASSWORD@10.10.10.20:3306/libreupc"
    db.init_app(app)
    migrate.init_app(app, db)

    @app.context_processor
    def utility_processor():
        return {}

    @app.before_request
    def before_request():
        pass

    @app.after_request
    def after_request(response: Response) -> Response:
        return response

    with app.app_context():
        db.create_all()
        return app


# https://api.bestbuy.com/click/-/6537139/pdp?IPID=79301
# https://www.bestbuy.com/site/searchpage.jsp?&st=6537139
