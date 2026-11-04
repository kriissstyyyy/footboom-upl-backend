from flask import Blueprint, request
from app.my_project.auth.controller.player_controller import PlayerController

player_bp = Blueprint("player_bp", __name__)
controller = PlayerController()

@player_bp.route("", methods=["GET"])
def get_all():
    return controller.get_all()

@player_bp.route("/<int:player_id>", methods=["GET"])
def get_by_id(player_id):
    return controller.get_by_id(player_id)

@player_bp.route("", methods=["POST"])
def create():
    return controller.create(request.get_json())

@player_bp.route("/<int:player_id>", methods=["PUT"])
def update(player_id):
    return controller.update(player_id, request.get_json())

@player_bp.route("/<int:player_id>", methods=["DELETE"])
def delete(player_id):
    return controller.delete(player_id)
