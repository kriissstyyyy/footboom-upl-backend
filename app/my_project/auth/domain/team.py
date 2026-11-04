from app.my_project import db

class Team(db.Model):
    __tablename__ = "teams"

    team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    short_name = db.Column(db.String(10), nullable=False)
    stadium_id = db.Column(db.Integer, db.ForeignKey("stadiums.stadium_id"), nullable=False)

    players = db.relationship("Player", backref="team", cascade="all, delete-orphan", lazy=True)
    stadium = db.relationship("Stadium", lazy=True)

    def put_into_dto(self):
        return {
            "team_id": self.team_id,
            "name": self.name,
            "short_name": self.short_name,
            "stadium_id": self.stadium_id,
        }

    @staticmethod
    def create_from_dto(dto_dict):
        return Team(
            name=dto_dict.get("name"),
            short_name=dto_dict.get("short_name"),
            stadium_id=dto_dict.get("stadium_id"),
        )
