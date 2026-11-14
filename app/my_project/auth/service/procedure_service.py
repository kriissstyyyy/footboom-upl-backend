from decimal import Decimal
from app.my_project.auth.dao.procedure_dao import ProcedureDAO

class ProcedureService:
    def __init__(self):
        self.dao = ProcedureDAO()

    @staticmethod
    def _normalize(rows):
        result = []
        for row in rows:
            result.append({k: float(v) if isinstance(v, Decimal) else v for k, v in row.items()})
        return result

    def insert_player(self, data):
        rows = self.dao.insert_player(
            data.get("first_name"),
            data.get("last_name"),
            data.get("position"),
            data.get("team_id"),
        )
        return self._normalize(rows)[0]

    def link_player_sponsor(self, data):
        rows = self.dao.link_player_sponsor(
            data.get("first_name"),
            data.get("last_name"),
            data.get("sponsor_name"),
        )
        return self._normalize(rows)[0]

    def insert_noname_cities(self):
        return self._normalize(self.dao.insert_noname_cities())

    def stadium_capacity_stat(self, func):
        return self._normalize(self.dao.stadium_capacity_stat(func))[0]

    def split_players_random(self):
        return self._normalize(self.dao.split_players_random())[0]
