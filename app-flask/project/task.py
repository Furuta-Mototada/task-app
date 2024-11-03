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

    task_list = List.query.filter_by(id=list_id, user_id=current_user.id).first()
    if not task_list:
        return {"message": "List not found or not authorized"}, 404

    tasks = Task.query.filter_by(list_id=list_id).all()

    tasks_data = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "list_id": task.list_id,
            "parent_id": task.parent_id,
            "is_complete": task.is_complete,
            "is_collapsed": task.is_collapsed,
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
    parent_id = data.get("parent_id")

    if not title or not list_id:
        return {"message": "Task title and list_id are required"}, 400

    task_list = List.query.filter_by(id=list_id, user_id=current_user.id).first()

    if not task_list:
        return {"message": "List not found or not authorized"}, 404

    if task_list.title == "Completed":
        return {"message": "Cannot add tasks to the Completed list"}, 403

    new_task = Task(
        title=title, description=description, list_id=list_id, parent_id=parent_id
    )

    db.session.add(new_task)
    db.session.commit()

    task_data = {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "list_id": new_task.list_id,
        "parent_id": new_task.parent_id,
        "is_complete": new_task.is_complete,
        "is_collapsed": new_task.is_collapsed,
    }

    return jsonify(task_data), 201


@tasks.route("/tasks/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):
    task = (
        Task.query.filter(Task.id == task_id, List.user_id == current_user.id)
        .join(List)
        .first()
    )

    if not task:
        return jsonify({"message": "Task not found or not authorized"}), 404

    db.session.delete(task)
    db.session.commit()

    return (
        jsonify({"message": "Task and all associated subtasks deleted successfully"}),
        200,
    )


@tasks.route("/tasks/<int:task_id>", methods=["PUT"])
@login_required
def update_task(task_id):
    task = (
        Task.query.filter(Task.id == task_id, List.user_id == current_user.id)
        .join(List)
        .first()
    )

    if not task:
        return {"message": "Task not found or not authorized"}, 404

    data = request.get_json()
    new_title = data.get("title")
    new_description = data.get("description")

    if new_title is None:
        return {"message": "New title is required"}, 400

    task.title = new_title
    task.description = new_description
    db.session.commit()

    return {"message": "Task updated successfully"}, 200


@tasks.route("/lists", methods=["GET"])
@login_required
def get_lists():
    lists = List.query.filter_by(user_id=current_user.id).all()
    lists_data = [
        {
            "id": list.id,
            "title": list.title,
        }
        for list in lists
    ]
    return jsonify(lists_data), 200


@tasks.route("/lists", methods=["POST"])
@login_required
def create_list():
    data = request.get_json()
    title = data.get("title") if data else None

    if not title:
        return {"message": "List title is required"}, 400

    if title in ["Todo", "Completed"]:
        return {"message": "Cannot create a list with title 'Todo' or 'Completed'"}, 403

    new_list = List(title=title, user_id=current_user.id)

    db.session.add(new_list)
    db.session.commit()

    list_data = {
        "id": new_list.id,
        "title": new_list.title,
    }

    return jsonify(list_data), 201


@tasks.route("/lists/<int:list_id>", methods=["DELETE"])
@login_required
def delete_list(list_id):
    list = List.query.filter_by(id=list_id, user_id=current_user.id).first()

    if not list:
        return {"message": "List not found or not authorized"}, 404

    if list.title in ["Todo", "Completed"]:
        return {
            "message": "Cannot delete the list with title 'Todo' or 'Completed'"
        }, 403

    db.session.delete(list)
    db.session.commit()

    return {"message": "List and all associated tasks deleted successfully"}, 200


@tasks.route("/lists/<int:list_id>", methods=["PUT"])
@login_required
def update_list_title(list_id):
    list = List.query.filter_by(id=list_id, user_id=current_user.id).first()

    if not list:
        return {"message": "List not found or not authorized"}, 404

    if list.title in ["Todo", "Completed"]:
        return {
            "message": "Cannot modify the list with title 'Todo' or 'Completed'"
        }, 403

    data = request.get_json()
    new_title = data.get("title")

    if not new_title:
        return {"message": "New title is required"}, 400

    list.title = new_title
    db.session.commit()

    return {"message": "List title updated successfully"}, 200


@tasks.route("/tasks/<int:task_id>/expand", methods=["PUT"])
@login_required
def expand_task(task_id):
    task = (
        Task.query.filter(Task.id == task_id, List.user_id == current_user.id)
        .join(List)
        .first()
    )

    if not task:
        return {"message": "Task not found or not authorized"}, 404

    data = request.get_json()
    collapsed = data.get("is_collapsed")

    task.is_collapsed = collapsed
    db.session.commit()

    return {"message": "Task expanded successfully"}, 200


@tasks.route("/tasks/<int:task_id>/complete", methods=["PUT"])
@login_required
def complete_task(task_id):
    task = (
        Task.query.filter(Task.id == task_id, List.user_id == current_user.id)
        .join(List)
        .first()
    )

    if not task:
        return {"message": "Task not found or not authorized"}, 404

    complete_list = List.query.filter_by(
        title="Completed", user_id=current_user.id
    ).first()
    todo_list = List.query.filter_by(title="Todo", user_id=current_user.id).first()
    data = request.get_json()
    completed = data.get("is_complete")

    def complete_subtasks(subtask, completed, is_root):
        subtask.is_complete = completed
        if is_root:
            subtask.list_id = complete_list.id if completed else todo_list.id
        for child in subtask.sub_tasks:
            complete_subtasks(child, completed, is_root)

    if task.parent_id is None:
        task.is_complete = completed
        if completed:
            task.list_id = complete_list.id
        else:
            task.list_id = todo_list.id
        db.session.commit()

        for subtask in task.sub_tasks:
            complete_subtasks(subtask, completed, is_root=True)
        db.session.commit()
    else:
        task.is_complete = completed

        for subtask in task.sub_tasks:
            complete_subtasks(subtask, completed, is_root=False)
        db.session.commit()

    return {"message": "Task completed successfully"}, 200


@tasks.route("/tasks/<int:task_id>/move", methods=["PUT"])
@login_required
def move_task(task_id):
    task = (
        Task.query.filter(Task.id == task_id, List.user_id == current_user.id)
        .join(List)
        .first()
    )

    if not task:
        return {"message": "Task not found or not authorized"}, 404

    if task.parent_id is not None:
        return {"message": "Cannot move subtasks"}, 403

    title = task.list.title

    data = request.get_json()
    new_list_id = data.get("list_id")

    # Check if the new list exists and belongs to the current user
    new_list = List.query.filter_by(id=new_list_id, user_id=current_user.id).first()
    if not new_list:
        return {"message": "New list not found or not authorized"}, 404

    task.list_id = new_list_id
    if new_list.title == "Completed":
        task.is_complete = True
    elif title == "Completed":
        task.is_complete = False
    db.session.commit()

    # If the task has subtasks, update their list_id as well
    def update_subtasks(task, new_list_id, moving, completed):
        for subtask in task.sub_tasks:
            subtask.list_id = new_list_id
            if moving:
                subtask.is_complete = completed
            update_subtasks(
                subtask, new_list_id, moving, completed
            )  # Recursive call to update subtasks

    if new_list.title == "Completed":
        update_subtasks(task, new_list_id, moving=True, completed=True)
    elif title == "Completed":
        update_subtasks(task, new_list_id, moving=True, completed=False)
    else:
        update_subtasks(task, new_list_id, moving=False, completed=False)

    db.session.commit()

    return {"message": "Task and its subtasks moved successfully"}, 200
