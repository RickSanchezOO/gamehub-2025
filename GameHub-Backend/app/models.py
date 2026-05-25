from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

# Callback que Flask-Login usa para recargar el usuario desde la sesión
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(db.Model, UserMixin):
    """Modelo de usuario. Gestiona autenticación, roles e idioma."""
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    foto_perfil = db.Column(db.String(255), nullable=True)
    rol = db.Column(db.Enum('Administrador','Redactor','Colaborador','Suscriptor'), nullable=False, default='Suscriptor')
    idioma = db.Column(db.Enum('es','en'), nullable=False, default='es')
    activo = db.Column(db.Boolean, nullable=False, default=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_acceso = db.Column(db.DateTime, nullable=True)

    # Relaciones con otros modelos
    noticias = db.relationship('Noticia', backref='autor', lazy=True, foreign_keys='Noticia.autor_id')
    posts = db.relationship('PostBlog', backref='autor', lazy=True, foreign_keys='PostBlog.autor_id')
    comentarios = db.relationship('Comentario', backref='usuario', lazy=True, foreign_keys='Comentario.usuario_id')
    multimedia = db.relationship('Multimedia', backref='autor', lazy=True, foreign_keys='Multimedia.autor_id')
    eventos = db.relationship('Evento', backref='autor', lazy=True, foreign_keys='Evento.autor_id')
    videojuegos = db.relationship('Videojuego', backref='autor', lazy=True, foreign_keys='Videojuego.autor_id')

class Noticia(db.Model):
    """Modelo de noticia. Soporta borradores y publicación programada."""
    __tablename__ = 'noticia'
    id = db.Column(db.Integer, primary_key=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='SET NULL'), nullable=True)
    titulo = db.Column(db.String(255), nullable=False)
    cuerpo = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(255), nullable=True)
    etiquetas = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.Enum('publicada','borrador'), nullable=False, default='borrador')
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_programada = db.Column(db.DateTime, nullable=True)

class PostBlog(db.Model):
    """Modelo de post de blog con soporte de comentarios."""
    __tablename__ = 'post_blog'
    id = db.Column(db.Integer, primary_key=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='SET NULL'), nullable=True)
    titulo = db.Column(db.String(255), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(255), nullable=True)
    comentarios_activos = db.Column(db.Boolean, nullable=False, default=True)
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)
    comentarios = db.relationship('Comentario', backref='post', lazy=True, cascade='all, delete-orphan')

class Comentario(db.Model):
    """Modelo de comentario asociado a un post de blog."""
    __tablename__ = 'comentario'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='SET NULL'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post_blog.id', ondelete='CASCADE'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    eliminado = db.Column(db.Boolean, nullable=False, default=False)  # Borrado lógico
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class Videojuego(db.Model):
    """Modelo de videojuego con notas de prensa y comunidad."""
    __tablename__ = 'videojuego'
    id = db.Column(db.Integer, primary_key=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='SET NULL'), nullable=True)
    nombre = db.Column(db.String(255), nullable=False, unique=True)
    imagen = db.Column(db.String(255), nullable=True)
    descripcion = db.Column(db.Text, nullable=True)
    nota_prensa = db.Column(db.Numeric(4,2), nullable=True)
    nota_comunidad = db.Column(db.Numeric(4,2), nullable=True)
    anio_lanzamiento = db.Column(db.Integer, nullable=True)
    genero = db.Column(db.String(100), nullable=True)

class Multimedia(db.Model):
    """Modelo de contenido multimedia (trailers, streams, gameplay)."""
    __tablename__ = 'multimedia'
    id = db.Column(db.Integer, primary_key=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='SET NULL'), nullable=True)
    titulo = db.Column(db.String(255), nullable=False)
    url_video = db.Column(db.String(500), nullable=False)
    tipo = db.Column(db.Enum('trailer','stream','gameplay','otro'), nullable=False, default='otro')
    fecha_alta = db.Column(db.DateTime, default=datetime.utcnow)

class Evento(db.Model):
    """Modelo de evento de la industria del videojuego."""
    __tablename__ = 'evento'
    id = db.Column(db.Integer, primary_key=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='SET NULL'), nullable=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    fecha_evento = db.Column(db.Date, nullable=False)
    lugar = db.Column(db.String(255), nullable=True)

class Contacto(db.Model):
    """Modelo de mensaje de contacto enviado por usuarios."""
    __tablename__ = 'contacto'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='SET NULL'), nullable=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.DateTime, default=datetime.utcnow)
    leido = db.Column(db.Boolean, nullable=False, default=False)