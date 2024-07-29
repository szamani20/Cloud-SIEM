from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    This User model is only for webserver local SQLite database. The User model is only used
    for authentication of Lambdas within customers' AWS that call the endpoints of webserver
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
