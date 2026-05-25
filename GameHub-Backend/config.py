import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

class Config:
    # Clave secreta para firmar sesiones y tokens CSRF
    # - Durante pruebas y desarrollo se proporciona un valor por defecto
    #   para evitar fallos cuando no exista un .env con SECRET_KEY.
    # - En producción, define `SECRET_KEY` en el entorno o en .env.
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave_por_defecto')

    # Configuración de la base de datos
    # -------------------------------------------------
    # Flujo de decisión:
    # 1) Si se proporcionan las 5 variables MySQL (DB_USER, DB_PASSWORD,
    #    DB_HOST, DB_PORT, DB_NAME), se construye la URI para MySQL/PyMySQL.
    # 2) Si no están todas, se usa la variable `SQLALCHEMY_DATABASE_URI`
    #    si está definida, o por defecto un archivo SQLite local
    #    (`sqlite:///gamehub.db`). Esto facilita pruebas aisladas.
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    if DB_USER and DB_PASSWORD and DB_HOST and DB_PORT and DB_NAME:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
            f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    else:
        # Fallback seguro para desarrollo y pruebas locales
        SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///gamehub.db')

    # Desactiva el sistema de seguimiento de modificaciones de SQLAlchemy
    # para mejorar el rendimiento y evitar warnings innecesarios.
    SQLALCHEMY_TRACK_MODIFICATIONS = False