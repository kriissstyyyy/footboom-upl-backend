from app.my_project.auth.dao.match_dao import MatchDAO
from app.my_project.auth.domain.match import Match

class MatchService:
    def __init__(self):
        self.dao = MatchDAO()

    def get_all(self):
        return [m.put_into_dto() for m in self.dao.get_all()]

    def get_by_id(self, match_id):
        match = self.dao.get_by_id(match_id)
        return match.put_into_dto() if match else None

    def create(self, data):
        match = Match.create_from_dto(data)
        return self.dao.create(match).put_into_dto()

    def update(self, match_id, data):
        updated = self.dao.update(match_id, data)
        return updated.put_into_dto() if updated else None

    def delete(self, match_id):
        return self.dao.delete(match_id)

    def get_goals_by_match(self, match_id):
        goals = self.dao.get_goals_by_match(match_id)
        return [
            {
                "goal_id": g.goal_id,
                "player_id": g.player_id,
                "player_name": f"{g.player.first_name} {g.player.last_name}",
                "minute": g.minute,
                "goal_type": g.goal_type,
            }
            for g in goals
        ]
