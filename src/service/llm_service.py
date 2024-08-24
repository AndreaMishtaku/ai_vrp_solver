from src.module.llm import LLMSolver
from src.repository import TripRepository, NodeRepository, VehicleRepository
from src.model import Trip,TripDemands
from src.config.database import db
from sqlalchemy import text
from src.payload import Error
from datetime import datetime


class LLMService:
    def __init__(self):
        self.node_repository=NodeRepository()
        self.vehicle_repository=VehicleRepository()
        self.trip_repository=TripRepository()
        self.solver=LLMSolver()

    def solve(self, request_payload):
        self.check_payload(trip_dict=request_payload)
        try:
            data = fetch_data(request_payload=request_payload)
            prompt_inputs={
                **data,
                "demands": request_payload['demands'],
                "schema": self.solver.parser.get_format_instructions()
            }

            result = self.solver.solve(inputs=prompt_inputs)

            nodes=data['nodes']
            # Save trip to repository
            for route in result['routes']:
                depo=self.node_repository.get_node_by_id(route['route'][0])
                self.node_repository.update_node(depo,{'capacity':depo.capacity-route['load']})
                trip_demands=[]
                for r in route['route'][1:-1]:
                    v_node = next((node for node in nodes if node['id'] == r), None)
                    demand = next((demand['demand'] for demand in request_payload['demands'] if demand["node"] == v_node['name'] ), None)
                    td=TripDemands(node_id=v_node['id'], demand=demand)
                    trip_demands.append(td) 
                trip = Trip(vehicle_id=1 ,depo_id=route['route'][0], total_load=result['total_load'], total_distance=result['total_distance'] , date=datetime.now(),demands=trip_demands)
                self.trip_repository.add_trip(trip)
            return result
        except Exception as e:
            raise Error(message=f'Solution not found! {e}',status_code=400)
        
    def check_payload(self,trip_dict):     
        demands=trip_dict['demands']
        requested_quantity = 0

        for demand in demands:
            if self.node_repository.check_node_by_name(name=demand['node'],is_depo=False) is False:
                raise Error(message=f'Location {demand['node']} not found!',status_code=404)
            else:
                requested_quantity+=demand['demand']
            
        depo_vehicle=trip_dict['depo_vehicle']

        for dv in depo_vehicle:
            if self.node_repository.check_node_by_name(name=dv['depo'],is_depo=True) is False:
                raise Error(message=f'Depo {dv['depo']} not found!',status_code=404)
            else:
                depo=self.node_repository.get_node_by_name(dv['depo'])

                if(depo.capacity<requested_quantity):
                    raise Error(message=f'Not enough quantity in depo',status_code=404)

            if self.vehicle_repository.check_vehicle_by_plate(plate=dv['plate']) is False:
                raise Error(message=f'Vehicle {dv['plate']} not found!',status_code=404)
            
        pass


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
