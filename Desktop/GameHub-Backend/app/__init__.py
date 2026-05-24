from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Debes iniciar sesión para acceder a esta página.'

    from app.routes.auth import auth
    from app.routes.main import main
    from app.routes.noticias import noticias
    from app.routes.blog import blog
    from app.routes.videojuegos import videojuegos
    from app.routes.multimedia import multimedia
    from app.routes.eventos import eventos
    from app.routes.contacto import contacto
    from app.routes.admin import admin
    from app.routes.api import api

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(noticias)
    app.register_blueprint(blog)
    app.register_blueprint(videojuegos)
    app.register_blueprint(multimedia)
    app.register_blueprint(eventos)
    app.register_blueprint(contacto)
    app.register_blueprint(admin)
    app.register_blueprint(api)

    return app