from flask_restx import Namespace, Resource, fields
from src.service import BasicService

basic_ns = Namespace('basic', description='Basic operations')
basic_service = BasicService()


node_model=basic_ns.model('Node',{
    'name': fields.String(required=True, description='Name of the node'),
    'latitude':fields.Float(required=True, description='Latitude coordinate'),
    'longitude':fields.Float(required=True, description='Longitude coordinate')
})


@basic_ns.route('/node')
class NodeController(Resource):
    @basic_ns.expect(node_model)
    def post(self):
        node_dict = basic_ns.payload
        basic_service.create_node(node_dict)
        return {'message': 'Node created successfully'}, 201


        
@basic_ns.route('/node/<int:id>')
class NodeWithParamController(Resource):
    def get(self,id):
        return basic_service.get_node_by_id(id), 200 

    @basic_ns.expect(node_model)
    def put(self,id):
        node_dict = basic_ns.payload
        basic_service.update_node(id,node_dict)
        return {'message': 'Node updated successfully'}, 201

    def delete(self,id):
        return basic_service.delete_node(id), 204  

    

@basic_ns.route('/get-all-nodes')
class NodesController(Resource):
    def get(self):
        try:
            return basic_service.get_all_nodes(), 200
        except Exception as e:
            return {'message': f'An error occurred while processing the file: {str(e)}'}, 500
        

@basic_ns.route('/get-all-depos')
class NodesController(Resource):
    def get(self):
        try:
            return basic_service.get_all_depos(), 200
        except Exception as e:
            return {'message': f'An error occurred while processing the file: {str(e)}'}, 500
        