from flask import Blueprint, request
from app.my_project.auth.controller.sponsor_controller import SponsorController

sponsor_bp = Blueprint("sponsor_bp", __name__)
controller = SponsorController()

@sponsor_bp.route("", methods=["GET"])
def get_all():
    return controller.get_all()

@sponsor_bp.route("/<int:sponsor_id>", methods=["GET"])
def get_by_id(sponsor_id):
    return controller.get_by_id(sponsor_id)

@sponsor_bp.route("", methods=["POST"])
def create():
    return controller.create(request.get_json())

@sponsor_bp.route("/<int:sponsor_id>", methods=["PUT"])
def update(sponsor_id):
    return controller.update(sponsor_id, request.get_json())

@sponsor_bp.route("/<int:sponsor_id>", methods=["DELETE"])
def delete(sponsor_id):
    return controller.delete(sponsor_id)
