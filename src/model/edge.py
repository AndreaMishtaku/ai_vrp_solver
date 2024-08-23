from src.config.database import db
from sqlalchemy.orm import relationship

class Edge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_node_id= db.Column(db.Integer,db.ForeignKey('node.id'),nullable=False)
    end_node_id = db.Column(db.Integer,db.ForeignKey('node.id'),nullable=False)
    distance = db.Column(db.Integer, nullable=False)

    start_node = relationship("Node", foreign_keys=[start_node_id], back_populates="routes")
    end_node = relationship("Node", foreign_keys=[end_node_id])

    def __repr__(self):
        return f'<Edge {self.start_node_id} {self.end_node_id}>'