from werkzeug.security import generate_password_hash
import argparse
import getpass

from project import db, create_app
from project.models import User


def main():
    parser = argparse.ArgumentParser(description="A script to add admin users to the sqlite database.")

    parser.add_argument("-e", "--email", type=str, nargs=1,
                        metavar="email", default="none",
                        help="Email to use for admin creation")
    parser.add_argument("-u", "--username", type=str, nargs=1,
                        metavar="user_name", default="none",
                        help="Username to use for admin creation")

    args = parser.parse_args()
    if args.email is not None and args.username is not None:
        create_admin(args)


def create_admin(args):
    password = getpass.getpass("Enter a password.")

    admin_user = User(email=args.email[0], password=generate_password_hash(password, method='sha256'),
                      name=args.username[0],
                      role="admin")

    app = create_app()
    with app.app_context():
        db.session.add(admin_user)
        db.session.commit()


if __name__ == "__main__":
    main()
