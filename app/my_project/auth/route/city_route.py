from flask import Blueprint, request
from app.my_project.auth.controller.city_controller import CityController

city_bp = Blueprint("city_bp", __name__)
controller = CityController()

@city_bp.route("", methods=["GET"])
def get_all():
    return controller.get_all()

@city_bp.route("/<int:city_id>", methods=["GET"])
def get_by_id(city_id):
    return controller.get_by_id(city_id)

@city_bp.route("", methods=["POST"])
def create():
    return controller.create(request.get_json())

@city_bp.route("/<int:city_id>", methods=["PUT"])
def update(city_id):
    return controller.update(city_id, request.get_json())

@city_bp.route("/<int:city_id>", methods=["DELETE"])
def delete(city_id):
    return controller.delete(city_id)

@city_bp.route("/<int:city_id>/stadiums", methods=["GET"])
def get_city_stadiums(city_id):
    return controller.get_stadiums_by_city(city_id)

   