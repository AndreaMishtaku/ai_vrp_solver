from src.config.database import db
from sqlalchemy.orm import relationship

class Travel(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))

    vehicle = relationship("Vehicle",foreign_keys=[vehicle_id], back_populates="travels")
    demands = relationship("TravelDemands",foreign_keys="[TravelDemands.travel_id]")

    def __repr__(self):
        return f'<Travel {self.id}>'