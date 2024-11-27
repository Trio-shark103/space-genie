from Sates import db

class Satellite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50), nullable=False)
    continent = db.Column(db.String(50), nullable=False)
    satellite_type = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    manufacturer = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1024), nullable=False)

def __repr__(self):
    return f'User {self.name}'