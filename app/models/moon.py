from app import db

class Moon(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    size = db.Column(db.String)
    description = db.Column(db.String)
    distance_from_planet = db.Column(db.String)
    planets= db.relationship("Planet", back_populates="moon")