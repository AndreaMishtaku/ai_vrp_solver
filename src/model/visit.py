from src.config.database import db
from sqlalchemy.orm import relationship

class Visit(db.Model):
    trip_route_id = db.Column(db.Integer, db.ForeignKey('trip_route.id'), primary_key=True)
    node_id = db.Column(db.Integer,db.ForeignKey('node.id'), primary_key=True)

    trip_route = relationship("TripRoute",foreign_keys=[trip_route_id])
    node = relationship("Node", foreign_keys=[node_id])
    
    def __repr__(self):
        return f'<Demand trip_id:{self.trip_id} node_id:{self.node_id} demand:{self.demand}>'