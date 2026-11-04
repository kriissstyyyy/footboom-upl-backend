from flask import jsonify
from app.my_project.auth.service.city_service import CityService

class CityController:
    def __init__(self):
        self.service = CityService()

    def get_all(self):
        return jsonify(self.service.get_all()), 200

    def get_by_id(self, city_id):
        res = self.service.get_by_id(city_id)
        return (jsonify(res), 200) if res else (jsonify({"error": "City not found"}), 404)

    def create(self, data):
        return jsonify(self.service.create(data)), 201

    def update(self, city_id, data):
        res = self.service.update(city_id, data)
        return (jsonify(res), 200) if res else (jsonify({"error": "City not found"}), 404)

    def delete(self, city_id):
        return ("", 204) if self.service.delete(city_id) else (jsonify({"error": "City not found"}), 404)

    def get_stadiums_by_city(self, city_id):
        res = self.service.get_stadiums_by_city(city_id)
        return (jsonify(res), 200) if res is not None else (jsonify({"error": "City not found"}), 404)

