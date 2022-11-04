from app import db
from app.models.moon import Moon
from app.models.planet import Planet
from app.planet_routes import validate_model
from flask import Blueprint, jsonify, abort, make_response, request