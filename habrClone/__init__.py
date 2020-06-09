from flask import Flask  # из библиотеки flask импортируем КЛАСС Flask

App = Flask(__name__)

from habrClone import routes  # импортировали маршруты
