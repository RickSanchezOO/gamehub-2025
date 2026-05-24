from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Noticia, Videojuego, Evento

main = Blueprint('main', __name__)

@main.route('/')
def index():
    noticias = Noticia.query.filter_by(estado='publicada').order_by(Noticia.fecha_publicacion.desc()).limit(5).all()
    videojuegos = Videojuego.query.order_by(Videojuego.nota_comunidad.desc()).limit(6).all()
    eventos = Evento.query.order_by(Evento.fecha_evento.asc()).limit(4).all()
    return render_template('main/index.html', noticias=noticias, videojuegos=videojuegos, eventos=eventos)

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dashboard.html')