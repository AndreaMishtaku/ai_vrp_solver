from src.repository.edge_repository import EdgeRepository
from src.repository.node_repository import NodeRepository
from src.utils import Mapper
from src.payload import Error
from src.model import Node

class BasicService:
    def __init__(self):
        self.node_repository=NodeRepository()
        self.edge_repository=EdgeRepository()

    def get_all_nodes(self):
        nodes_list=self.node_repository.get_all_nodes()
        response=Mapper.to_dict(nodes_list)
        return response

    def get_all_depos(self):
        nodes_list=self.node_repository.get_all_depos()
        response=Mapper.to_dict(nodes_list)
        return response
    

    def create_node(self,dict):
        new_node= Node(**dict)
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
