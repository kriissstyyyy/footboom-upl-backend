import os
import yaml
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    config_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "config", "app.yml")
    )
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    db_cfg = cfg["db"]
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{db_cfg['user']}:{db_cfg['password']}@"
        f"{db_cfg['host']}:{db_cfg['port']}/{db_cfg['database']}?charset=utf8mb4"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        from app.my_project.auth.route.city_route import city_bp
        from app.my_project.auth.route.team_route import team_bp
        from app.my_project.auth.route.player_route import player_bp
        from app.my_project.auth.route.match_route import match_bp

        app.register_blueprint(city_bp, url_prefix="/api/cities")
        app.register_blueprint(team_bp, url_prefix="/api/teams")
        app.register_blueprint(player_bp, url_prefix="/api/players")
        app.register_blueprint(match_bp, url_prefix="/api/matches")

    return app
