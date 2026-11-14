USE footboom_upl;

DELETE FROM players WHERE player_id = 11;
SELECT * FROM players_delete_log;

CALL sp_insert_player('Тест', 'Гравець', 'MID', 1);
CALL sp_link_player_sponsor('Андрій', 'Ярмоленко', 'Puma');
CALL sp_insert_noname_cities();

SELECT fn_stadium_capacity_stat('MAX'), fn_stadium_capacity_stat('MIN'), fn_stadium_capacity_stat('SUM'), fn_stadium_capacity_stat('AVG');
CALL sp_stadium_capacity_stat('AVG');

CALL sp_split_players_random();
SHOW TABLES LIKE 'players_%';

SELECT * FROM sponsors;
SELECT * FROM player_sponsors;

INSERT INTO sponsors (name, team_id, contract_amount) VALUES ('Test', 999, 12345);
INSERT INTO sponsors (name, team_id, contract_amount) VALUES ('Test', 1, 12300);
UPDATE sponsors SET team_id = 999 WHERE sponsor_id = 1;
DELETE FROM seasons WHERE season_id = 1;
