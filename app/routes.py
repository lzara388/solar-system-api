from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.planet import Planet

planets_bp = Blueprint('planets_bp', __name__, url_prefix= "/planets")

@planets_bp.route("", methods=["GET"])

def read_all_planets():
    name_query = request.args.get("name")
    if name_query:
        planets = Planet.query.filter_by(name=name_query)
    else:
        planets = Planet.query.all()
        
    planets_response = []
    for planet in planets:
        planets_response.append(
            {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "from_sun": planet.from_sun
            }
        )
    return jsonify(planets_response)

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message":f"planet {planet_id} invalid"}, 400))

    planet = Planet.query.get(planet_id)

    if not planet:
        abort(make_response({"message":f"planet {planet_id} not found"}, 404))

    return planet
    

@planets_bp.route("/<planet_id>", methods= ["GET"])
def read_one_planet(planet_id):
    planet = validate_planet(planet_id)
    return {
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "from sun": planet.from_sun
        }

@planets_bp.route("", methods=["POST"])
def create_planet():
    request_body = request.get_json()
    new_planet = Planet(
                    name=request_body["name"],
                    description=request_body["description"],
                    from_sunn = request_body["from_sun"]
                    )

    db.session.add(new_planet)
    db.session.commit()

    return make_response(f"Planet {new_planet.title} successfully created", 201)


@planets_bp.route("/<planet_id>", methods = ["PUT"])
def update_planet(planet_id):
    planet = validate_planet(planet_id)

    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.from_sun = request_body["from_sun"]

    db.session.commit()

    return make_response(f"Planet #{planet.id} successfully updated")

#DELETE
@planets_bp.route("/<planet_id>", methods = ["DELETE"])
def delete_planet(planet_id):
    planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return make_response(f"Planet #{planet.id} successfully deleted")
