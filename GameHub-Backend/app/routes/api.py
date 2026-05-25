from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import Usuario, Noticia, PostBlog, Comentario, Videojuego, Multimedia, Evento, Contacto
from datetime import datetime

# Blueprint de la API REST — todas las rutas tienen el prefijo /api
api = Blueprint('api', __name__, url_prefix='/api')

# ── AUTH ──────────────────────────────────────────────────────────────────────

@api.route('/auth/register', methods=['POST'])
def register():
    """Registro de usuario vía API. Recibe JSON con displayName, email y password."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos no recibidos'}), 400
    nombre = data.get('displayName', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    if not nombre or not email or not password:
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400
    if Usuario.query.filter_by(email=email).first():
        return jsonify({'error': 'Ya existe una cuenta con ese email'}), 409
    # Encriptamos la contraseña antes de guardarla
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    usuario = Usuario(nombre=nombre, email=email, password_hash=password_hash)
    db.session.add(usuario)
    db.session.commit()
    return jsonify({
        'message': 'Usuario registrado correctamente',
        'user': {
            'id': usuario.id,
            'displayName': usuario.nombre,
            'role': usuario.rol
        }
    }), 201

@api.route('/auth/login', methods=['POST'])
def login():
    """Login vía API. Devuelve datos del usuario si las credenciales son correctas."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos no recibidos'}), 400
    email = data.get('email', '').strip()
    password = data.get('password', '')
    usuario = Usuario.query.filter_by(email=email).first()
    # Verificamos credenciales y estado de la cuenta
    if not usuario or not bcrypt.check_password_hash(usuario.password_hash, password):
        return jsonify({'error': 'Email o contraseña incorrectos'}), 401
    if not usuario.activo:
        return jsonify({'error': 'Cuenta suspendida'}), 403
    login_user(usuario)
    usuario.ultimo_acceso = datetime.utcnow()
    db.session.commit()
    return jsonify({
        'message': 'Login correcto',
        'user': {
            'id': usuario.id,
            'displayName': usuario.nombre,
            'role': usuario.rol
        }
    }), 200

@api.route('/auth/logout', methods=['POST'])
@login_required
def logout():
    """Cierre de sesión vía API."""
    logout_user()
    return jsonify({'message': 'Sesión cerrada'}), 200

# ── NOTICIAS ──────────────────────────────────────────────────────────────────

@api.route('/news', methods=['GET'])
def get_news():
    """Devuelve todas las noticias publicadas ordenadas por fecha descendente."""
    noticias = Noticia.query.filter_by(estado='publicada').order_by(Noticia.fecha_publicacion.desc()).all()
    return jsonify([{
        'id': n.id,
        'title': n.titulo,
        'excerpt': n.cuerpo[:150] + '...' if len(n.cuerpo) > 150 else n.cuerpo,
        'author': n.autor.nombre if n.autor else 'Redacción',
        'date': n.fecha_publicacion.strftime('%Y-%m-%d'),
        'image': n.imagen,
        'tags': n.etiquetas,
        'status': n.estado
    } for n in noticias])

@api.route('/news/<int:id>', methods=['GET'])
def get_noticia(id):
    """Devuelve el detalle completo de una noticia por su ID."""
    n = Noticia.query.get_or_404(id)
    return jsonify({
        'id': n.id,
        'title': n.titulo,
        'body': n.cuerpo,
        'author': n.autor.nombre if n.autor else 'Redacción',
        'date': n.fecha_publicacion.strftime('%Y-%m-%d'),
        'image': n.imagen,
        'tags': n.etiquetas,
        'status': n.estado
    })

# ── VIDEOJUEGOS ───────────────────────────────────────────────────────────────

@api.route('/games', methods=['GET'])
def get_games():
    """Devuelve todos los videojuegos ordenados por nota de comunidad descendente."""
    juegos = Videojuego.query.order_by(Videojuego.nota_comunidad.desc()).all()
    return jsonify([{
        'id': j.id,
        'title': j.nombre,
        'genre': j.genero,
        'description': j.descripcion,
        'image': j.imagen,
        'pressScore': float(j.nota_prensa) if j.nota_prensa else None,
        'communityScore': float(j.nota_comunidad) if j.nota_comunidad else None,
        'year': j.anio_lanzamiento
    } for j in juegos])

@api.route('/games/<int:id>', methods=['GET'])
def get_game(id):
    """Devuelve el detalle de un videojuego por su ID."""
    j = Videojuego.query.get_or_404(id)
    return jsonify({
        'id': j.id,
        'title': j.nombre,
        'genre': j.genero,
        'description': j.descripcion,
        'image': j.imagen,
        'pressScore': float(j.nota_prensa) if j.nota_prensa else None,
        'communityScore': float(j.nota_comunidad) if j.nota_comunidad else None,
        'year': j.anio_lanzamiento
    })

@api.route('/games/ranking', methods=['GET'])
def get_ranking():
    """Devuelve el top 10 de videojuegos por nota de comunidad."""
    juegos = Videojuego.query.order_by(Videojuego.nota_comunidad.desc()).limit(10).all()
    return jsonify([{
        'id': j.id,
        'title': j.nombre,
        'communityScore': float(j.nota_comunidad) if j.nota_comunidad else None,
        'pressScore': float(j.nota_prensa) if j.nota_prensa else None,
        'image': j.imagen
    } for j in juegos])

# ── BLOG ──────────────────────────────────────────────────────────────────────

@api.route('/posts', methods=['GET'])
def get_posts():
    """Devuelve todos los posts del blog ordenados por fecha descendente."""
    posts = PostBlog.query.order_by(PostBlog.fecha_publicacion.desc()).all()
    return jsonify([{
        'id': p.id,
        'title': p.titulo,
        'excerpt': p.contenido[:150] + '...' if len(p.contenido) > 150 else p.contenido,
        'author': p.autor.nombre if p.autor else 'Redacción',
        'date': p.fecha_publicacion.strftime('%Y-%m-%d'),
        'image': p.imagen,
        'commentsActive': p.comentarios_activos
    } for p in posts])

@api.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    """Devuelve el detalle completo de un post por su ID."""
    p = PostBlog.query.get_or_404(id)
    return jsonify({
        'id': p.id,
        'title': p.titulo,
        'body': p.contenido,
        'author': p.autor.nombre if p.autor else 'Redacción',
        'date': p.fecha_publicacion.strftime('%Y-%m-%d'),
        'image': p.imagen,
        'commentsActive': p.comentarios_activos
    })

@api.route('/posts/<int:id>/comments', methods=['GET'])
def get_comments(id):
    """Devuelve los comentarios no eliminados de un post."""
    PostBlog.query.get_or_404(id)
    comentarios = Comentario.query.filter_by(post_id=id, eliminado=False).order_by(Comentario.fecha_creacion.desc()).all()
    return jsonify([{
        'id': c.id,
        'author': c.usuario.nombre if c.usuario else 'Usuario',
        'body': c.contenido,
        'createdAt': c.fecha_creacion.strftime('%Y-%m-%dT%H:%M:%S')
    } for c in comentarios])

@api.route('/posts/<int:id>/comments', methods=['POST'])
@login_required
def post_comment(id):
    """Publica un comentario en un post. Requiere sesión iniciada."""
    PostBlog.query.get_or_404(id)
    data = request.get_json()
    contenido = data.get('body', '').strip()
    if not contenido:
        return jsonify({'error': 'El comentario no puede estar vacío'}), 400
    comentario = Comentario(contenido=contenido, post_id=id, usuario_id=current_user.id)
    db.session.add(comentario)
    db.session.commit()
    return jsonify({
        'id': comentario.id,
        'author': current_user.nombre,
        'body': comentario.contenido,
        'createdAt': comentario.fecha_creacion.strftime('%Y-%m-%dT%H:%M:%S')
    }), 201

# ── MULTIMEDIA ────────────────────────────────────────────────────────────────

@api.route('/media', methods=['GET'])
def get_media():
    """Devuelve todos los contenidos multimedia ordenados por fecha descendente."""
    items = Multimedia.query.order_by(Multimedia.fecha_alta.desc()).all()
    return jsonify([{
        'id': m.id,
        'title': m.titulo,
        'url': m.url_video,
        'type': m.tipo,
        'date': m.fecha_alta.strftime('%Y-%m-%d')
    } for m in items])

# ── EVENTOS ───────────────────────────────────────────────────────────────────

@api.route('/events', methods=['GET'])
def get_events():
    """Devuelve todos los eventos ordenados por fecha ascendente (próximos primero)."""
    eventos = Evento.query.order_by(Evento.fecha_evento.asc()).all()
    return jsonify([{
        'id': e.id,
        'name': e.nombre,
        'description': e.descripcion,
        'date': str(e.fecha_evento),
        'location': e.lugar
    } for e in eventos])

# ── CONTACTO ──────────────────────────────────────────────────────────────────

@api.route('/contact', methods=['POST'])
def contact():
    """Recibe un mensaje de contacto y lo guarda en la base de datos."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos no recibidos'}), 400
    nombre = data.get('name', '').strip()
    email = data.get('email', '').strip()
    mensaje = data.get('message', '').strip()
    if not nombre or not email or not mensaje:
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400
    contacto = Contacto(
        nombre=nombre, email=email, mensaje=mensaje,
        usuario_id=current_user.id if current_user.is_authenticated else None
    )
    db.session.add(contacto)
    db.session.commit()
    return jsonify({'message': 'Mensaje enviado correctamente'}), 201

# ── DASHBOARD ─────────────────────────────────────────────────────────────────

@api.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Devuelve estadísticas del usuario autenticado para el panel personal."""
    comentarios = Comentario.query.filter_by(usuario_id=current_user.id, eliminado=False).count()
    return jsonify({
        'welcome': f'Bienvenido de nuevo, {current_user.nombre}.',
        'user': {
            'id': current_user.id,
            'displayName': current_user.nombre,
            'email': current_user.email,
            'role': current_user.rol
        },
        'stats': [
            {'label': 'Comentarios publicados', 'value': comentarios}
        ]
    })

# ── EQUIPO ────────────────────────────────────────────────────────────────────

@api.route('/team', methods=['GET'])
def get_team():
    """Devuelve los usuarios con rol editorial (Administrador, Redactor, Colaborador)."""
    redactores = Usuario.query.filter(
        Usuario.rol.in_(['Administrador', 'Redactor', 'Colaborador']),
        Usuario.activo == True
    ).all()
    return jsonify([{
        'id': u.id,
        'displayName': u.nombre,
        'role': u.rol
    } for u in redactores])