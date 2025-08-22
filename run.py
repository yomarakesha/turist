import os
from flask_migrate import Migrate
from app import app, db

migrate = Migrate(app, db)

if __name__ == "__main__":
    # Для локальной разработки:
    debug = os.environ.get("FLASK_DEBUG", "False").lower() in ("1", "true", "yes")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=debug)
