from app.my_project import db
from app.my_project.auth.domain.city import City

class CityDAO:
    def get_all(self):
        return City.query.all()

    def get_by_id(self, city_id):
        return City.query.get(city_id)

    def create(self, city):
        db.session.add(city)
        db.session.commit()
        return city

    def update(self, city_id, data):
        city = City.query.get(city_id)
        if not city:
            return None
        city.name = data.get("name", city.name)
        db.session.commit()
        return city

    def delete(self, city_id):
        city = City.query.get(city_id)
        if not city:
            return False
        db.session.delete(city)
        db.session.commit()
        return True

    def get_stadiums_by_city(self, city_id):
        city = City.query.get(city_id)
        return city.stadiums if city else None






