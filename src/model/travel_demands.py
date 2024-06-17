from src.config.database import db
from sqlalchemy.orm import relationship

class TravelDemands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    travel_id = db.Column(db.Integer, db.ForeignKey('travel.id'))
    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    demand = db.Column(db.Integer)

    travel = relationship("Travel",foreign_keys=[travel_id], back_populates="demands")

    def __repr__(self):
        return f'<Demand travel_id:{self.travel_id} node_id:{self.node_id} demand:{self.demand}>'