from app.my_project import db
from app.my_project.auth.domain.match import Match, Goal

class MatchDAO:
    def get_all(self):
        return Match.query.all()

    def get_by_id(self, match_id):
        return Match.query.get(match_id)

    def create(self, match):
        db.session.add(match)
        db.session.commit()
        return match

    def update(self, match_id, data):
        match = Match.query.get(match_id)
        if not match:
            return None
        match.season_id = data.get("season_id", match.season_id)
        match.matchday = data.get("matchday", match.matchday)
        match.match_date = data.get("match_date", match.match_date)
        match.home_team_id = data.get("home_team_id", match.home_team_id)
        match.away_team_id = data.get("away_team_id", match.away_team_id)
        match.referee_id = data.get("referee_id", match.referee_id)
        match.home_score = data.get("home_score", match.home_score)
        match.away_score = data.get("away_score", match.away_score)
        match.status = data.get("status", match.status)
        db.session.commit()
        return match

    def delete(self, match_id):
        match = Match.query.get(match_id)
        if not match:
            return False
        db.session.delete(match)
        db.session.commit()
        return True

    def get_goals_by_match(self, match_id):
        return Goal.query.filter_by(match_id=match_id).all()
