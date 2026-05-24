from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Usuario, Noticia, PostBlog, Videojuego, Multimedia, Evento, Contacto

admin = Blueprint('admin', __name__, url_prefix='/admin')

def solo_admin():
    if not current_user.is_authenticated or current_user.rol != 'Administrador':
        abort(403)

@admin.route('/')
@login_required
def panel():
    solo_admin()
    total_usuarios = Usuario.query.count()
    total_noticias = Noticia.query.count()
    total_posts = PostBlog.query.count()
    total_videojuegos = Videojuego.query.count()
    total_eventos = Evento.query.count()
    mensajes_no_leidos = Contacto.query.filter_by(leido=False).count()
    return render_template('admin/panel.html',
        total_usuarios=total_usuarios,
        total_noticias=total_noticias,
        total_posts=total_posts,
        total_videojuegos=total_videojuegos,
        total_eventos=total_eventos,
        mensajes_no_leidos=mensajes_no_leidos
    )

@admin.route('/usuarios')
@login_required
def usuarios():
    solo_admin()
    page = request.args.get('page', 1, type=int)
    lista = Usuario.query.order_by(Usuario.fecha_registro.desc()).paginate(page=page, per_page=20)
    return render_template('admin/usuarios.html', usuarios=lista)

@admin.route('/usuarios/<int:id>/rol', methods=['POST'])
@login_required
def cambiar_rol(id):
    solo_admin()
    usuario = Usuario.query.get_or_404(id)
    nuevo_rol = request.form.get('rol')
    if nuevo_rol in ['Administrador', 'Redactor', 'Colaborador', 'Suscriptor']:
        usuario.rol = nuevo_rol
        db.session.commit()
        flash(f'Rol de {usuario.nombre} actualizado a {nuevo_rol}.', 'success')
    else:
        flash('Rol no válido.', 'danger')
    return redirect(url_for('admin.usuarios'))

@admin.route('/usuarios/<int:id>/suspender', methods=['POST'])
@login_required
def suspender_usuario(id):
    solo_admin()
    usuario = Usuario.query.get_or_404(id)
    if usuario.id == current_user.id:
        flash('No puedes suspenderte a ti mismo.', 'danger')
        return redirect(url_for('admin.usuarios'))
    usuario.activo = not usuario.activo
    db.session.commit()
    estado = 'activado' if usuario.activo else 'suspendido'
    flash(f'Usuario {usuario.nombre} {estado}.', 'info')
    return redirect(url_for('admin.usuarios'))

@admin.route('/usuarios/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_usuario(id):
    solo_admin()
    usuario = Usuario.query.get_or_404(id)
    if usuario.id == current_user.id:
        flash('No puedes eliminarte a ti mismo.', 'danger')
        return redirect(url_for('admin.usuarios'))
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado.', 'info')
    return redirect(url_for('admin.usuarios'))