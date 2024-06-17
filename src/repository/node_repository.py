from src.model import Node, Depo
from src.config.database import db

class NodeRepository:
    def __init__(self):
        self.session = db.session

    def get_all_nodes(self):
        return self.session.query(Node).all()
    
    def get_all_depos(self):
        return self.session.query(Depo).all()

    def get_node_by_id(self, node_id):
        return self.session.query(Node).get(node_id)

    def create_node(self, new_node):
        self.session.add(new_node)
        self.session.commit()
        return new_node

    def update_node(self, node, node_dict):
        for key, value in node_dict.items():
            setattr(node, key, value)
        self.session.commit()
        return node

    def delete_node(self, node):
        self.session.delete(node)
        self.session.commit()