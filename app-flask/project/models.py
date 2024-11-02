from . import db
from datetime import datetime
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    lists = db.relationship("List", back_populates="user")


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="lists")
    tasks = db.relationship("Task", back_populates="list")


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(511))
    created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    is_complete = db.Column(db.Boolean, default=False)
    is_collapsed = db.Column(db.Boolean, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey("list.id"), nullable=False)

    list = db.relationship("List", back_populates="tasks")

    parent_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=True)
    parent = db.relationship("Task", remote_side=[id], back_populates="sub_tasks")
    sub_tasks = db.relationship("Task", back_populates="parent")
