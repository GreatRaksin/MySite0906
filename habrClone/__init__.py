from flask import Flask  # из библиотеки flask импортируем КЛАСС Flask
from config import Config

App = Flask(__name__)
App.config.from_object(Config)

from habrClone import routes  # импортировали маршруты
