USE footboom_upl;

DROP TABLE IF EXISTS player_sponsors;
DROP TABLE IF EXISTS sponsors;
DROP TABLE IF EXISTS players_delete_log;

CREATE TABLE sponsors (
    sponsor_id      INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    team_id         INT UNSIGNED NOT NULL,
    contract_amount INT UNSIGNED NOT NULL,
    INDEX idx_sponsors_team (team_id)
) ENGINE=InnoDB;

CREATE TABLE player_sponsors (
    player_id  INT UNSIGNED NOT NULL,
    sponsor_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (player_id, sponsor_id),
    CONSTRAINT fk_ps_player  FOREIGN KEY (player_id)  REFERENCES players(player_id)   ON DELETE CASCADE,
    CONSTRAINT fk_ps_sponsor FOREIGN KEY (sponsor_id) REFERENCES sponsors(sponsor_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE players_delete_log (
    log_id     INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    player_id  INT UNSIGNED NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name  VARCHAR(50) NOT NULL,
    position   VARCHAR(10) NOT NULL,
    team_id    INT UNSIGNED NOT NULL,
    deleted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

DROP TRIGGER IF EXISTS trg_sponsors_bi;
DROP TRIGGER IF EXISTS trg_sponsors_bu;
DROP TRIGGER IF EXISTS trg_teams_bd;
DROP TRIGGER IF EXISTS trg_sponsors_amount_bi;
DROP TRIGGER IF EXISTS trg_sponsors_amount_bu;
DROP TRIGGER IF EXISTS trg_seasons_bd;
DROP TRIGGER IF EXISTS trg_players_ad;

DELIMITER $$

CREATE TRIGGER trg_sponsors_bi
BEFORE INSERT ON sponsors
FOR EACH ROW
BEGIN
    IF NOT EXISTS (SELECT 1 FROM teams WHERE team_id = NEW.team_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Team with such team_id does not exist';
    END IF;
END$$

CREATE TRIGGER trg_sponsors_bu
BEFORE UPDATE ON sponsors
FOR EACH ROW
BEGIN
    IF NOT EXISTS (SELECT 1 FROM teams WHERE team_id = NEW.team_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Team with such team_id does not exist';
    END IF;
END$$

CREATE TRIGGER trg_teams_bd
BEFORE DELETE ON teams
FOR EACH ROW
BEGIN
    DELETE FROM sponsors WHERE team_id = OLD.team_id;
END$$

CREATE TRIGGER trg_sponsors_amount_bi
BEFORE INSERT ON sponsors
FOR EACH ROW
BEGIN
    IF MOD(NEW.contract_amount, 100) = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'contract_amount must not end with two zeros';
    END IF;
END$$

CREATE TRIGGER trg_sponsors_amount_bu
BEFORE UPDATE ON sponsors
FOR EACH ROW
BEGIN
    IF MOD(NEW.contract_amount, 100) = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'contract_amount must not end with two zeros';
    END IF;
END$$

CREATE TRIGGER trg_seasons_bd
BEFORE DELETE ON seasons
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Deleting rows from seasons is forbidden';
END$$

CREATE TRIGGER trg_players_ad
AFTER DELETE ON players
FOR EACH ROW
BEGIN
    INSERT INTO players_delete_log (player_id, first_name, last_name, position, team_id, deleted_at)
    VALUES (OLD.player_id, OLD.first_name, OLD.last_name, OLD.position, OLD.team_id, NOW());
END$$

DELIMITER ;

INSERT INTO sponsors (name, team_id, contract_amount) VALUES
('Nike', 1, 1250075),
('Adidas', 2, 980050),
('Puma', 3, 450025),
('Parimatch', 1, 770030),
('Kernel', 6, 310015),
('Epicentr', 8, 205045);

INSERT INTO player_sponsors (player_id, sponsor_id) VALUES
(3, 1),
(7, 2),
(12, 5);

DROP PROCEDURE IF EXISTS sp_insert_player;
DROP PROCEDURE IF EXISTS sp_link_player_sponsor;
DROP PROCEDURE IF EXISTS sp_insert_noname_cities;
DROP FUNCTION  IF EXISTS fn_stadium_capacity_stat;
DROP PROCEDURE IF EXISTS sp_stadium_capacity_stat;
DROP PROCEDURE IF EXISTS sp_split_players_random;

DELIMITER $$

CREATE PROCEDURE sp_insert_player(
    IN p_first_name VARCHAR(50),
    IN p_last_name  VARCHAR(50),
    IN p_position   VARCHAR(10),
    IN p_team_id    INT UNSIGNED
)
BEGIN
    INSERT INTO players (first_name, last_name, position, team_id)
    VALUES (p_first_name, p_last_name, p_position, p_team_id);

    SELECT LAST_INSERT_ID() AS player_id;
END$$

CREATE PROCEDURE sp_link_player_sponsor(
    IN p_first_name   VARCHAR(50),
    IN p_last_name    VARCHAR(50),
    IN p_sponsor_name VARCHAR(100)
)
BEGIN
    DECLARE v_player_id  INT UNSIGNED DEFAULT NULL;
    DECLARE v_sponsor_id INT UNSIGNED DEFAULT NULL;

    SELECT player_id INTO v_player_id
    FROM players
    WHERE first_name = p_first_name AND last_name = p_last_name
    LIMIT 1;

    SELECT sponsor_id INTO v_sponsor_id
    FROM sponsors
    WHERE name = p_sponsor_name
    LIMIT 1;

    IF v_player_id IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Player with such first_name and last_name does not exist';
    END IF;

    IF v_sponsor_id IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Sponsor with such name does not exist';
    END IF;

    INSERT IGNORE INTO player_sponsors (player_id, sponsor_id) VALUES (v_player_id, v_sponsor_id);

    SELECT v_player_id AS player_id, v_sponsor_id AS sponsor_id;
END$$

CREATE PROCEDURE sp_insert_noname_cities()
BEGIN
    DECLARE v_start INT DEFAULT 0;
    DECLARE v_i     INT DEFAULT 1;

    SELECT IFNULL(MAX(CAST(SUBSTRING(name, 7) AS UNSIGNED)), 0)
    INTO v_start
    FROM cities
    WHERE name REGEXP '^Noname[0-9]+$';

    WHILE v_i <= 10 DO
        INSERT INTO cities (name) VALUES (CONCAT('Noname', v_start + v_i));
        SET v_i = v_i + 1;
    END WHILE;

    SELECT city_id, name
    FROM cities
    WHERE name REGEXP '^Noname[0-9]+$'
    ORDER BY city_id DESC
    LIMIT 10;
END$$

CREATE FUNCTION fn_stadium_capacity_stat(p_func VARCHAR(10))
RETURNS DECIMAL(20, 2)
READS SQL DATA
BEGIN
    DECLARE v_result DECIMAL(20, 2) DEFAULT NULL;

    IF UPPER(p_func) = 'MAX' THEN
        SELECT MAX(capacity) INTO v_result FROM stadiums;
    ELSEIF UPPER(p_func) = 'MIN' THEN
        SELECT MIN(capacity) INTO v_result FROM stadiums;
    ELSEIF UPPER(p_func) = 'SUM' THEN
        SELECT SUM(capacity) INTO v_result FROM stadiums;
    ELSEIF UPPER(p_func) = 'AVG' THEN
        SELECT AVG(capacity) INTO v_result FROM stadiums;
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Unsupported function, use MAX, MIN, SUM or AVG';
    END IF;

    RETURN v_result;
END$$

CREATE PROCEDURE sp_stadium_capacity_stat(IN p_func VARCHAR(10))
BEGIN
    SELECT UPPER(p_func) AS func, fn_stadium_capacity_stat(p_func) AS result;
END$$

CREATE PROCEDURE sp_split_players_random()
BEGIN
    DECLARE v_done      INT DEFAULT 0;
    DECLARE v_player_id INT UNSIGNED;
    DECLARE v_stamp     VARCHAR(30);
    DECLARE v_table_a   VARCHAR(64);
    DECLARE v_table_b   VARCHAR(64);
    DECLARE v_count_a   INT DEFAULT 0;
    DECLARE v_count_b   INT DEFAULT 0;
    DECLARE cur_players CURSOR FOR SELECT player_id FROM players;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = 1;

    SET v_stamp   = DATE_FORMAT(NOW(6), '%Y%m%d_%H%i%s_%f');
    SET v_table_a = CONCAT('players_', v_stamp, '_a');
    SET v_table_b = CONCAT('players_', v_stamp, '_b');

    SET @sql_create_a = CONCAT('CREATE TABLE `', v_table_a, '` LIKE players');
    PREPARE stmt_create_a FROM @sql_create_a;
    EXECUTE stmt_create_a;
    DEALLOCATE PREPARE stmt_create_a;

    SET @sql_create_b = CONCAT('CREATE TABLE `', v_table_b, '` LIKE players');
    PREPARE stmt_create_b FROM @sql_create_b;
    EXECUTE stmt_create_b;
    DEALLOCATE PREPARE stmt_create_b;

    SET @sql_insert_a = CONCAT('INSERT INTO `', v_table_a, '` SELECT * FROM players WHERE player_id = ?');
    SET @sql_insert_b = CONCAT('INSERT INTO `', v_table_b, '` SELECT * FROM players WHERE player_id = ?');
    PREPARE stmt_insert_a FROM @sql_insert_a;
    PREPARE stmt_insert_b FROM @sql_insert_b;

    OPEN cur_players;

    read_loop: LOOP
        FETCH cur_players INTO v_player_id;
        IF v_done = 1 THEN
            LEAVE read_loop;
        END IF;

        SET @row_player_id = v_player_id;

        IF RAND() < 0.5 THEN
            EXECUTE stmt_insert_a USING @row_player_id;
            SET v_count_a = v_count_a + 1;
        ELSE
            EXECUTE stmt_insert_b USING @row_player_id;
            SET v_count_b = v_count_b + 1;
        END IF;
    END LOOP;

    CLOSE cur_players;

    DEALLOCATE PREPARE stmt_insert_a;
    DEALLOCATE PREPARE stmt_insert_b;

    SELECT v_table_a AS table_a, v_count_a AS rows_a, v_table_b AS table_b, v_count_b AS rows_b;
END$$

DELIMITER ;
