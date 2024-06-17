from flask import Flask
from dotenv import load_dotenv
from src.config.database import init_db
from src.handler import register_error_handlers
from src.controller import init_api


load_dotenv()

def create_app():
    app = Flask(__name__)
    init_db(app)    
    init_api(app)
    register_error_handlers(app)
    return app