from flask import Response, json, jsonify, request
from flask_restx import Namespace, Resource
from src.utils.file import read_excel_file
from src.service import ImportService

import_ns = Namespace('import', description='Import data from exel')
import_service = ImportService()


@import_ns.route('/')
class DataImportController(Resource):
    @import_ns.doc('upload_file')
    @import_ns.expect(import_ns.parser().add_argument('locations', location='files', type='file'))
    def post(self):
        uploaded_file = request.files['locations']

        if uploaded_file.filename == '':
            return {'message': 'No file selected for uploading'}, 400
        
        try:
            locations=read_excel_file(uploaded_file,['Name','Latitude', 'Longitude'])
            return  import_service.add_node(locations), 200
        except Exception as e:
            return {'message': f'An error occurred while processing the file: {str(e)}'}, 500