from app.my_project import db

class Sponsor(db.Model):
    __tablename__ = "sponsors"

    sponsor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    team_id = db.Column(db.Integer, nullable=False)
    contract_amount = db.Column(db.Integer, nullable=False)

    def put_into_dto(self):
        return {
            "sponsor_id": self.sponsor_id,
            "name": self.name,
            "team_id": self.team_id,
            "contract_amount": self.contract_amount,
        }

    @staticmethod
    def create_from_dto(dto_dict):
        return Sponsor(
            name=dto_dict.get("name"),
            team_id=dto_dict.get("team_id"),
            contract_amount=dto_dict.get("contract_amount"),
        )
