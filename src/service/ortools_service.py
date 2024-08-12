from src.repository import EdgeRepository,NodeRepository, VehicleRepository
from src.payload import Error
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

class ORToolsService:
    def __init__(self):
        self.node_repository=NodeRepository()
        self.edge_repository=EdgeRepository()
        self.vehicle_repository=VehicleRepository()

    def create_data_model(self, travel_dict):
        """Stores the data for the problem."""
        depos=self.node_repository.get_all_depos()
        nodes=self.node_repository.get_all_nodes()
        
        
        depot = next((depo for depo in depos if depo.name ==travel_dict['depo_vehicle'][0]['depo']), None)
        if depot is None:
            raise ValueError(f"Depot '{travel_dict['depo_vehicle'][0]['depo']}' not found in the list of all depots.")
        
        demand_nodes = [node for node in nodes if any(d['node'] == node.name and d['demand'] > 0 for d in travel_dict['demands'])]
        filtered_nodes =  [depot] + demand_nodes

        data = {}
        
        node_name_to_filtered_index = {node.name: i for i, node in enumerate(filtered_nodes)}
        original_index_to_filtered_index = {i: node_name_to_filtered_index[node.name] for i, node in enumerate(depos + nodes) if node.name in node_name_to_filtered_index}
            
        # Store original node indices for reference in solution
        original_indices = [node.id for node in filtered_nodes]

        demands = [0] * len(filtered_nodes)
        for demand in travel_dict['demands']:
            node_name = demand['node']
            demand_value = demand['demand']
            if node_name in node_name_to_filtered_index:
                index = node_name_to_filtered_index[node_name]
                demands[index] = demand_value

        data['demands'] = demands
        data['vehicle_capacities'] = []
        #data['starts'] = []
        #data['ends'] = []


        for dv in travel_dict['depo_vehicle']:
            vehicle = self.vehicle_repository.get_by_plate(plate=dv['plate'])
            data['vehicle_capacities'].append(vehicle.capacity)


        data['depot'] =  node_name_to_filtered_index[travel_dict['depo_vehicle'][0]['depo']] 
        data['num_vehicles'] = len(data['vehicle_capacities'])


        # Create the reduced distance matrix
        num_filtered_locations = len(filtered_nodes)
        distance_matrix = [[0 if i == j else float('inf') for j in range(num_filtered_locations)] for i in range(num_filtered_locations)]
        edges = self.edge_repository.get_all()
        original_index = {node.id: index for index, node in enumerate(depos + nodes)}

        for edge in edges:
            if edge.start_node_id in original_index and edge.end_node_id in original_index:
                if original_index[edge.start_node_id] in original_index_to_filtered_index and original_index[edge.end_node_id] in original_index_to_filtered_index:
                    start_index = original_index_to_filtered_index[original_index[edge.start_node_id]]
                    end_index = original_index_to_filtered_index[original_index[edge.end_node_id]]
                    distance_matrix[start_index][end_index] = edge.distance
                    distance_matrix[end_index][start_index] = edge.distance 

        data['distance_matrix'] = distance_matrix
        return data,original_indices
    

    def get_solution(self, data, manager, routing, solution, original_indices):
        summary = {
        'routes': [],
        'total_distance': 0,
        'total_load': 0
        }

        for vehicle_id in range(data['num_vehicles']):
            index = routing.Start(vehicle_id)
            route = []
            route_distance = 0
            route_load = 0
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                original_node_index = original_indices[node_index]  
                route_load += data['demands'][node_index]
                route.append(original_node_index)  
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)

            node_index = manager.IndexToNode(index)
            original_node_index = original_indices[node_index]  
            route.append(original_node_index)  

            if route_load > 0: 
                summary['routes'].append({
                'plate': vehicle_id,
                'route': route,
                'load': route_load,
                'distance': route_distance
            })
                summary['total_distance'] += route_distance
                summary['total_load'] += route_load

        return summary

    def check_payload(self,travel_dict):     
        demands=travel_dict['demands']

        for demand in demands:
            if self.node_repository.check_node_by_name(name=demand['node'],is_depo=False) is False:
                raise Error(message=f'Location not found!',status_code=404)
            
        depo_vehicle=travel_dict['depo_vehicle']

        for dv in depo_vehicle:
            if self.node_repository.check_node_by_name(name=dv['depo'],is_depo=True) is False:
                raise Error(message=f'Depo not found!',status_code=404)
            if self.vehicle_repository.check_vehicle_by_plate(plate=dv['plate']) is False:
                raise Error(message=f'Vehicle not found!',status_code=404)
            
        return True


    def routing_model(self, travel_dict):
        """Solve the CVRP problem."""
        # Instantiate the data problem.
        data, original_indices = self.create_data_model(travel_dict=travel_dict)

        manager = pywrapcp.RoutingIndexManager(
            len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
        )

        routing = pywrapcp.RoutingModel(manager)
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""

            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data["distance_matrix"][from_node][to_node]
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        def demand_callback(from_index):
            """Returns the demand of the node."""
            # Convert from routing variable Index to demands NodeIndex.
            from_node = manager.IndexToNode(from_index)
            return data["demands"][from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  
            data["vehicle_capacities"], 
            True,
            "Capacity",
        )

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_parameters.time_limit.FromSeconds(1)
        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            return self.get_solution(data, manager, routing, solution, original_indices)
        else:
            raise Error(message=f'No solution found!',status_code=400)

