DROP DATABASE IF EXISTS footboom_upl;
CREATE DATABASE IF NOT EXISTS footboom_upl
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE footboom_upl;

DROP TABLE IF EXISTS cards;
DROP TABLE IF EXISTS goals;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS coaches;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS stadiums;
DROP TABLE IF EXISTS referees;
DROP TABLE IF EXISTS seasons;
DROP TABLE IF EXISTS cities;

CREATE TABLE cities (
    city_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name    VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE stadiums (
    stadium_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(150) NOT NULL,
    city_id    INT UNSIGNED NOT NULL,
    capacity   INT UNSIGNED NOT NULL,
    CONSTRAINT fk_stadium_city FOREIGN KEY (city_id) REFERENCES cities(city_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE teams (
    team_id    INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    short_name VARCHAR(10) NOT NULL,
    stadium_id INT UNSIGNED NOT NULL,
    CONSTRAINT fk_team_stadium FOREIGN KEY (stadium_id) REFERENCES stadiums(stadium_id) ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE coaches (
    coach_id   INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name  VARCHAR(50) NOT NULL,
    team_id    INT UNSIGNED NOT NULL,
    CONSTRAINT fk_coach_team FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE players (
    player_id  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name  VARCHAR(50) NOT NULL,
    position   ENUM('GK', 'DEF', 'MID', 'FWD') NOT NULL,
    team_id    INT UNSIGNED NOT NULL,
    CONSTRAINT fk_player_team FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE seasons (
    season_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name      VARCHAR(20) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE referees (
    referee_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name  VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE matches (
    match_id     INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    season_id    INT UNSIGNED NOT NULL,
    matchday     TINYINT UNSIGNED NOT NULL,
    match_date   DATETIME NOT NULL,
    home_team_id INT UNSIGNED NOT NULL,
    away_team_id INT UNSIGNED NOT NULL,
    referee_id   INT UNSIGNED NOT NULL,
    home_score   TINYINT UNSIGNED DEFAULT NULL,
    away_score   TINYINT UNSIGNED DEFAULT NULL,
    status       ENUM('scheduled', 'finished', 'postponed') DEFAULT 'scheduled',
    CONSTRAINT fk_match_season  FOREIGN KEY (season_id)    REFERENCES seasons(season_id) ON DELETE CASCADE,
    CONSTRAINT fk_match_home    FOREIGN KEY (home_team_id) REFERENCES teams(team_id) ON DELETE CASCADE,
    CONSTRAINT fk_match_away    FOREIGN KEY (away_team_id) REFERENCES teams(team_id) ON DELETE CASCADE,
    CONSTRAINT fk_match_referee FOREIGN KEY (referee_id)   REFERENCES referees(referee_id) ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE goals (
    goal_id   INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    match_id  INT UNSIGNED NOT NULL,
    player_id INT UNSIGNED NOT NULL,
    minute    TINYINT UNSIGNED NOT NULL,
    goal_type ENUM('regular', 'penalty', 'own_goal', 'free_kick') DEFAULT 'regular',
    CONSTRAINT fk_goal_match  FOREIGN KEY (match_id)  REFERENCES matches(match_id) ON DELETE CASCADE,
    CONSTRAINT fk_goal_player FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE cards (
    card_id   INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    match_id  INT UNSIGNED NOT NULL,
    player_id INT UNSIGNED NOT NULL,
    minute    TINYINT UNSIGNED NOT NULL,
    card_type ENUM('yellow', 'red') NOT NULL,
    CONSTRAINT fk_card_match  FOREIGN KEY (match_id)  REFERENCES matches(match_id) ON DELETE CASCADE,
    CONSTRAINT fk_card_player FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_matches_date ON matches(match_date);
CREATE INDEX idx_players_search ON players(last_name, position);
CREATE INDEX idx_goals_player ON goals(player_id);

INSERT INTO cities (city_id, name) VALUES
(1, 'Київ'),
(2, 'Львів'),
(3, 'Донецьк'),
(4, 'Харків'),
(5, 'Одеса'),
(6, 'Дніпро'),
(7, 'Запоріжжя'),
(8, 'Полтава'),
(9, 'Житомир'),
(10, 'Ковалівка');

INSERT INTO stadiums (stadium_id, name, city_id, capacity) VALUES
(1, 'НСК Олімпійський', 1, 70050),
(2, 'Арена Львів', 2, 34915),
(3, 'Донбас Арена', 3, 52518),
(4, 'Металіст', 4, 40003),
(5, 'Чорноморець', 5, 34164),
(6, 'Дніпро-Арена', 6, 31003),
(7, 'Славутич-Арена', 7, 12000),
(8, 'Ворскла ім. Бутовського', 8, 24795),
(9, 'Центральний міський стадіон', 9, 10000),
(10, 'Колос Арена', 10, 5000);

INSERT INTO teams (team_id, name, short_name, stadium_id) VALUES
(1, 'Динамо Київ', 'ДИН', 1),
(2, 'Шахтар Донецьк', 'ШАХ', 3),
(3, 'Рух Львів', 'РУХ', 2),
(4, 'Металіст 1925', 'МЕТ', 4),
(5, 'Чорноморець Одеса', 'ЧОР', 5),
(6, 'СК Дніпро-1', 'ДНІ', 6),
(7, 'Зоря Луганськ', 'ЗОР', 7),
(8, 'Ворскла Полтава', 'ВОР', 8),
(9, 'Полісся Житомир', 'ПОЛ', 9),
(10, 'Колос Ковалівка', 'КОЛ', 10);

INSERT INTO coaches (coach_id, first_name, last_name, team_id) VALUES
(1, 'Олександр', 'Шовковський', 1),
(2, 'Маріно', 'Пушич', 2),
(3, 'Віталій', 'Пономарьов', 3),
(4, 'Віктор', 'Скрипник', 4),
(5, 'Роман', 'Григорчук', 5),
(6, 'Юрій', 'Максимов', 6),
(7, 'Валерій', 'Кривенцов', 7),
(8, 'Сергій', 'Долганський', 8),
(9, 'Імад', 'Ашур', 9),
(10, 'Олександр', 'Поздєєв', 10);

INSERT INTO players (player_id, first_name, last_name, position, team_id) VALUES
(1, 'Георгій', 'Бущан', 'GK', 1),
(2, 'Микола', 'Шапаренко', 'MID', 1),
(3, 'Андрій', 'Ярмоленко', 'MID', 1),
(4, 'Владислав', 'Ванат', 'FWD', 1),
(5, 'Дмитро', 'Різник', 'GK', 2),
(6, 'Тарас', 'Степаненко', 'MID', 2),
(7, 'Георгій', 'Судаков', 'MID', 2),
(8, 'Данило', 'Сікан', 'FWD', 2),
(9, 'Юрій', 'Климчук', 'FWD', 3),
(10, 'Марко', 'Сапуга', 'MID', 3),
(11, 'Олексій', 'Гуцуляк', 'MID', 6),
(12, 'Артем', 'Довбик', 'FWD', 6),
(13, 'Артем', 'Бондаренко', 'MID', 2),
(14, 'Олександр', 'Тимчик', 'DEF', 1),
(15, 'Ігор', 'Пердута', 'DEF', 8);

INSERT INTO seasons (season_id, name) VALUES
(1, '2015/2016'),
(2, '2016/2017'),
(3, '2017/2018'),
(4, '2018/2019'),
(5, '2019/2020'),
(6, '2020/2021'),
(7, '2021/2022'),
(8, '2022/2023'),
(9, '2023/2024'),
(10, '2024/2025');

INSERT INTO referees (referee_id, first_name, last_name) VALUES
(1, 'Микола', 'Балакін'),
(2, 'Катерина', 'Монзуль'),
(3, 'Віталій', 'Романов'),
(4, 'Євген', 'Арановський'),
(5, 'Олександр', 'Дердо'),
(6, 'Юрій', 'Іванов'),
(7, 'Ігор', 'Пасхал'),
(8, 'Сергій', 'Бойко'),
(9, 'Анатолій', 'Абдула'),
(10, 'Дмитро', 'Панчишин');

INSERT INTO matches (match_id, season_id, matchday, match_date, home_team_id, away_team_id, referee_id, home_score, away_score, status) VALUES
(1, 10, 1, '2024-08-03 18:00:00', 1, 2, 1, 2, 1, 'finished'),
(2, 10, 1, '2024-08-04 15:30:00', 3, 5, 2, 1, 0, 'finished'),
(3, 10, 2, '2024-08-10 18:00:00', 2, 3, 3, 3, 0, 'finished'),
(4, 10, 2, '2024-08-11 17:00:00', 6, 8, 4, 1, 1, 'finished'),
(5, 10, 3, '2024-08-17 15:00:00', 5, 1, 5, 0, 2, 'finished'),
(6, 10, 3, '2024-08-18 19:30:00', 9, 10, 6, 2, 0, 'finished'),
(7, 10, 4, '2024-08-24 17:00:00', 4, 7, 7, 1, 2, 'finished'),
(8, 10, 4, '2024-08-25 19:00:00', 1, 6, 8, 3, 1, 'finished'),
(9, 10, 5, '2024-08-31 16:00:00', 8, 2, 9, 0, 4, 'finished'),
(10, 10, 5, '2024-09-01 18:00:00', 7, 9, 10, 1, 1, 'finished'),
(11, 10, 6, '2024-09-14 17:00:00', 2, 1, 1, NULL, NULL, 'scheduled'),
(12, 10, 6, '2024-09-15 15:00:00', 3, 6, 2, NULL, NULL, 'scheduled');

INSERT INTO goals (goal_id, match_id, player_id, minute, goal_type) VALUES
(1, 1, 4, 21, 'regular'),
(2, 1, 7, 44, 'regular'),
(3, 1, 3, 82, 'penalty'),
(4, 2, 9, 65, 'regular'),
(5, 3, 8, 12, 'regular'),
(6, 3, 8, 55, 'regular'),
(7, 3, 13, 78, 'free_kick'),
(8, 4, 12, 33, 'penalty'),
(9, 5, 4, 19, 'regular'),
(10, 5, 2, 74, 'regular'),
(11, 8, 4, 10, 'regular'),
(12, 8, 3, 50, 'regular');

INSERT INTO cards (card_id, match_id, player_id, minute, card_type) VALUES
(1, 1, 6, 32, 'yellow'),
(2, 1, 14, 67, 'yellow'),
(3, 1, 6, 89, 'red'),
(4, 2, 10, 41, 'yellow'),
(5, 3, 9, 25, 'yellow'),
(6, 4, 15, 60, 'yellow'),
(7, 5, 2, 70, 'yellow'),
(8, 7, 10, 83, 'yellow'),
(9, 8, 11, 15, 'yellow'),
(10, 8, 14, 77, 'yellow'),
(11, 9, 15, 45, 'red');