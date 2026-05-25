from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import Config

# Instancias globales de las extensiones
# Se inicializan aquí pero se vinculan a la app en create_app()
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    """Factoría de la aplicación Flask. Inicializa extensiones y registra blueprints."""
    app = Flask(__name__)
    
    # Carga la configuración desde el objeto Config
    app.config.from_object(Config)

    # Inicialización de extensiones con la app
    db.init_app(app)
    CORS(app)  # Permite peticiones desde el frontend externo
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Redirige al login si el usuario intenta acceder a una ruta protegida
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Debes iniciar sesión para acceder a esta página.'

    # Registro de blueprints — cada módulo agrupa rutas relacionadas
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
    app.register_blueprint(api)  # API REST para el frontend

    return app