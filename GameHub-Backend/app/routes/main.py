from flask import Blueprint, render_template, send_from_directory
from flask_login import login_required
from app.models import Noticia, Videojuego, Evento
import os

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

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'GameHub-Frontend')

@main.route('/frontend')
def frontend_index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@main.route('/frontend/<path:filename>')
def frontend_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)

@main.route('/assets/<path:filename>')
def frontend_assets(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, 'assets'), filename)

@main.route('/<page>.html')
def frontend_page(page):
    return send_from_directory(FRONTEND_DIR, f'{page}.html')