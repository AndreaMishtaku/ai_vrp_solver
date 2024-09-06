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
            depos, nodes, vehicles, edges = fetch_data(request_payload=request_payload)
            locations_str, vehicle_depo_str, distances_str = get_formatted_data(depos, nodes, edges, vehicles, request_payload['demands'], request_payload['depo_vehicle'])
            
            prompt_inputs={
                'locations':locations_str,
                'distances': distances_str,
                'vehicle_depo':  vehicle_depo_str,
                "schema": self.solver.parser.get_format_instructions()
            }

            result = self.solver.solve(inputs=prompt_inputs)

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
    depos=query_data(table='node', attributes=['name'], valueList=depo_names)
    vehicles=query_data(table='vehicle', attributes=['plate'], valueList=vehicle_plates)

    ids= [node['id'] for node in nodes]+ [depo['id'] for depo in depos]
        
    edges=query_data(table='edge', attributes=['start_node_id', 'end_node_id'], valueList=ids)
        
    return depos, nodes, vehicles, edges

def get_formatted_data(depos, nodes, edges, vehicles, demands, vehicle_depo):
    locations=depos+nodes
    location_index_map = {location['id']: idx for idx, location in enumerate(locations)}
    n = len(locations)

    # Initializing the matrix
    distance_matrix = [[0 if i == j else float('inf') for j in range(n)] for i in range(n)]

    # Fill the distance matrix with the given edges
    for edge in edges:
        start_id = edge['start_node_id']
        end_id = edge['end_node_id']
        distance = edge['distance']
        # Find the indices of the start and end locations
        start_idx = location_index_map[start_id]
        end_idx = location_index_map[end_id]
        distance_matrix[start_idx][end_idx] = distance


    # Provide location info
    location_strings = [
        f"Depo {location['id']}: {location['name']} with capacity {location['capacity']}\n"
        if location['type'] == 'DEPO' else 
        f"Node {location['id']}: {location['name']} with demand: {next((demand['demand'] for demand in demands if demand['node'] == location['name']), None)}\n"
        for location in locations
    ]

    locations_str = ''.join(location_strings)

    distance_strings = []
    processed_pairs = []  # List to keep track of processed pairs
    
    for i in range(n):
        for j in range(n):
            if i != j:
                start_id = locations[i]['id']
                end_id = locations[j]['id']
                
                
                pair = (start_id, end_id)
                reverse_pair = (end_id, start_id)
                
                if pair in processed_pairs or reverse_pair in processed_pairs:
                    continue
                
                distance = distance_matrix[i][j]
                reverse_distance = distance_matrix[j][i]
                
                if distance != float('inf') and reverse_distance != float('inf'):
                    distance_strings.append(f"{start_id} to {end_id}: {distance} and {end_id} to {start_id}: {reverse_distance}, ")
                
                processed_pairs.append(pair)
    
    distances_str = ', '.join(distance_strings)

    vehicle_depo_str='Depo | Vehicle\n'
    for vd in vehicle_depo:
        vehicle = next((v for v in vehicles if v['plate'] == vd['plate']), None)
        vehicle_depo_str+= f"{vd['depo']} | Vehicle-> Plate: {vehicle['plate']}, Capacity: {vehicle['capacity']}" 



    return locations_str, vehicle_depo_str, distances_str
    
def query_data(table, attributes, valueList):
    value_list_str = ', '.join([f"'{value}'" for value in valueList])

    conditions = ' AND '.join([f"{attr} IN ({value_list_str})" for attr in attributes])
    sql_query=text(f"SELECT * FROM {table}  WHERE {conditions}")

    result = db.session.execute(sql_query)
    return result.mappings().all()
