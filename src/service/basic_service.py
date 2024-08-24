from src.repository import NodeRepository, EdgeRepository, VehicleRepository, TripRepository
from src.utils import Mapper
from src.payload import Error
from src.model import Node

class BasicService:
    def __init__(self):
        self.node_repository=NodeRepository()
        self.edge_repository=EdgeRepository()
        self.vehicle_repository=VehicleRepository()
        self.trip_repository=TripRepository()

    def get_all_nodes(self):
        nodes_list=self.node_repository.get_all_nodes()
        response=Mapper.to_dict(nodes_list)
        return response

    def get_all_depos(self):
        nodes_list=self.node_repository.get_all_depos()
        response=Mapper.to_dict(nodes_list)
        return response
    

    def create_node(self,dict):
        #new_node= Node(**dict)
        self.node_repository.create_node(dict)
        return

    def get_node_by_id(self,id):
        node = self.node_repository.get_node_by_id(id)
        if node is None:
            raise Error(message=f'Node with id {id} doesnt exist',status_code=404)
        response=Mapper.to_dict(node)
        return response
    
    def update_node(self,id,dict):
        node = self.node_repository.get_node_by_id(id)
        if node is None:
            raise Error(message=f'Node with id {id} doesnt exist',status_code=404)
        
        self.node_repository.update_node(node,dict)
        return
    
    def delete_node(self,id):
        node = self.node_repository.get_node_by_id(id)
        if node is None:
            raise Error(message=f'Node with id {id} doesnt exist',status_code=404)
        self.node_repository.delete_node(node)
        return
    
    def create_vehicle(self,dict):
        self.vehicle_repository.add(dict)
        return
    
    def get_vehicle_by_id(self,id):
        vehicle = self.vehicle_repository.get_by_id(id)
        if vehicle is None:
            raise Error(message=f'Vehicle with id {id} doesnt exist',status_code=404)
        response=Mapper.to_dict(vehicle)
        return response

    def update_vehicle(self,id,dict):
        vehicle = self.vehicle_repository.get_by_id(id)
        if vehicle is None:
            raise Error(message=f'Vehicle with id {id} doesnt exist',status_code=404)

        self.vehicle_repository.update_vehicle(vehicle,dict)
        return
    
    def get_all_vehicles(self):
        vehicles_list=self.vehicle_repository.get_all()
        response=Mapper.to_dict(vehicles_list)
        return response
    
    def delete_vehicle(self,id):
        vehicle = self.vehicle_repository.get_by_id(id)
        if vehicle is None:
            raise Error(message=f'Vehicle with id {id} doesnt exist',status_code=404)
        self.vehicle_repository.remove(vehicle)
        return
    
    def get_trip_by_id(self,id):
        trip = self.trip_repository.get_by_id(id)
        if trip is None:
            raise Error(message=f'Trip with id {id} doesnt exist',status_code=404)
        response=Mapper.to_dict(trip)
        return response
    
    def get_all_trips(self):
        trips_list=self.trip_repository.get_all()
        response=Mapper.to_dict(trips_list)
        return response