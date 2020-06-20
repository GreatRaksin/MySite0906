from habrClone import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(20))
    avatar = db.Column(db.String(20), default='default.jpg')
    news = db.relationship('New', backref='author', lazy=True)

    def __repr__(self):
        return f'Пользователь: {self.username}, email {self.email}'


class New(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article = db.Column(db.String(100))
    publish_date = db.Column(db.DateTime, default=datetime.utcnow)
    body = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

