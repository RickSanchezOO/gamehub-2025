import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

class Config:
    # Clave secreta para firmar sesiones y tokens CSRF
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave_por_defecto')
    
    # URI de conexión a la base de datos MySQL usando PyMySQL como conector
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    
    # Desactiva el sistema de seguimiento de modificaciones de SQLAlchemy
    # para mejorar el rendimiento
    SQLALCHEMY_TRACK_MODIFICATIONS = False