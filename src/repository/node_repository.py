from src.model import Node
from src.config.database import db
from src.enums.node_type import NodeType

class NodeRepository:
    def __init__(self):
        self.session = db.session

    def get_all_nodes(self):
        return self.session.query(Node).filter(Node.type ==NodeType.NODE).all()
    
    def get_all_depos(self): 
        return self.session.query(Node).filter(Node.type ==NodeType.DEPO).all()

    def get_node_by_id(self, node_id):
        return self.session.query(Node).get(node_id)
    
    def get_node_by_name(self,name):
        return self.session.query(Node).filter_by(name=name).first()

    def create_node(self, new_node):
        self.session.add(new_node)
        self.session.commit()
        return new_node
    
    def check_node_by_name(self,name,is_depo):
        if(is_depo is True):
            return self.session.query(Node).filter_by(name=name,type=NodeType.DEPO).first() is not None
        else:
            return self.session.query(Node).filter_by(name=name,type=NodeType.NODE).first() is not None

    def update_node(self, node):
        self.session.commit()
        return node

    def delete_node(self, node):
        self.session.delete(node)
        self.session.commit()