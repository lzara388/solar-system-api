from app import db

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    from_sun = db.Column(db.String)
    moons = db.relationship("Moon", back_populates="planet")

    # def to_dict(self):
        # planet_as_dict = {}
        # planet_as_dict["id"] = self.id
        # planet_as_dict["name"] = self.name
        # planet_as_dict["description"] = self.description
        # planet_as_dict["from_sun"] = self.from_sun
    def to_dict(self):
        planet_dict = {
        "id": self.id,
        "name": self.name,
        "description": self.description,
        "from_sun": self.from_sun
    }
        return planet_dict

    @classmethod
    def from_dict(cls, planet_data):
        new_planet = Planet(name=planet_data["name"],
                        description=planet_data["description"],
                        from_sun=planet_data["from_sun"])

        return new_planet