from src.config.database import db
from sqlalchemy.orm import relationship

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_load = db.Column(db.Integer, nullable=False)
    total_distance = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime ,nullable=False)
    generated_by = db.Column(db.String(20), nullable=False)
    generated_for = db.Column(db.Float, nullable=False)
    llm_model_name = db.Column(db.String(20))
    reference = db.Column(db.String(80))
    
    demands = relationship("TripDemands", back_populates="trip", lazy='joined')
    routes = relationship("TripRoute",  back_populates="trip", lazy='joined')

    def to_dict(self):
        routes = []

        for route in self.routes:
            visits=[]
            for visit in route.visits:
                visits.append(visit.node_id)
            routes.append({
                "plate": route.vehicle.plate,  
                "route": visits,
                "load": route.load,
                "distance": route.distance
            })

        # Build the demands array
        demands = []
        for demand in self.demands:
            demands.append({
                "demand": demand.demand,
                "node_name": demand.node.name  
            })

        # Build the final response
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "total_distance": self.total_distance,
            "total_load": self.total_load,
            "routes": routes,
            "demands": demands,
            "generated_for": self.generated_for,
            "generated_by": self.generated_by,
            "reference": self.reference,
            "llm_model_name": self.llm_model_name
        }


    def add_demand(self, demand):
        """
        Add a demand to the trip.
        """
        self.demands.append(demand)

    def add_route(self, route):
        """
        Add a route to the trip.
        """
        self.routes.append(route)

    def __repr__(self):
        return f'<Trip {self.id}>'
