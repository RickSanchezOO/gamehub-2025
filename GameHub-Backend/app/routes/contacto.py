from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Contacto

contacto = Blueprint('contacto', __name__, url_prefix='/contacto')

@contacto.route('/', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        mensaje = request.form.get('mensaje', '').strip()
        if not nombre or not email or not mensaje:
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('contacto/formulario.html')
        mensaje_contacto = Contacto(
            nombre=nombre,
            email=email,
            mensaje=mensaje,
            usuario_id=current_user.id if current_user.is_authenticated else None
        )
        db.session.add(mensaje_contacto)
        db.session.commit()
        flash('Mensaje enviado correctamente. Nos pondremos en contacto contigo pronto.', 'success')
        return redirect(url_for('contacto.formulario'))
    return render_template('contacto/formulario.html')

@contacto.route('/mensajes')
@login_required
def mensajes():
    if current_user.rol != 'Administrador':
        abort(403)
    page = request.args.get('page', 1, type=int)
    solo_no_leidos = request.args.get('no_leidos', False)
    query = Contacto.query
    if solo_no_leidos:
        query = query.filter_by(leido=False)
    lista = query.order_by(Contacto.fecha_envio.desc()).paginate(page=page, per_page=20)
    return render_template('contacto/mensajes.html', mensajes=lista)

@contacto.route('/mensajes/<int:id>/leido', methods=['POST'])
@login_required
def marcar_leido(id):
    if current_user.rol != 'Administrador':
        abort(403)
    mensaje = Contacto.query.get_or_404(id)
    mensaje.leido = True
    db.session.commit()
    return redirect(url_for('contacto.mensajes'))

@contacto.route('/mensajes/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    if current_user.rol != 'Administrador':
        abort(403)
    mensaje = Contacto.query.get_or_404(id)
    db.session.delete(mensaje)
    db.session.commit()
    flash('Mensaje eliminado.', 'info')
    return redirect(url_for('contacto.mensajes'))