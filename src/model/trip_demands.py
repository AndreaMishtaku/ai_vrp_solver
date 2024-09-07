from src.config.database import db
from sqlalchemy.orm import relationship

class TripDemands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    demand = db.Column(db.Integer)

    trip = relationship("Trip",foreign_keys=[trip_id], back_populates="demands")
    node = relationship("Node",foreign_keys=[node_id])

    def __repr__(self):
        return f'<Demand trip_id:{self.trip_id} node_id:{self.node_id} demand:{self.demand}>'