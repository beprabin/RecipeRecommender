from sqlalchemy.orm import backref

from app import db

from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False, unique=True)

    def __repr__(self):
        return '<User %r>' % self.username


class Favourite(db.Model):
    __tablename__ = "favourite"

    def __init__(self):
        id = self.id
        recipe = self.recipe

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref=backref("request", uselist=False), foreign_keys=[user_id])

    recipe = db.Column(db.String(100))

    def __repr__(self):
        return self.recipe

# request = Request.query.first()
# print(request.agent.name)
#
# agent = Agent.query.first()
# print(agent.request.applicationdate)
