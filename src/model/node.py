from src.config.database import db
from sqlalchemy.orm import relationship

class Node(db.Model):        
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    routes = relationship("Edge", foreign_keys="[Edge.start_node_id]")

    def __repr__(self):
        return f'<Node {self.name}>'