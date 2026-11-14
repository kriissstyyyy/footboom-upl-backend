from flask import jsonify
from app.my_project.auth.service.sponsor_service import SponsorService

class SponsorController:
    def __init__(self):
        self.service = SponsorService()

    def get_all(self):
        return jsonify(self.service.get_all()), 200

    def get_by_id(self, sponsor_id):
        res = self.service.get_by_id(sponsor_id)
        return (jsonify(res), 200) if res else (jsonify({"error": "Sponsor not found"}), 404)

    def create(self, data):
        return jsonify(self.service.create(data)), 201

    def update(self, sponsor_id, data):
        res = self.service.update(sponsor_id, data)
        return (jsonify(res), 200) if res else (jsonify({"error": "Sponsor not found"}), 404)

    def delete(self, sponsor_id):
        return ("", 204) if self.service.delete(sponsor_id) else (jsonify({"error": "Sponsor not found"}), 404)
