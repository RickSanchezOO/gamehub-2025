from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Multimedia

multimedia = Blueprint('multimedia', __name__, url_prefix='/multimedia')

@multimedia.route('/')
def lista():
    page = request.args.get('page', 1, type=int)
    tipo = request.args.get('tipo', '')
    query = Multimedia.query
    if tipo:
        query = query.filter_by(tipo=tipo)
    lista_multimedia = query.order_by(Multimedia.fecha_alta.desc()).paginate(page=page, per_page=12)
    return render_template('multimedia/lista.html', multimedia=lista_multimedia, tipo=tipo)

@multimedia.route('/<int:id>')
def detalle(id):
    item = Multimedia.query.get_or_404(id)
    return render_template('multimedia/detalle.html', item=item)

@multimedia.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if current_user.rol not in ['Administrador', 'Redactor']:
        abort(403)
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        url_video = request.form.get('url_video', '').strip()
        if not titulo or not url_video:
            flash('El título y la URL del vídeo son obligatorios.', 'danger')
            return render_template('multimedia/form.html')
        item = Multimedia(
            titulo=titulo,
            url_video=url_video,
            tipo=request.form.get('tipo', 'otro'),
            autor_id=current_user.id
        )
        db.session.add(item)
        db.session.commit()
        flash('Vídeo añadido correctamente.', 'success')
        return redirect(url_for('multimedia.detalle', id=item.id))
    return render_template('multimedia/form.html')

@multimedia.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    item = Multimedia.query.get_or_404(id)
    if current_user.rol not in ['Administrador', 'Redactor']:
        abort(403)
    if request.method == 'POST':
        item.titulo = request.form.get('titulo', '').strip()
        item.url_video = request.form.get('url_video', '').strip()
        item.tipo = request.form.get('tipo', 'otro')
        db.session.commit()
        flash('Vídeo actualizado correctamente.', 'success')
        return redirect(url_for('multimedia.detalle', id=item.id))
    return render_template('multimedia/form.html', item=item)

@multimedia.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    if current_user.rol != 'Administrador':
        abort(403)
    item = Multimedia.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Vídeo eliminado.', 'info')
    return redirect(url_for('multimedia.lista'))