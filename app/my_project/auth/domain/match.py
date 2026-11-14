from app.my_project import db

class Match(db.Model):
    __tablename__ = "matches"

    match_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    season_id = db.Column(db.Integer, db.ForeignKey("seasons.season_id"), nullable=False)
    matchday = db.Column(db.Integer, nullable=False)
    match_date = db.Column(db.DateTime, nullable=False)
    home_team_id = db.Column(db.Integer, db.ForeignKey("teams.team_id"), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey("teams.team_id"), nullable=False)
    referee_id = db.Column(db.Integer, db.ForeignKey("referees.referee_id"), nullable=False)
    home_score = db.Column(db.Integer, nullable=True)
    away_score = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Enum("scheduled", "finished", "postponed"), default="scheduled")

    home_team = db.relationship("Team", foreign_keys=[home_team_id])
    away_team = db.relationship("Team", foreign_keys=[away_team_id])
    goals = db.relationship("Goal", backref="match", cascade="all, delete-orphan", lazy=True)

    def put_into_dto(self):
        return {
            "match_id": self.match_id,
            "season_id": self.season_id,
            "matchday": self.matchday,
            "match_date": self.match_date.strftime("%Y-%m-%d %H:%M:%S") if self.match_date else None,
            "home_team_id": self.home_team_id,
            "away_team_id": self.away_team_id,
            "referee_id": self.referee_id,
            "home_score": self.home_score,
            "away_score": self.away_score,
            "status": self.status,
        }

    @staticmethod
    def create_from_dto(dto_dict):
        return Match(
            season_id=dto_dict.get("season_id"),
            matchday=dto_dict.get("matchday"),
            match_date=dto_dict.get("match_date"),
            home_team_id=dto_dict.get("home_team_id"),
            away_team_id=dto_dict.get("away_team_id"),
            referee_id=dto_dict.get("referee_id"),
            home_score=dto_dict.get("home_score"),
            away_score=dto_dict.get("away_score"),
            status=dto_dict.get("status", "scheduled"),
        )


class Season(db.Model):
    __tablename__ = "seasons"
    season_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)


class Referee(db.Model):
    __tablename__ = "referees"
    referee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)


class Goal(db.Model):
    __tablename__ = "goals"
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    match_id = db.Column(db.Integer, db.ForeignKey("matches.match_id"), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey("players.player_id"), nullable=False)
    minute = db.Column(db.Integer, nullable=False)
    goal_type = db.Column(db.Enum("regular", "penalty", "own_goal", "free_kick"), default="regular")

    player = db.relationship("Player", lazy=True)

    def put_into_dto(self):
        return {
            "goal_id": self.goal_id,
            "match_id": self.match_id,
            "player_id": self.player_id,
            "minute": self.minute,
            "goal_type": self.goal_type,
        }
