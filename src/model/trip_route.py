from src.config.database import db
from sqlalchemy.orm import relationship

class TripRoute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    depo_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    load = db.Column(db.Integer)
    distance = db.Column(db.Integer)

    visits =relationship("Visit", back_populates="trip_route", lazy='joined')
    trip = relationship("Trip", foreign_keys=[trip_id])
    depo = relationship("Node", foreign_keys=[depo_id])
    vehicle = relationship("Vehicle", foreign_keys=[vehicle_id])

    def add_visit(self, visit):
        """
        Add a visit
        """
        self.visits.append(visit)

    def __repr__(self):
        return f'<Trip route id:{self.id}>' 