from app.my_project import db

class Player(db.Model):
    __tablename__ = "players"

    player_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.Enum("GK", "DEF", "MID", "FWD"), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.team_id"), nullable=False)

    def put_into_dto(self):
        return {
            "player_id": self.player_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "position": self.position,
            "team_id": self.team_id,
        }

    @staticmethod
    def create_from_dto(dto_dict):
        return Player(
            first_name=dto_dict.get("first_name"),
            last_name=dto_dict.get("last_name"),
            position=dto_dict.get("position"),
            team_id=dto_dict.get("team_id"),
        )
