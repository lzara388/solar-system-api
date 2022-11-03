import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.planet import Planet

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_saved_planets(app):
    # Arrange
    earth_planet = Planet(name="Earth",
                      description="third planet from the Sun and the only astronomical object known to harbor life.",
                      from_sun= "92.211 million m")
    jupiter_planet = Planet(name="Jupiter",
                         description="fifth planet from the Sun and the largest in the Solar System.",
                         from_sun= "483.8 million mi")

    db.session.add_all([earth_planet, jupiter_planet])
    # Alternatively, we could do
    # db.session.add(ocean_book)
    # db.session.add(mountain_book)
    db.session.commit()