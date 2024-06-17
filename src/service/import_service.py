from src.payload import Success
from src.payload import Error
from src.repository.node_repository import NodeRepository
from src.model import Node

class ImportService:
    def __init__(self):
        self.node_repository=NodeRepository()

    def add_node(self, data):
        try:
            """
            Adds a list of coordinates to the database.
            :param data: List of dictionaries with keys 'name', 'latitude', and 'longitude'
            """
            for location in data:
                new_node = Node(name=location[0], latitude=location[1], longitude= location[2])
                self.node_repository.create_node(new_node)
        
            return Success(status_code=200,message="Database updated successfully.").to_dict()
        except Exception as e:
            return Error(status_code=400, message=str(e)).to_dict()