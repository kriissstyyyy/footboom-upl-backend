from flask import jsonify
from app.my_project.auth.service.match_service import MatchService

class MatchController:
    def __init__(self):
        self.service = MatchService()

    def get_all(self):
        return jsonify(self.service.get_all()), 200

    def get_by_id(self, match_id):
        res = self.service.get_by_id(match_id)
        return (jsonify(res), 200) if res else (jsonify({"error": "Match not found"}), 404)

    def create(self, data):
        return jsonify(self.service.create(data)), 201

    def update(self, match_id, data):
        res = self.service.update(match_id, data)
        return (jsonify(res), 200) if res else (jsonify({"error": "Match not found"}), 404)

    def delete(self, match_id):
        return ("", 204) if self.service.delete(match_id) else (jsonify({"error": "Match not found"}), 404)

    def get_goals_by_match(self, match_id):
        return jsonify(self.service.get_goals_by_match(match_id)), 200
