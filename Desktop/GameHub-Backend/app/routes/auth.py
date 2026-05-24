from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import Usuario
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirmar = request.form.get('confirmar', '')
        if not nombre or not email or not password:
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('auth/registro.html')
        if password != confirmar:
            flash('Las contraseñas no coinciden.', 'danger')
            return render_template('auth/registro.html')
        if Usuario.query.filter_by(email=email).first():
            flash('Ya existe una cuenta con ese email.', 'danger')
            return render_template('auth/registro.html')
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        usuario = Usuario(nombre=nombre, email=email, password_hash=password_hash)
        db.session.add(usuario)
        db.session.commit()
        flash('Cuenta creada correctamente. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/registro.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario or not bcrypt.check_password_hash(usuario.password_hash, password):
            flash('Email o contraseña incorrectos.', 'danger')
            return render_template('auth/login.html')
        if not usuario.activo:
            flash('Tu cuenta está suspendida. Contacta con el administrador.', 'danger')
            return render_template('auth/login.html')
        login_user(usuario)
        usuario.ultimo_acceso = datetime.utcnow()
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        idioma = request.form.get('idioma', 'es')
        if nombre:
            current_user.nombre = nombre
        if idioma in ['es', 'en']:
            current_user.idioma = idioma
        password_nuevo = request.form.get('password_nuevo', '')
        confirmar = request.form.get('confirmar', '')
        if password_nuevo:
            if password_nuevo != confirmar:
                flash('Las contraseñas nuevas no coinciden.', 'danger')
                return render_template('auth/perfil.html')
            current_user.password_hash = bcrypt.generate_password_hash(password_nuevo).decode('utf-8')
        db.session.commit()
        flash('Perfil actualizado correctamente.', 'success')
        return redirect(url_for('auth.perfil'))
    return render_template('auth/perfil.html')