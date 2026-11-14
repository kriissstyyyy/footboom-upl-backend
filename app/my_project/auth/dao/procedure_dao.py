from app.my_project.auth.utils.procedure_caller import call_procedure

class ProcedureDAO:
    def insert_player(self, first_name, last_name, position, team_id):
        return call_procedure("sp_insert_player", (first_name, last_name, position, team_id))

    def link_player_sponsor(self, first_name, last_name, sponsor_name):
        return call_procedure("sp_link_player_sponsor", (first_name, last_name, sponsor_name))

    def insert_noname_cities(self):
        return call_procedure("sp_insert_noname_cities")

    def stadium_capacity_stat(self, func):
        return call_procedure("sp_stadium_capacity_stat", (func,))

    def split_players_random(self):
        return call_procedure("sp_split_players_random")
