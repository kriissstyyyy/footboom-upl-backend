from app.my_project import db
from app.my_project.auth.domain.player import Player

class PlayerDAO:
    def get_all(self):
        return Player.query.all()

    def get_by_id(self, player_id):
        return Player.query.get(player_id)

    def create(self, player):
        db.session.add(player)
        db.session.commit()
        return player

    def update(self, player_id, data):
        player = Player.query.get(player_id)
        if not player:
            return None
        player.first_name = data.get("first_name", player.first_name)
        player.last_name = data.get("last_name", player.last_name)
        player.position = data.get("position", player.position)
        player.team_id = data.get("team_id", player.team_id)
        db.session.commit()
        return player

    def delete(self, player_id):
        player = Player.query.get(player_id)
        if not player:
            return False
        db.session.delete(player)
        db.session.commit()
        return True
