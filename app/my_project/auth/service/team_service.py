from app.my_project.auth.dao.team_dao import TeamDAO
from app.my_project.auth.domain.team import Team

class TeamService:
    def __init__(self):
        self.dao = TeamDAO()

    def get_all(self):
        return [t.put_into_dto() for t in self.dao.get_all()]

    def get_by_id(self, team_id):
        team = self.dao.get_by_id(team_id)
        return team.put_into_dto() if team else None

    def create(self, data):
        team = Team.create_from_dto(data)
        return self.dao.create(team).put_into_dto()

    def update(self, team_id, data):
        updated = self.dao.update(team_id, data)
        return updated.put_into_dto() if updated else None

    def delete(self, team_id):
        return self.dao.delete(team_id)

    def get_players_by_team(self, team_id):
        players = self.dao.get_players_by_team(team_id)
        if players is None:
            return None
        return [p.put_into_dto() for p in players]
