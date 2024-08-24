from flask_restx import Namespace, Resource, fields
from src.service import BasicService

basic_ns = Namespace('basic', description='Basic operations')
basic_service = BasicService()


node_model=basic_ns.model('Node',{
    'name': fields.String(required=True, description='Name of the node'),
    'latitude':fields.Float(required=True, description='Latitude coordinate'),
    'longitude':fields.Float(required=True, description='Longitude coordinate')
})


vehicle_model=basic_ns.model('Vehicle',{
    'plate': fields.String(required=True, description='License plate'),
    'capacity':fields.Integer(required=True, description='Capacity of the vehicle'),
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

@basic_ns.route('/node/get-all')
class NodesController(Resource):
    def get(self):
        try:
            return basic_service.get_all_nodes(), 200
        except Exception as e:
            return {'message': f'An error occurred {str(e)}'}, 500

@basic_ns.route('/depo/get-all')
class NodesController(Resource):
    def get(self):
        try:
            return basic_service.get_all_depos(), 200
        except Exception as e:
            return {'message': f'An error occurred {str(e)}'}, 500


@basic_ns.route('/trip/<int:id>')
class TripWithParamController(Resource):
    def get(self,id):
        return basic_service.get_trip_by_id(id), 200 


@basic_ns.route('/trip/get-all')
class TripsController(Resource):
    def get(self):
        try:
            return basic_service.get_all_trips(), 200
        except Exception as e:
            return {'message': f'An error occurred {str(e)}'}, 500

@basic_ns.route('/vehicle')
class VehicleController(Resource):
    @basic_ns.expect(vehicle_model)
    def post(self):
        vehicle_dict = basic_ns.payload
        basic_service.create_vehicle(vehicle_dict)
        return {'message': 'Vehicle created successfully'}, 201


        
@basic_ns.route('/vehicle/<int:id>')
class VehicleWithParamController(Resource):
    def get(self,id):
        return basic_service.get_vehicle_by_id(id), 200 

    @basic_ns.expect(vehicle_model)
    def put(self,id):
        vehicle_dict = basic_ns.payload
        basic_service.update_vehicle(id,vehicle_dict)
        return {'message': 'Vehicle updated successfully'}, 201

    def delete(self,id):
        return basic_service.delete_vehicle(id), 204  

@basic_ns.route('/vehicle/get-all')
class VehiclesController(Resource):
    def get(self):
        try:
            return basic_service.get_all_vehicles(), 200
        except Exception as e:
            return {'message': f'An error occurred {str(e)}'}, 500
