from src.model import Edge
from src.config.database import db

class EdgeRepository:
    def __init__(self):
        self.session = db.session

    def get_all(self):
        return self.session.query(Edge).all()

    def create_edge(self, start_node_id, end_node_id, distance):
        new_edge = Edge(start_node_id=start_node_id, end_node_id=end_node_id, distance=distance)
        self.session.add(new_edge)
        self.session.commit()
        return new_edge

    def delete_edge(self, edge):
        self.session.delete(edge)
        self.session.commit()