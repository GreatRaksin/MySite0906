from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from habrClone import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(20))
    avatar = db.Column(db.String(20), default='default.jpg')
    news = db.relationship('New', backref='author', lazy=True)
    zvonki = db.relationship('Zvonok', backref='author', lazy=True)

    def __repr__(self):
        return f'Пользователь: {self.username}, email {self.email}'

    def set_password(self, user_pass):
        self.password = generate_password_hash(user_pass)

    def check_password(self, user_pass):
        return check_password_hash(self.password, user_pass)


class New(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article = db.Column(db.String(100))
    publish_date = db.Column(db.DateTime, default=datetime.utcnow)
    body = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Zvonok(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    phone = db.Column(db.String(40))

    user_username = db.Column(db.String(20), db.ForeignKey('user.username'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
