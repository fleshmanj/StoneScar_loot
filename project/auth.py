from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from project import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        return {"msg": "User does not exist or incorrect password"}, 200

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return {"msg": "User logged in"}, 200


@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    role = "user"

    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        return {"msg": "User already has an account"}, 200

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), role=role)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return {"msg": "User has registered"}, 200


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return {"msg": "User has logged out"}, 200