from flask import jsonify
from app.my_project.auth.service.team_service import TeamService

class TeamController:
    def __init__(self):
        self.service = TeamService()

    def get_all(self):
        return jsonify(self.service.get_all()), 200

    def get_by_id(self, team_id):
        res = self.service.get_by_id(team_id)
        return (jsonify(res), 200) if res else (jsonify({"error": "Team not found"}), 404)

    def create(self, data):
        return jsonify(self.service.create(data)), 201

    def update(self, team_id, data):
        res = self.service.update(team_id, data)
        return (jsonify(res), 200) if res else (jsonify({"error": "Team not found"}), 404)

    def delete(self, team_id):
        return ("", 204) if self.service.delete(team_id) else (jsonify({"error": "Team not found"}), 404)

    def get_players_by_team(self, team_id):
        res = self.service.get_players_by_team(team_id)
        return (jsonify(res), 200) if res is not None else (jsonify({"error": "Team not found"}), 404)
