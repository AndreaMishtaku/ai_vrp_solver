from flask_restx import Namespace, Resource, fields
from flask import request
from src.service import ORToolsService
from src.service import ORToolsTWService

ortools_ns = Namespace('ortools', description='Vehicle routing problem (Google)')
ortools_service = ORToolsService()
ortools_tw_service = ORToolsTWService()


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

@ortools_ns.route('/cc/vrp')
class ORToolsController(Resource):
    @ortools_ns.expect(trip_model)
    @ortools_ns.doc(params={
        'reference': 'An optional reference'
    })
    def post(self):
        reference = request.args.get('reference')
        trip_dict = ortools_ns.payload 
        return ortools_service.routing_model(trip_dict,reference), 200
    
@ortools_ns.route('/tw/vrp')
class ORToolsController(Resource):
    @ortools_ns.expect(trip_model)
    def post(self):
        trip_dict = ortools_ns.payload 
        return ortools_tw_service.routing_model(trip_dict), 200