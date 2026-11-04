from flask import Blueprint, request
from app.my_project.auth.controller.team_controller import TeamController

team_bp = Blueprint("team_bp", __name__)
controller = TeamController()

@team_bp.route("", methods=["GET"])
def get_all():
    return controller.get_all()

@team_bp.route("/<int:team_id>", methods=["GET"])
def get_by_id(team_id):
    return controller.get_by_id(team_id)

@team_bp.route("", methods=["POST"])
def create():
    return controller.create(request.get_json())

@team_bp.route("/<int:team_id>", methods=["PUT"])
def update(team_id):
    return controller.update(team_id, request.get_json())

@team_bp.route("/<int:team_id>", methods=["DELETE"])
def delete(team_id):
    return controller.delete(team_id)

@team_bp.route("/<int:team_id>/players", methods=["GET"])
def get_team_players(team_id):
    return controller.get_players_by_team(team_id)
