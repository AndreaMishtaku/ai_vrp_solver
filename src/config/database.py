import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from src.utils.mysql import create_database_if_not_exists

username = os.getenv('MYSQL_USERNAME')
password = os.getenv('MYSQL_PASSWORD')
db_name = os.getenv('MYSQL_DB_NAME')
host = os.getenv('MYSQL_HOST', 'localhost')
port = os.getenv('MYSQL_PORT', 3306)
connection_uri=f'mysql+mysqldb://{username}:{password}@{host}'

create_database_if_not_exists(connection_uri,db_name)

SQLALCHEMY_DATABASE_URI = connection_uri+ f'/{db_name}'

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)