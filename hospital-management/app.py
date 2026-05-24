from flask import Flask, redirect, url_for
from flask_wtf.csrf import CSRFProtect

from models import db, seed_data


csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "change-this-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///meditrack.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = "static/uploads"
    app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

    db.init_app(app)
    csrf.init_app(app)

    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.patients import patients_bp
    from routes.doctors import doctors_bp
    from routes.appointments import appointments_bp
    from routes.records import records_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(doctors_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(records_bp)

    @app.route("/")
    def index():
        return redirect(url_for("dashboard.dashboard"))

    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        seed_data()
        print("Meditrack database initialized with sample data.")

    return app


app = create_app()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True)
