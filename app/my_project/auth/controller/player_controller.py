from flask import jsonify
from app.my_project.auth.service.player_service import PlayerService

class PlayerController:
    def __init__(self):
        self.service = PlayerService()

    def get_all(self):
        return jsonify(self.service.get_all()), 200

    def get_by_id(self, player_id):
        res = self.service.get_by_id(player_id)
        return (jsonify(res), 200) if res else (jsonify({"error": "Player not found"}), 404)

    def create(self, data):
        return jsonify(self.service.create(data)), 201

    def update(self, player_id, data):
        res = self.service.update(player_id, data)
        return (jsonify(res), 200) if res else (jsonify({"error": "Player not found"}), 404)

    def delete(self, player_id):
        return ("", 204) if self.service.delete(player_id) else (jsonify({"error": "Player not found"}), 404)
