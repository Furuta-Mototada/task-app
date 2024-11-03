from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "dev"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["debug"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_SECURE"] = True

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    CORS(
        app,
        resources={r"/api/*": {"origins": "http://localhost:3000"}},
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .task import tasks as tasks_blueprint

    app.register_blueprint(tasks_blueprint, url_prefix="/api")

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/api/auth")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.cli.command("init-db")
    def init_db():
        """Initialize the database."""
        with app.app_context():
            db.create_all()
        print("Initialized the database.")

    with app.app_context():
        db.create_all()  # Initialize the database

    return app
