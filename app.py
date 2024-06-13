from flask import Flask
from dbinit import db
from flask_migrate import Migrate
from routes.auth import auth
from routes.main import main
from flask_login import LoginManager
from models.user import User

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()

    manager = LoginManager()
    manager.login_view = "auth.login"
    manager.init_app(app)

    @manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app