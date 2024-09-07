from src.config.database import db
from sqlalchemy.orm import relationship

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_route_id = db.Column(db.Integer, db.ForeignKey('trip_route.id'))
    node_id = db.Column(db.Integer,db.ForeignKey('node.id'))

    trip_route = relationship("TripRoute",foreign_keys=[trip_route_id])
    node = relationship("Node", foreign_keys=[node_id])
    
    def __repr__(self):
        return f'<Visit visit_id:{self.id}>'