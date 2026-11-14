from flask import jsonify
from app.my_project.auth.service.procedure_service import ProcedureService

class ProcedureController:
    def __init__(self):
        self.service = ProcedureService()

    @staticmethod
    def _missing(data, fields):
        if not data:
            return list(fields)
        return [f for f in fields if data.get(f) in (None, "")]

    def insert_player(self, data):
        missing = self._missing(data, ("first_name", "last_name", "position", "team_id"))
        if missing:
            return jsonify({"error": "Missing fields", "fields": missing}), 400
        return jsonify(self.service.insert_player(data)), 201

    def link_player_sponsor(self, data):
        missing = self._missing(data, ("first_name", "last_name", "sponsor_name"))
        if missing:
            return jsonify({"error": "Missing fields", "fields": missing}), 400
        return jsonify(self.service.link_player_sponsor(data)), 201

    def insert_noname_cities(self):
        return jsonify(self.service.insert_noname_cities()), 201

    def stadium_capacity_stat(self, func):
        if not func:
            return jsonify({"error": "Query parameter func is required"}), 400
        return jsonify(self.service.stadium_capacity_stat(func)), 200

    def split_players_random(self):
        return jsonify(self.service.split_players_random()), 201
