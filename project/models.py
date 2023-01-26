from . import db
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    role = db.Column(db.String(255))
    confirmed_at = db.Column(db.DateTime())


class MyModelView(ModelView):
    def is_accessible(self):

        if current_user.is_authenticated:
            if current_user.role == "admin":
                return True
        else:
            return False


class Normal_Raid(UserMixin, db.Model):
    __tablename__ = "normal_raid"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    boss = db.Column(db.String(100))
    item = db.Column(db.String(100))


class Heroic_Raid(UserMixin, db.Model):
    __tablename__ = "heroic_raid"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    boss = db.Column(db.String(100))
    item = db.Column(db.String(100))


class Mythic_Raid(UserMixin, db.Model):
    __tablename__ = "mythic_raid"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    boss = db.Column(db.String(100))
    item = db.Column(db.String(100))
