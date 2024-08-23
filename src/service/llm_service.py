from src.module.llm import LLMSolver
from src.config.database import db
from sqlalchemy import text
from src.payload import Error


class LLMService:
    def solve(self, request_payload):
        try:
            solver = LLMSolver()
            data = fetch_data(request_payload=request_payload)
            prompt_inputs={
                **data,
                "demands": request_payload['demands'],
                "schema": solver.parser.get_format_instructions()
            }
            print(prompt_inputs)
            result = solver.solve(inputs=prompt_inputs)
            return result
        except Exception:
            raise Error(message=f'Solution not found',status_code=400)


def fetch_data(request_payload):
    depo_names = [depo_vehicle['depo'] for depo_vehicle in request_payload["depo_vehicle"]]
    node_names = [demand["node"] for demand in request_payload["demands"]]
    vehicle_plates = [depo_vehicle['plate'] for depo_vehicle in request_payload["depo_vehicle"]]
        
    nodes=query_data(table='node', attributes=['name'], valueList=node_names)
    filtered_nodes = [{'id': node['id'], 'name': node['name'], 'latitude': node['latitude'], 'longitude': node['longitude']} for node in nodes]
    depos=query_data(table='node', attributes=['name'], valueList=depo_names)
    filtered_depos = [{'id': depo['id'], 'name': depo['name'], 'latitude': depo['latitude'], 'longitude': depo['longitude'], 'capacity':depo['capacity']} for depo in depos]
    vehicles=query_data(table='vehicle', attributes=['plate'], valueList=vehicle_plates)

    ids= [node['id'] for node in nodes]+ [depo['id'] for depo in depos]
        
    edges=query_data(table='edge', attributes=['start_node_id', 'end_node_id'], valueList=ids)
    filtered_edges = [{'start_node_id': edge['start_node_id'], 'end_node_id': edge['end_node_id'], 'distance': edge['distance']} for edge in edges]
        
    return {
            "nodes": filtered_nodes,
            "depos": filtered_depos,
            "edges": filtered_edges,
            "vehicles": vehicles
        }
    
def query_data(table, attributes, valueList):
    value_list_str = ', '.join([f"'{value}'" for value in valueList])

    conditions = ' AND '.join([f"{attr} IN ({value_list_str})" for attr in attributes])
    sql_query=text(f"SELECT * FROM {table}  WHERE {conditions}")

    result = db.session.execute(sql_query)
    return result.mappings().all()