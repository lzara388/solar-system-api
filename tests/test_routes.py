from flask import Blueprint, jsonify

def test_get_all_planets_with_no_records(client):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

#GET /planets/1 returns a response body that matches our fixture
def test_get_one_planet(client, two_saved_planets):
    # Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        'id': 1,
        'name': 'Earth',
        'description': 'third planet from the Sun and the only astronomical object known to harbor life.',
        'from_sun': '92.211 million m'
    }

#GET /planets/1 with no data in test database (no fixture) returns a 404
def test_get_one_planet_not_found(client):
    # Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message":"planet 1 not found"}

#POST /planets with a JSON request body returns a 201
def test_create_one_planet(client):
    # Act
    response = client.post("/planets", json={
        'name': 'Pluto',
        'description': 'dwarf planet in the Kuiper belt, a ring of bodies beyond the orbit of Neptune.',
        'from_sun': '3.7 billion m'
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == "Planet Pluto successfully created"

#GET /planets with valid test data (fixtures) returns a 200 with an array including appropriate test data

def test_get_all_planets(client, two_saved_planets):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [{
                        "id": 1,
                        "name":"Earth",
                        "description":"third planet from the Sun and the only astronomical object known to harbor life.",
                        "from_sun":"92.211 million m"},
                        {
                            "id": 2,
                            "name":"Jupiter",
                            "description":"fifth planet from the Sun and the largest in the Solar System.",
                            "from_sun": "483.8 million mi"}]
    assert len(response_body) == 2
    # assert response_body == two_saved_planets <- convert from object to list of dict
