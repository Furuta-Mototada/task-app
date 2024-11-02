from flask import Blueprint, request, jsonify
from .models import Task, List
from . import db
from flask_login import current_user, login_required

tasks = Blueprint("tasks", __name__)


@tasks.route("/tasks", methods=["GET"])
@login_required
def get_tasks():
    list_id = request.args.get("list_id")

    if not list_id:
        return {"message": "List ID is required"}, 400

    tasks = Task.query.filter_by(list_id=list_id).all()

    tasks_data = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "list_id": task.list_id,
        }
        for task in tasks
    ]

    return jsonify(tasks_data), 200


@tasks.route("/tasks", methods=["POST"])
@login_required
def create_task():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    list_id = data.get("list_id")

    if not title or not list_id:
        return {"message": "Task title and list_id are required"}, 400

    task_list = List.query.filter_by(id=list_id, user_id=current_user.id).first()

    if not task_list:
        return {"message": "List not found or not authorized"}, 404

    new_task = Task(title=title, description=description, list_id=list_id)

    db.session.add(new_task)
    db.session.commit()

    task_data = {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "list_id": new_task.list_id,
    }

    return jsonify(task_data), 201


@tasks.route("/lists", methods=["GET"])
@login_required
def get_lists():
    lists = List.query.filter_by(user_id=current_user.id).all()
    lists_data = [{"id": list.id, "title": list.title} for list in lists]
    return jsonify(lists_data), 200


@tasks.route("/lists", methods=["POST"])
@login_required
def create_list():
    data = request.get_json()
    title = data.get("title") if data else None

    if not title:
        return {"message": "List title is required"}, 400

    new_list = List(title=title, user_id=current_user.id)

    db.session.add(new_list)
    db.session.commit()

    list_data = {
        "id": new_list.id,
        "title": new_list.title,
        "user_id": new_list.user_id,
    }

    return jsonify(list_data), 201
