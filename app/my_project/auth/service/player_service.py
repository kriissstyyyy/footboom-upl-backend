from app.my_project.auth.dao.player_dao import PlayerDAO
from app.my_project.auth.domain.player import Player

class PlayerService:
    def __init__(self):
        self.dao = PlayerDAO()

    def get_all(self):
        return [p.put_into_dto() for p in self.dao.get_all()]

    def get_by_id(self, player_id):
        player = self.dao.get_by_id(player_id)
        return player.put_into_dto() if player else None

    def create(self, data):
        player = Player.create_from_dto(data)
        return self.dao.create(player).put_into_dto()

    def update(self, player_id, data):
        updated = self.dao.update(player_id, data)
        return updated.put_into_dto() if updated else None

    def delete(self, player_id):
        return self.dao.delete(player_id)
