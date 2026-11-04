import os
import yaml
from app.my_project import create_app

app = create_app()

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), "app", "config", "app.yml")
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    srv = cfg.get("server", {})
    app.run(
        host=srv.get("host", "127.0.0.1"),
        port=srv.get("port", 5000),
        debug=srv.get("debug", True)
    )
