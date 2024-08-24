from src.config.database import db
from sqlalchemy.orm import relationship

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    depo_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    total_load = db.Column(db.Integer, nullable=False)
    total_distance = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime,nullable=False)

    vehicle = relationship("Vehicle",foreign_keys=[vehicle_id], back_populates="trips")
    depo = relationship("Node",foreign_keys=[depo_id], back_populates="trips")
    demands = relationship("TripDemands",foreign_keys="[TripDemands.trip_id]")

    def __repr__(self):
        return f'<Trip {self.id}>'