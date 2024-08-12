from flask_restx import Api
from .data_import_controller import import_ns
from .basic_controller import basic_ns
from .ortools_controller import ortools_ns


api = Api( title='Vehicle Routing Problem API',
          version='1.0',
          description='API for solving vehicle routing problems using AI techniques'
          )

def init_api(app):
    api.init_app(app)
    api.add_namespace(import_ns)
    api.add_namespace(basic_ns)
    api.add_namespace(ortools_ns)






