from app.my_project.auth.dao.city_dao import CityDAO
from app.my_project.auth.domain.city import City

class CityService:
    def __init__(self):
        self.dao = CityDAO()

    def get_all(self):
        return [c.put_into_dto() for c in self.dao.get_all()]

    def get_by_id(self, city_id):
        city = self.dao.get_by_id(city_id)
        return city.put_into_dto() if city else None

    def create(self, data):
        city = City.create_from_dto(data)
        return self.dao.create(city).put_into_dto()

    def update(self, city_id, data):
        updated = self.dao.update(city_id, data)
        return updated.put_into_dto() if updated else None

    def delete(self, city_id):
        return self.dao.delete(city_id)

    def get_stadiums_by_city(self, city_id):
        stadiums = self.dao.get_stadiums_by_city(city_id)
        if stadiums is None:
            return None
        return [s.put_into_dto() for s in stadiums]

