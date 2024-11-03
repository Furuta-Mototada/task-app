from flask import (
    Blueprint,
    request,
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, List
from . import db


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if User.query.filter_by(username=username).first():
        return {"message": "Username already exists"}, 400

    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    todo_list = List(title="Todo", user_id=new_user.id)
    completed_list = List(title="Completed", user_id=new_user.id)

    db.session.add(todo_list)
    db.session.add(completed_list)

    db.session.commit()

    return {"message": "User registered successfully"}, 201


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    remember = data.get("remember", False)

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return {"message": "Invalid credentials"}, 401

    login_user(user, remember=remember)
    return {"message": "Logged in successfully"}, 200


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return {"message": "Logged out successfully"}, 200


@auth.route("/current_user", methods=["GET"])
@login_required
def get_current_user():
    return {"id": current_user.id, "username": current_user.username}, 200


@auth.route("/user", methods=["PUT"])
@login_required
def update_user():
    data = request.get_json()
    password = data.get("password")

    if not password:
        return {"message": "No data provided"}, 400

    current_user.password = generate_password_hash(password, method="pbkdf2:sha256")

    db.session.commit()

    return {"message": "User updated successfully"}, 200


@auth.route("/user", methods=["DELETE"])
@login_required
def delete_user():
    db.session.delete(current_user)
    db.session.commit()

    return {"message": "User deleted successfully"}, 200
