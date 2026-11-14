from flask import Blueprint, request
from app.my_project.auth.controller.procedure_controller import ProcedureController

procedure_bp = Blueprint("procedure_bp", __name__)
controller = ProcedureController()

@procedure_bp.route("/insert-player", methods=["POST"])
def insert_player():
    return controller.insert_player(request.get_json(silent=True))

@procedure_bp.route("/link-player-sponsor", methods=["POST"])
def link_player_sponsor():
    return controller.link_player_sponsor(request.get_json(silent=True))

@procedure_bp.route("/insert-noname-cities", methods=["POST"])
def insert_noname_cities():
    return controller.insert_noname_cities()

@procedure_bp.route("/stadium-capacity-stat", methods=["GET"])
def stadium_capacity_stat():
    return controller.stadium_capacity_stat(request.args.get("func"))

@procedure_bp.route("/split-players-random", methods=["POST"])
def split_players_random():
    return controller.split_players_random()
