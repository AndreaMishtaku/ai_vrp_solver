from src.payload import Success
from src.payload import Error
from src.repository.node_repository import NodeRepository
from src.repository.edge_repository import EdgeRepository
from src.model import Node
from geopy.distance import geodesic

class ImportService:
    def __init__(self):
        self.node_repository=NodeRepository()
        self.edge_repository=EdgeRepository()

    def add_node(self, data):
        try:
            for location in data:
                new_node = Node(name=location[0], latitude=location[1], longitude= location[2],type=location[3],capacity=location[4])
                self.node_repository.create_node(new_node)

            nodes_list=self.node_repository.get_all_nodes()
            depos_list=self.node_repository.get_all_depos()

            all_nodes = nodes_list + depos_list

            for start_node in all_nodes:
                for end_node in all_nodes:
                    if start_node.id != end_node.id:
                        distance = self._calculate_distance(start_node, end_node)
                        self.edge_repository.create_edge(start_node_id=start_node.id, end_node_id=end_node.id, distance=distance,time=0)

            return Success(status_code=200,message="Database updated successfully.").to_dict()
        except Exception as e:
            return Error(status_code=400, message=str(e)).to_dict()
        
    
    def _calculate_distance(self, node1, node2):
        coords_1 = (node1.latitude, node1.longitude)
        coords_2 = (node2.latitude, node2.longitude)

        return geodesic(coords_1, coords_2).km