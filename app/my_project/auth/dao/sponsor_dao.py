from app.my_project import db
from app.my_project.auth.domain.sponsor import Sponsor

class SponsorDAO:
    def get_all(self):
        return Sponsor.query.all()

    def get_by_id(self, sponsor_id):
        return Sponsor.query.get(sponsor_id)

    def create(self, sponsor):
        db.session.add(sponsor)
        db.session.commit()
        return sponsor

    def update(self, sponsor_id, data):
        sponsor = Sponsor.query.get(sponsor_id)
        if not sponsor:
            return None
        sponsor.name = data.get("name", sponsor.name)
        sponsor.team_id = data.get("team_id", sponsor.team_id)
        sponsor.contract_amount = data.get("contract_amount", sponsor.contract_amount)
        db.session.commit()
        return sponsor

    def delete(self, sponsor_id):
        sponsor = Sponsor.query.get(sponsor_id)
        if not sponsor:
            return False
        db.session.delete(sponsor)
        db.session.commit()
        return True
