from app.my_project import db

class City(db.Model):
    __tablename__ = "cities"

    city_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    stadiums = db.relationship("Stadium", backref="city", cascade="all, delete-orphan", lazy=True)

    def put_into_dto(self):
        return {
            "city_id": self.city_id,
            "name": self.name,
        }

    @staticmethod
    def create_from_dto(dto_dict):
        return City(name=dto_dict.get("name"))


class Stadium(db.Model):
    __tablename__ = "stadiums"

    stadium_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey("cities.city_id"), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    def put_into_dto(self):
        return {
            "stadium_id": self.stadium_id,
            "name": self.name,
            "city_id": self.city_id,
            "capacity": self.capacity,
        }
