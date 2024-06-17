from src.payload.error import Error 

def register_error_handlers(app):
    @app.errorhandler(Error)
    def handle_custom_error(error):
        return error.to_dict(), error.status_code

    @app.errorhandler(Exception)
    def handle_general_error(error):
        return {'message': f'An internal error occurred {str(error)}'}, 500