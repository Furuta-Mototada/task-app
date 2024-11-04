from . import db
from datetime import datetime
from flask_login import UserMixin


# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(80), nullable=False, unique=True)  # Unique username
    password = db.Column(db.String(200), nullable=False)  # Password
    lists = db.relationship(
        "List", back_populates="user", cascade="all, delete-orphan"
    )  # Relationship to List


# List model
class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    title = db.Column(db.String(120), nullable=False)  # List title
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )  # Foreign key to User
    user = db.relationship("User", back_populates="lists")  # Relationship to User
    tasks = db.relationship(
        "Task", back_populates="list", cascade="all, delete-orphan"
    )  # Relationship to Task


# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    title = db.Column(db.String(255), nullable=False)  # Task title
    description = db.Column(db.String(511), nullable=True)  # Task description
    created = db.Column(
        db.DateTime, default=datetime.now, nullable=False
    )  # Creation timestamp
    is_complete = db.Column(db.Boolean, default=False)  # Completion status
    is_collapsed = db.Column(db.Boolean, default=False)  # Collapse status
    list_id = db.Column(
        db.Integer, db.ForeignKey("list.id"), nullable=False
    )  # Foreign key to List

    list = db.relationship("List", back_populates="tasks")  # Relationship to List

    parent_id = db.Column(
        db.Integer, db.ForeignKey("task.id"), nullable=True
    )  # Foreign key to parent Task
    parent = db.relationship(
        "Task", remote_side=[id], back_populates="sub_tasks"
    )  # Relationship to parent Task
    sub_tasks = db.relationship(
        "Task", back_populates="parent", cascade="all, delete-orphan"
    )  # Relationship to sub-tasks
