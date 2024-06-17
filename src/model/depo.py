from .node import Node
from src.config.database import db

class Depo(Node):
    __mapper_args__ = {'polymorphic_identity': 'depo'}
    id = db.Column(db.Integer, db.ForeignKey('node.id'), primary_key=True)
    capacity =db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Depo {self.name}, Capacity: {self.capacity}>'