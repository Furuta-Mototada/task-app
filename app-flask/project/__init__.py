from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager

# Initialize the SQLAlchemy object
db = SQLAlchemy()


def create_app():
    # Create a Flask application instance
    app = Flask(__name__)

    # Set configuration variables
    app.config["SECRET_KEY"] = "dev"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["debug"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_SECURE"] = True

    # Initialize the database with the app
    db.init_app(app)

    # Initialize the login manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(
        app,
        resources={r"/api/*": {"origins": "http://localhost:3000"}},
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    # Import the User model
    from .models import User

    # Define the user loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register the tasks blueprint
    from .task import tasks as tasks_blueprint

    app.register_blueprint(tasks_blueprint, url_prefix="/api")

    # Import and register the auth blueprint
    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/api/auth")

    # Define the index route
    @app.route("/")
    def index():
        return render_template("index.html")

    # Define a custom CLI command to initialize the database
    @app.cli.command("init-db")
    def init_db():
        """Initialize the database."""
        with app.app_context():
            db.create_all()
        print("Initialized the database.")

    # Initialize the database within the app context
    with app.app_context():
        db.create_all()

    return app
