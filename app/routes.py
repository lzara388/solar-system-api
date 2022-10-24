from crypt import methods
from flask import Blueprint, jsonify, abort, make_response

class Planet:
    def __init__(self, id, name, description, from_sun):
        self.id = id
        self.name = name
        self.description = description
        self.from_sun = from_sun
    

planets = [
    Planet(1, "Mars", "Mars is the fourth planet from the Sun and the second-smallest planet in the Solar System", "141.6 million m"),
    Planet(2, "Venus", "Venus is the second planet from the Sun.", "67.24 million m"), 
    Planet(3, "Neptune", "eighth planet from the Sun and the farthest known solar planet", "2.793 billion mi") 
    ]

planets_bp = Blueprint('planets_bp', __name__, url_prefix= "/planets")

@planets_bp.route("", methods=["GET"])
def handle_planets():
    # planets_response = []
    # for planet in planets:
    #     planets_response.append(
    #         {
    #             "id": planet.id,
    #             "name": planet.name,
    #             "description": planet.description,
    #             "from_sun" : planet.from_sun
    #         }
    #     )
    planets_response = [vars(planet) for planet in planets]
    return jsonify(planets_response)

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message":f"planet {planet_id} invalid"}, 400))

    for planet in planets:
        if planet.id == planet_id:
            return vars(planet)
    
    abort(make_response({"message":f"planet {planet_id} not found"}, 404))

@planets_bp.route("/<planet_id>", methods= ["GET"])
def handle_planet(planet_id):
    planet = validate_planet(planet_id)
    return planet




