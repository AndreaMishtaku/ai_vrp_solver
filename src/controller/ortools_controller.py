from flask_restx import Namespace, Resource, fields
from src.service import ORToolsService

ortools_ns = Namespace('ortools', description='Vehicle routing problem (Google)')
ortools_service = ORToolsService()


demand_model = ortools_ns.model('Demand', {
    'node': fields.String(),
    'demand': fields.Integer()
})

depo_vehicle_model=ortools_ns.model('Vehicle_Depo', {
    'depo': fields.String(),
    'plate': fields.String()
})

trip_model=ortools_ns.model('Trip',{
    'demands':fields.List(fields.Nested(demand_model),required=True),
    'depo_vehicle':fields.List(fields.Nested(depo_vehicle_model),required=True)
})

@ortools_ns.route('/vrp')
class ORToolsController(Resource):
    @ortools_ns.expect(trip_model)
    def post(self):
        trip_dict = ortools_ns.payload 
        return ortools_service.routing_model(trip_dict), 200