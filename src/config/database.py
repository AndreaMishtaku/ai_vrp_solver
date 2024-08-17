import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,text

username = os.getenv('MYSQL_USERNAME')
password = os.getenv('MYSQL_PASSWORD')
db_name = os.getenv('MYSQL_DB_NAME')
host = os.getenv('MYSQL_HOST', 'localhost')
port = os.getenv('MYSQL_PORT', 3306)
connection_uri=f'mysql+mysqldb://{username}:{password}@{host}'


def create_database_if_not_exists(connection_uri,db_name):
    engine = create_engine(connection_uri)
    conn = engine.connect()  
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
    conn.close()


create_database_if_not_exists(connection_uri,db_name)

SQLALCHEMY_DATABASE_URI = connection_uri+ f'/{db_name}'

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)