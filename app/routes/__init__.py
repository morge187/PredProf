from .auth import bp as auth_bp
from .student import bp as student_bp
from .cook import bp as cook_bp
from .admin import bp as admin_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(cook_bp)
    app.register_blueprint(admin_bp)
