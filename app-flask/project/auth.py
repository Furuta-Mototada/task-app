from flask import (
    Blueprint,  # Import Blueprint to create a modular application
    request,  # Import request to handle incoming HTTP requests
)
from flask_login import (
    login_user,  # Import login_user to log in a user
    logout_user,  # Import logout_user to log out a user
    login_required,  # Import login_required to protect routes
    current_user,  # Import current_user to get the currently logged-in user
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)  # Import functions to hash and check passwords
from .models import User, List  # Import User and List models
from . import db  # Import the database instance

# Create a Blueprint named 'auth'
auth = Blueprint("auth", __name__)


# Route to handle user registration
@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()  # Get JSON data from the request
    username = data.get("username")  # Extract username
    password = data.get("password")  # Extract password

    # Check if the username already exists
    if User.query.filter_by(username=username).first():
        return {"message": "Username already exists"}, 400

    # Hash the password and create a new user
    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    # Create default lists for the new user
    todo_list = List(title="Todo", user_id=new_user.id)
    completed_list = List(title="Completed", user_id=new_user.id)

    db.session.add(todo_list)
    db.session.add(completed_list)
    db.session.commit()

    return {"message": "User registered successfully"}, 201


# Route to handle user login
@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()  # Get JSON data from the request
    username = data.get("username")  # Extract username
    password = data.get("password")  # Extract password
    remember = data.get("remember", False)  # Extract remember flag, default to False

    # Query the user by username
    user = User.query.filter_by(username=username).first()

    # Check if user exists and password is correct
    if not user or not check_password_hash(user.password, password):
        return {"message": "Invalid credentials"}, 401

    # Log in the user
    login_user(user, remember=remember)
    return {"message": "Logged in successfully"}, 200


# Route to handle user logout
@auth.route("/logout", methods=["POST"])
@login_required  # Protect the route, user must be logged in
def logout():
    logout_user()  # Log out the user
    return {"message": "Logged out successfully"}, 200


# Route to get the current logged-in user's information
@auth.route("/current_user", methods=["GET"])
@login_required  # Protect the route, user must be logged in
def get_current_user():
    return {"id": current_user.id, "username": current_user.username}, 200


# Route to update the current logged-in user's password
@auth.route("/user", methods=["PUT"])
@login_required  # Protect the route, user must be logged in
def update_user():
    data = request.get_json()  # Get JSON data from the request
    password = data.get("password")  # Extract new password

    # Check if password is provided
    if not password:
        return {"message": "No data provided"}, 400

    # Update the user's password
    current_user.password = generate_password_hash(password, method="pbkdf2:sha256")
    db.session.commit()

    return {"message": "User updated successfully"}, 200


# Route to delete the current logged-in user's account
@auth.route("/user", methods=["DELETE"])
@login_required  # Protect the route, user must be logged in
def delete_user():
    db.session.delete(current_user)  # Delete the user
    db.session.commit()

    return {"message": "User deleted successfully"}, 200
