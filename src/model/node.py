from src.config.database import db
from sqlalchemy.orm import relationship
from src.enums.node_type import NodeType

class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    type = db.Column(db.Enum(NodeType), default='NODE', nullable=False)
    capacity = db.Column(db.Float,nullable=True)
    time = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<Node {self.name}>'
    
    def __str__(self):
        if self.type == NodeType.NODE:
            return f'Node-> Id: {self.id}, Name: {self.name}, Location: ({self.latitude}, {self.longitude})\n'
        else:
            return f'Depo-> Id: {self.id}, Name: {self.name}, Location: ({self.latitude}, {self.longitude}), Capacity: {self.capacity}\n'