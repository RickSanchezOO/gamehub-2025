from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Noticia
from datetime import datetime

noticias = Blueprint('noticias', __name__, url_prefix='/noticias')

@noticias.route('/')
def lista():
    page = request.args.get('page', 1, type=int)
    noticias_list = Noticia.query.filter_by(estado='publicada').order_by(Noticia.fecha_publicacion.desc()).paginate(page=page, per_page=10)
    return render_template('noticias/lista.html', noticias=noticias_list)

@noticias.route('/<int:id>')
def detalle(id):
    noticia = Noticia.query.get_or_404(id)
    if noticia.estado == 'borrador' and (not current_user.is_authenticated or current_user.rol not in ['Administrador', 'Redactor']):
        abort(404)
    return render_template('noticias/detalle.html', noticia=noticia)

@noticias.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if current_user.rol not in ['Administrador', 'Redactor']:
        abort(403)
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        cuerpo = request.form.get('cuerpo', '').strip()
        imagen = request.form.get('imagen', '').strip()
        etiquetas = request.form.get('etiquetas', '').strip()
        estado = request.form.get('estado', 'borrador')
        fecha_prog = request.form.get('fecha_programada', '')
        if not titulo or not cuerpo:
            flash('El título y el cuerpo son obligatorios.', 'danger')
            return render_template('noticias/form.html')
        noticia = Noticia(
            titulo=titulo, cuerpo=cuerpo, imagen=imagen or None,
            etiquetas=etiquetas or None, estado=estado,
            autor_id=current_user.id,
            fecha_programada=datetime.strptime(fecha_prog, '%Y-%m-%dT%H:%M') if fecha_prog else None
        )
        db.session.add(noticia)
        db.session.commit()
        flash('Noticia guardada correctamente.', 'success')
        return redirect(url_for('noticias.detalle', id=noticia.id))
    return render_template('noticias/form.html')

@noticias.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    noticia = Noticia.query.get_or_404(id)
    if current_user.rol not in ['Administrador', 'Redactor']:
        abort(403)
    if request.method == 'POST':
        noticia.titulo = request.form.get('titulo', '').strip()
        noticia.cuerpo = request.form.get('cuerpo', '').strip()
        noticia.imagen = request.form.get('imagen', '').strip() or None
        noticia.etiquetas = request.form.get('etiquetas', '').strip() or None
        noticia.estado = request.form.get('estado', 'borrador')
        fecha_prog = request.form.get('fecha_programada', '')
        noticia.fecha_programada = datetime.strptime(fecha_prog, '%Y-%m-%dT%H:%M') if fecha_prog else None
        db.session.commit()
        flash('Noticia actualizada correctamente.', 'success')
        return redirect(url_for('noticias.detalle', id=noticia.id))
    return render_template('noticias/form.html', noticia=noticia)

@noticias.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    if current_user.rol != 'Administrador':
        abort(403)
    noticia = Noticia.query.get_or_404(id)
    db.session.delete(noticia)
    db.session.commit()
    flash('Noticia eliminada.', 'info')
    return redirect(url_for('noticias.lista'))