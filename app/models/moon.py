from app import db

class Moon(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    size = db.Column(db.String)
    description = db.Column(db.String)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet= db.relationship("Planet", back_populates="moons")