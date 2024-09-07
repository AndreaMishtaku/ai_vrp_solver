from src.config.database import db
from sqlalchemy.orm import relationship

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(10), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<Vehicle {self.plate}>'