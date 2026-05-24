from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Videojuego

videojuegos = Blueprint('videojuegos', __name__, url_prefix='/videojuegos')

@videojuegos.route('/')
def lista():
    page = request.args.get('page', 1, type=int)
    genero = request.args.get('genero', '')
    query = Videojuego.query
    if genero:
        query = query.filter(Videojuego.genero.ilike(f'%{genero}%'))
    lista_juegos = query.order_by(Videojuego.nota_comunidad.desc()).paginate(page=page, per_page=12)
    return render_template('videojuegos/lista.html', videojuegos=lista_juegos, genero=genero)

@videojuegos.route('/<int:id>')
def detalle(id):
    videojuego = Videojuego.query.get_or_404(id)
    return render_template('videojuegos/detalle.html', videojuego=videojuego)

@videojuegos.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if current_user.rol not in ['Administrador', 'Redactor']:
        abort(403)
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        if not nombre:
            flash('El nombre es obligatorio.', 'danger')
            return render_template('videojuegos/form.html')
        if Videojuego.query.filter_by(nombre=nombre).first():
            flash('Ya existe un videojuego con ese nombre.', 'danger')
            return render_template('videojuegos/form.html')
        videojuego = Videojuego(
            nombre=nombre,
            imagen=request.form.get('imagen', '').strip() or None,
            descripcion=request.form.get('descripcion', '').strip() or None,
            nota_prensa=request.form.get('nota_prensa') or None,
            nota_comunidad=request.form.get('nota_comunidad') or None,
            anio_lanzamiento=request.form.get('anio_lanzamiento') or None,
            genero=request.form.get('genero', '').strip() or None,
            autor_id=current_user.id
        )
        db.session.add(videojuego)
        db.session.commit()
        flash('Videojuego añadido correctamente.', 'success')
        return redirect(url_for('videojuegos.detalle', id=videojuego.id))
    return render_template('videojuegos/form.html')

@videojuegos.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    videojuego = Videojuego.query.get_or_404(id)
    if current_user.rol not in ['Administrador', 'Redactor']:
        abort(403)
    if request.method == 'POST':
        videojuego.nombre = request.form.get('nombre', '').strip()
        videojuego.imagen = request.form.get('imagen', '').strip() or None
        videojuego.descripcion = request.form.get('descripcion', '').strip() or None
        videojuego.nota_prensa = request.form.get('nota_prensa') or None
        videojuego.nota_comunidad = request.form.get('nota_comunidad') or None
        videojuego.anio_lanzamiento = request.form.get('anio_lanzamiento') or None
        videojuego.genero = request.form.get('genero', '').strip() or None
        db.session.commit()
        flash('Videojuego actualizado correctamente.', 'success')
        return redirect(url_for('videojuegos.detalle', id=videojuego.id))
    return render_template('videojuegos/form.html', videojuego=videojuego)

@videojuegos.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    if current_user.rol != 'Administrador':
        abort(403)
    videojuego = Videojuego.query.get_or_404(id)
    db.session.delete(videojuego)
    db.session.commit()
    flash('Videojuego eliminado.', 'info')
    return redirect(url_for('videojuegos.lista'))