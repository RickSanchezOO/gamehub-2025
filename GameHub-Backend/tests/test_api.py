"""
Tests de integración de la API REST (`app.routes.api`).

Estos tests realizan peticiones HTTP simuladas contra el blueprint
`/api` y verifican el comportamiento de los endpoints más relevantes:
- Autenticación (registro/login/logout)
- Endpoints públicos (news, games, posts, media, events, team)
- Operaciones que requieren login (comentarios, dashboard)

Los tests usan la fixture `client` para ejecutar peticiones y la
fixture `app` para preparar la base de datos en memoria.
"""

from datetime import date

from app import db, bcrypt
from app.models import Usuario, Noticia, PostBlog, Comentario, Videojuego, Multimedia, Evento


def test_register_login_and_dashboard(client):
    register_response = client.post('/api/auth/register', json={
        'displayName': 'Prueba API',
        'email': 'prueba@api.test',
        'password': 'secret123'
    })
    assert register_response.status_code == 201
    json_data = register_response.get_json()
    assert json_data['message'] == 'Usuario registrado correctamente'
    assert json_data['user']['displayName'] == 'Prueba API'

    with client:
        login_response = client.post('/api/auth/login', json={
            'email': 'prueba@api.test',
            'password': 'secret123'
        })
        assert login_response.status_code == 200
        assert login_response.get_json()['message'] == 'Login correcto'

        dashboard_response = client.get('/api/dashboard')
        assert dashboard_response.status_code == 200
        dashboard_data = dashboard_response.get_json()
        assert 'user' in dashboard_data
        assert dashboard_data['user']['displayName'] == 'Prueba API'


def test_news_game_post_media_event_and_team_endpoints(client, app):
    # Insertamos datos directamente en la base de datos para que los
    # endpoints GET devuelvan contenido verificable.
    with app.app_context():
        usuario = Usuario(
            nombre='Periodista',
            email='reportero@test.com',
            password_hash=bcrypt.generate_password_hash('password').decode('utf-8'),
            rol='Redactor'
        )
        noticia = Noticia(
            autor=usuario,
            titulo='Noticia de prueba',
            cuerpo='Cuerpo de noticia de prueba',
            estado='publicada'
        )
        juego = Videojuego(
            nombre='Prueba Game',
            descripcion='Juego de prueba',
            nota_prensa=8.7,
            nota_comunidad=9.2,
            anio_lanzamiento=2025,
            genero='Acción'
        )
        post = PostBlog(
            autor=usuario,
            titulo='Post de prueba',
            contenido='Contenido detallado del post de prueba.'
        )
        multimedia = Multimedia(
            titulo='Trailer prueba',
            url_video='https://stream.test/preview',
            tipo='trailer'
        )
        evento = Evento(
            autor=usuario,
            nombre='Lanzamiento prueba',
            descripcion='Evento de lanzamiento',
            fecha_evento=date(2026, 1, 1),
            lugar='Ciudad prueba'
        )
        db.session.add_all([usuario, noticia, juego, post, multimedia, evento])
        db.session.commit()

    news_response = client.get('/api/news')
    assert news_response.status_code == 200
    assert len(news_response.get_json()) == 1
    assert news_response.get_json()[0]['title'] == 'Noticia de prueba'

    game_response = client.get('/api/games')
    assert game_response.status_code == 200
    games = game_response.get_json()
    assert len(games) == 1
    assert games[0]['title'] == 'Prueba Game'

    game_detail = client.get('/api/games/1')
    assert game_detail.status_code == 200
    assert game_detail.get_json()['genre'] == 'Acción'

    post_response = client.get('/api/posts')
    assert post_response.status_code == 200
    assert post_response.get_json()[0]['title'] == 'Post de prueba'

    media_response = client.get('/api/media')
    assert media_response.status_code == 200
    assert media_response.get_json()[0]['title'] == 'Trailer prueba'

    event_response = client.get('/api/events')
    assert event_response.status_code == 200
    assert event_response.get_json()[0]['name'] == 'Lanzamiento prueba'

    team_response = client.get('/api/team')
    assert team_response.status_code == 200
    assert any(member['role'] == 'Redactor' for member in team_response.get_json())


def test_comment_creation_requires_login_and_is_visible(client, app):
    with app.app_context():
        password = 'secret123'
        usuario = Usuario(
            nombre='Comentarista',
            email='comentario@test.com',
            password_hash=bcrypt.generate_password_hash(password).decode('utf-8')
        )
        post = PostBlog(
            autor=usuario,
            titulo='Post con comentarios',
            contenido='Texto del post'
        )
        db.session.add_all([usuario, post])
        db.session.commit()

    # Usamos el client como contexto para preservar la sesión entre
    # peticiones (login -> post comment -> get comments).
    with client:
        login_response = client.post('/api/auth/login', json={
            'email': 'comentario@test.com',
            'password': 'secret123'
        })
        assert login_response.status_code == 200

        comment_response = client.post('/api/posts/1/comments', json={'body': 'Excelente artículo'})
        assert comment_response.status_code == 201
        comment_data = comment_response.get_json()
        assert comment_data['body'] == 'Excelente artículo'
        assert comment_data['author'] == 'Comentarista'

        comments_response = client.get('/api/posts/1/comments')
        assert comments_response.status_code == 200
        comments = comments_response.get_json()
        assert len(comments) == 1
        assert comments[0]['body'] == 'Excelente artículo'


def test_contact_validation_and_submission(client):
    missing_response = client.post('/api/contact', json={'name': '', 'email': '', 'message': ''})
    assert missing_response.status_code == 400

    contact_response = client.post('/api/contact', json={
        'name': 'Julio',
        'email': 'julio@test.com',
        'message': 'Quiero información'
    })
    assert contact_response.status_code == 201
    assert contact_response.get_json()['message'] == 'Mensaje enviado correctamente'


def test_dashboard_endpoint_rejects_without_login(client):
    response = client.get('/api/dashboard')
    assert response.status_code in (302, 401)
