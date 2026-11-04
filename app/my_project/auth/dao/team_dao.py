from app.my_project import db
from app.my_project.auth.domain.team import Team

class TeamDAO:
    def get_all(self):
        return Team.query.all()

    def get_by_id(self, team_id):
        return Team.query.get(team_id)

    def create(self, team):
        db.session.add(team)
        db.session.commit()
        return team

    def update(self, team_id, data):
        team = Team.query.get(team_id)
        if not team:
            return None
        team.name = data.get("name", team.name)
        team.short_name = data.get("short_name", team.short_name)
        team.stadium_id = data.get("stadium_id", team.stadium_id)
        db.session.commit()
        return team

    def delete(self, team_id):
        team = Team.query.get(team_id)
        if not team:
            return False
        db.session.delete(team)
        db.session.commit()
        return True

    def get_players_by_team(self, team_id):
        team = Team.query.get(team_id)
        return team.players if team else None
