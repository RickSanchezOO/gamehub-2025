from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import PostBlog, Comentario

blog = Blueprint('blog', __name__, url_prefix='/blog')

@blog.route('/')
def lista():
    page = request.args.get('page', 1, type=int)
    posts = PostBlog.query.order_by(PostBlog.fecha_publicacion.desc()).paginate(page=page, per_page=10)
    return render_template('blog/lista.html', posts=posts)

@blog.route('/<int:id>')
def detalle(id):
    post = PostBlog.query.get_or_404(id)
    return render_template('blog/detalle.html', post=post)

@blog.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if current_user.rol not in ['Administrador', 'Redactor', 'Colaborador']:
        abort(403)
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        contenido = request.form.get('contenido', '').strip()
        imagen = request.form.get('imagen', '').strip()
        comentarios_activos = request.form.get('comentarios_activos') == 'on'
        if not titulo or not contenido:
            flash('El título y el contenido son obligatorios.', 'danger')
            return render_template('blog/form.html')
        post = PostBlog(
            titulo=titulo, contenido=contenido,
            imagen=imagen or None,
            comentarios_activos=comentarios_activos,
            autor_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash('Post publicado correctamente.', 'success')
        return redirect(url_for('blog.detalle', id=post.id))
    return render_template('blog/form.html')

@blog.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    post = PostBlog.query.get_or_404(id)
    if current_user.rol not in ['Administrador', 'Redactor'] and post.autor_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        post.titulo = request.form.get('titulo', '').strip()
        post.contenido = request.form.get('contenido', '').strip()
        post.imagen = request.form.get('imagen', '').strip() or None
        post.comentarios_activos = request.form.get('comentarios_activos') == 'on'
        db.session.commit()
        flash('Post actualizado correctamente.', 'success')
        return redirect(url_for('blog.detalle', id=post.id))
    return render_template('blog/form.html', post=post)

@blog.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    if current_user.rol != 'Administrador':
        abort(403)
    post = PostBlog.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Post eliminado.', 'info')
    return redirect(url_for('blog.lista'))

@blog.route('/comentario/<int:post_id>', methods=['POST'])
@login_required
def comentar(post_id):
    post = PostBlog.query.get_or_404(post_id)
    if not post.comentarios_activos:
        flash('Los comentarios están desactivados en este post.', 'warning')
        return redirect(url_for('blog.detalle', id=post_id))
    contenido = request.form.get('contenido', '').strip()
    if not contenido:
        flash('El comentario no puede estar vacío.', 'danger')
        return redirect(url_for('blog.detalle', id=post_id))
    comentario = Comentario(contenido=contenido, post_id=post_id, usuario_id=current_user.id)
    db.session.add(comentario)
    db.session.commit()
    flash('Comentario añadido.', 'success')
    return redirect(url_for('blog.detalle', id=post_id))

@blog.route('/comentario/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_comentario(id):
    comentario = Comentario.query.get_or_404(id)
    if current_user.rol != 'Administrador' and comentario.usuario_id != current_user.id:
        abort(403)
    comentario.eliminado = True
    db.session.commit()
    flash('Comentario eliminado.', 'info')
    return redirect(url_for('blog.detalle', id=comentario.post_id))