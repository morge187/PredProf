import os
from flask import Flask, jsonify
from flask_cors import CORS
from database import init_db, get_db_session
from models import User
from auth import hash_password
from settings import settings
from routes.main.main import main_page

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    app.config["WTF_CSRF_ENABLED"] = True
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    init_db()

    with get_db_session() as db:
        admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
        if not admin:
            admin = User(
                email=settings.ADMIN_EMAIL,
                passwordHash=hash_password(settings.ADMIN_PASSWORD),
                role="ADMIN",
                isActive=True
            )
            db.add(admin)
            db.commit()

    app.register_blueprint(main_page)

    @app.route("/ping", methods=["GET"])
    def ping():
        return jsonify({"status": "ok"}), 200
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=False)