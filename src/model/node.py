from enum import Enum
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

    routes = relationship("Edge", foreign_keys="[Edge.start_node_id]")
    trips = relationship("Trip", foreign_keys="[Trip.depo_id]")

    def __repr__(self):
        return f'<Node {self.name}>'