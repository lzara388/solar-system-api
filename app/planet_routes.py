from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.planet import Planet
from app.models.moon import Moon

planets_bp = Blueprint('planets_bp', __name__, url_prefix= "/planets")
# moons_bp = Blueprint('moons_bp', __name__, url_prefix= "/moons")

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

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
    return model
    

@planets_bp.route("/<planet_id>", methods= ["GET"])
def read_one_planet(planet_id):
    planet = validate_model(Planet,planet_id)
    return planet.to_dict()
    # return {
    #         "id": planet.id,
    #         "name": planet.name,
    #         "description": planet.description,
    #         "from_sun": planet.from_sun
    #     }

@planets_bp.route("", methods=["POST"])
def create_planet():
    request_body = request.get_json()
    new_planet = Planet(
                    name=request_body["name"],
                    description=request_body["description"],
                    from_sun = request_body["from_sun"]
                    )

    db.session.add(new_planet)
    db.session.commit()


    return make_response(jsonify(f"Planet {new_planet.name} successfully created"), 201)


@planets_bp.route("/<planet_id>", methods = ["PUT"])
def update_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.from_sun = request_body["from_sun"]

    db.session.commit()

    return make_response(jsonify(f"Planet #{planet.id} successfully updated"))

#DELETE
@planets_bp.route("/<planet_id>", methods = ["DELETE"])
def delete_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    db.session.delete(planet)
    db.session.commit()

    return make_response(jsonify(f"Planet #{planet.id} successfully deleted"))

#NESTED ROUTE
@planets_bp.route("<planet_id>/moons", methods=["POST"])
def create_moon(planet_id):
    planet = validate_model(Planet, planet_id)
    request_body = request.get_json()
    new_moon = Moon(
        name =request_body["name"],
        description = request_body["description"],
        size = request_body["size"])

    planet.moons.append(new_moon)
    db.session.add(new_moon)
    db.session.commit()

    return make_response(jsonify(f"Moon {new_moon.name} successfully created"), 201)

@planets_bp.route("<planet_id>/moons", methods=["GET"])

def read_moons_for_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    moons_response = []
    for moon in planet.moons:
        moons_response.append(
            {
            "id": moon.id,
            "name": moon.name,
            "size":moon.size,
            "description": moon.description
            }
        )
    return jsonify(moons_response) 