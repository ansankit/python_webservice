# app/__init__.py
from flask import Flask
from app.routes import create_routes
from app.mysql_repo import MySQLRepo
from app.file_repo import FileRepo

def create_app(storage_type='mysql'):
    app = Flask(__name__)

    if storage_type == 'file':
        repo = FileRepo('employees.json')
    else:
        repo = MySQLRepo({
            'host': 'localhost',
            'user': 'root',
            'password': 'yourpassword',
            'database': 'testdb'
        })

    app.register_blueprint(create_routes(repo))
    return app