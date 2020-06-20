from flask import Flask  # из библиотеки flask импортируем КЛАСС Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

App = Flask(__name__)
App.config.from_object(Config)
db = SQLAlchemy(App)
migrate = Migrate(App, db)
login = LoginManager(App)

from habrClone import routes, models  # импортировали маршруты
