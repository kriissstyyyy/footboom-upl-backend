from app.my_project.auth.dao.sponsor_dao import SponsorDAO
from app.my_project.auth.domain.sponsor import Sponsor

class SponsorService:
    def __init__(self):
        self.dao = SponsorDAO()

    def get_all(self):
        return [s.put_into_dto() for s in self.dao.get_all()]

    def get_by_id(self, sponsor_id):
        sponsor = self.dao.get_by_id(sponsor_id)
        return sponsor.put_into_dto() if sponsor else None

    def create(self, data):
        sponsor = Sponsor.create_from_dto(data)
        return self.dao.create(sponsor).put_into_dto()

    def update(self, sponsor_id, data):
        updated = self.dao.update(sponsor_id, data)
        return updated.put_into_dto() if updated else None

    def delete(self, sponsor_id):
        return self.dao.delete(sponsor_id)
