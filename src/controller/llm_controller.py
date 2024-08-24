from flask_restx import Namespace, Resource, fields
from src.service import LLMService

llm_ns = Namespace('llm', description='Vehicle routing problem (Open AI, Anthropic)')
llm_service = LLMService()

demand_model = llm_ns.model('Demand', {
    'node': fields.String(),
    'demand': fields.Integer()
})

depo_vehicle_model=llm_ns.model('Vehicle_Depo', {
    'depo': fields.String(),
    'plate': fields.String()
})

trip_model=llm_ns.model('Trip',{
    'demands':fields.List(fields.Nested(demand_model),required=True),
    'depo_vehicle':fields.List(fields.Nested(depo_vehicle_model),required=True)
})

@llm_ns.route('/vrp')
class LLMController(Resource):
    @llm_ns.expect(trip_model)
    def post(self):
        trip_dict = llm_ns.payload 
        return llm_service.solve(trip_dict), 200