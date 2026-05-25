"""
Tests unitarios para los modelos SQLAlchemy definidos en `app.models`.

Cada test crea y persiste objetos en la base de datos en memoria
proporcionada por la fixture `app` (ver `conftest.py`). Esto asegura
aislamiento y que las pruebas no dependan de una base de datos externa.
"""

from datetime import date

from app import db, bcrypt
from app.models import Usuario, Noticia, PostBlog, Comentario, Videojuego, Multimedia, Evento, Contacto


def test_usuario_model_creation(app):
    usuario = Usuario(
        nombre='Juan Test',
        email='juan@test.com',
        password_hash=bcrypt.generate_password_hash('123456').decode('utf-8')
    )
    db.session.add(usuario)
    db.session.commit()

    assert Usuario.query.count() == 1
    stored = Usuario.query.filter_by(email='juan@test.com').first()
    assert stored is not None
    assert stored.nombre == 'Juan Test'
    assert stored.activo is True


def test_blog_post_and_comment_relationship(app):
    usuario = Usuario(
        nombre='Maria Blog',
        email='maria@test.com',
        password_hash=bcrypt.generate_password_hash('123456').decode('utf-8')
    )
    post = PostBlog(
        autor=usuario,
        titulo='Entrada de prueba',
        contenido='Contenido del post de prueba.'
    )
    comentario = Comentario(
        usuario=usuario,
        post=post,
        contenido='Comentario de prueba'
    )
    db.session.add_all([usuario, post, comentario])
    db.session.commit()

    assert PostBlog.query.count() == 1
    assert Comentario.query.count() == 1
    assert comentario.post.titulo == 'Entrada de prueba'
    assert comentario.usuario.email == 'maria@test.com'


def test_videojuego_media_evento_models(app):
    juego = Videojuego(
        nombre='Game Test',
        descripcion='Descripción de videojuego',
        nota_prensa=8.5,
        nota_comunidad=9.0,
        anio_lanzamiento=2025,
        genero='Aventura'
    )
    # Multimedia y Evento: comprobamos atributos básicos
    multimedia = Multimedia(
        titulo='Trailer Test',
        url_video='https://video.test/trailer',
        tipo='trailer'
    )
    evento = Evento(
        nombre='Evento Test',
        descripcion='Descripción de evento',
        # Usar un objeto date para compatibilidad con SQLite
        fecha_evento=date(2025, 10, 10),
        lugar='Sede Test'
    )
    db.session.add_all([juego, multimedia, evento])
    db.session.commit()

    assert Videojuego.query.first().nombre == 'Game Test'
    assert Multimedia.query.first().tipo == 'trailer'
    assert Evento.query.first().lugar == 'Sede Test'


def test_contacto_model(app):
    contacto = Contacto(
        nombre='Luis Contacto',
        email='luis@test.com',
        mensaje='Mensaje de prueba'
    )
    db.session.add(contacto)
    db.session.commit()

    saved = Contacto.query.first()
    assert saved.nombre == 'Luis Contacto'
    assert saved.leido is False
