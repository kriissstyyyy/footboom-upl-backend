from flask import Blueprint, request
from app.my_project.auth.controller.match_controller import MatchController

match_bp = Blueprint("match_bp", __name__)
controller = MatchController()

@match_bp.route("", methods=["GET"])
def get_all():
    return controller.get_all()

@match_bp.route("/<int:match_id>", methods=["GET"])
def get_by_id(match_id):
    return controller.get_by_id(match_id)

@match_bp.route("", methods=["POST"])
def create():
    return controller.create(request.get_json())

@match_bp.route("/<int:match_id>", methods=["PUT"])
def update(match_id):
    return controller.update(match_id, request.get_json())

@match_bp.route("/<int:match_id>", methods=["DELETE"])
def delete(match_id):
    return controller.delete(match_id)

@match_bp.route("/<int:match_id>/goals", methods=["GET"])
def get_match_goals(match_id):
    return controller.get_goals_by_match(match_id)
