from src.model import Trip
from src.config.database import db

class TripRepository:
    def __init__(self):
        self.session = db.session

    def get_all_trips(self):
        return self.session.query(Trip).all()
    
    def get_trip_by_id(self,trip_id):
        return self.session.query(Trip).get(trip_id)
    
    def add_trip(self, new_trip):
        self.session.add(new_trip)
        self.session.commit()
        return new_trip