from src.model import Vehicle
from src.config.database import db

class VehicleRepository:
    def __init__(self):
        self.session = db.session

    def get_all(self):
        return self.session.query(Vehicle).all()
    
    def get_by_plate(self,plate):
        return self.session.query(Vehicle).filter_by(plate=plate).first()

    def add(self, vehicle):
        self.session.add(vehicle)
        self.session.commit()
        return vehicle

    def remove(self, vehicle):
        self.session.delete(vehicle)
        self.session.commit()

    def check_vehicle_by_plate(self,plate):
        return self.session.query(Vehicle).filter_by(plate=plate).first() is not None