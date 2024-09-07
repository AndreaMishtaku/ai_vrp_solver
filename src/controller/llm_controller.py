from flask_restx import Namespace, Resource, fields
from flask import request
from src.service import LLMService
from src.enums.llm_model_name import LLM_ModelName
from src.payload import Error

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
    'depo_vehicle':fields.List(fields.Nested(depo_vehicle_model),required=True),
})

@llm_ns.route('/<string:model_name>/vrp')
class LLMController(Resource):
    @llm_ns.expect(trip_model)
    @llm_ns.doc(params={
        'model_name': 'The model name to use (e.g., gpt-4o, gpt-3.5, claude-3-sonnet, claude-3-sonnet)',
        'reference': 'An optional reference'
    })
    def post(self, model_name):
        reference = request.args.get('reference')
        try:
            model = LLM_ModelName(model_name)
        except ValueError:
            raise Error(message='Model not found!',status_code=404)
        
        trip_dict = llm_ns.payload
        return llm_service.solve(trip_dict, model ,reference), 200