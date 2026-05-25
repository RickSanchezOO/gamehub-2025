from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Evento

eventos = Blueprint('eventos', __name__, url_prefix='/eventos')

@eventos.route('/')
def lista():
    page = request.args.get('page', 1, type=int)
    lista_eventos = Evento.query.order_by(Evento.fecha_evento.asc()).paginate(page=page, per_page=10)
    return render_template('eventos/lista.html', eventos=lista_eventos)

@eventos.route('/<int:id>')
def detalle(id):
    evento = Evento.query.get_or_404(id)
    return render_template('eventos/detalle.html', evento=evento)

@eventos.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if current_user.rol not in ['Administrador', 'Redactor']:
        abort(403)
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        fecha_evento = request.form.get('fecha_evento', '').strip()
        if not nombre or not fecha_evento:
            flash('El nombre y la fecha son obligatorios.', 'danger')
            return render_template('eventos/form.html')
        evento = Evento(
            nombre=nombre,
            descripcion=request.form.get('descripcion', '').strip() or None,
            fecha_evento=fecha_evento,
            lugar=request.form.get('lugar', '').strip() or None,
            autor_id=current_user.id
        )
        db.session.add(evento)
        db.session.commit()
        flash('Evento creado correctamente.', 'success')
        return redirect(url_for('eventos.detalle', id=evento.id))
    return render_template('eventos/form.html')

@eventos.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    evento = Evento.query.get_or_404(id)
    if current_user.rol not in ['Administrador', 'Redactor']:
        abort(403)
    if request.method == 'POST':
        evento.nombre = request.form.get('nombre', '').strip()
        evento.descripcion = request.form.get('descripcion', '').strip() or None
        evento.fecha_evento = request.form.get('fecha_evento', '').strip()
        evento.lugar = request.form.get('lugar', '').strip() or None
        db.session.commit()
        flash('Evento actualizado correctamente.', 'success')
        return redirect(url_for('eventos.detalle', id=evento.id))
    return render_template('eventos/form.html', evento=evento)

@eventos.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    if current_user.rol != 'Administrador':
        abort(403)
    evento = Evento.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    flash('Evento eliminado.', 'info')
    return redirect(url_for('eventos.lista'))