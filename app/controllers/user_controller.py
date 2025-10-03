# project_name/routes/user_routes.py
from flask import Blueprint, request, render_template, redirect, session, flash
# Importamos la instancia de bcrypt que ya fue inicializada y vinculada a la app en __init__.py
from app import bcrypt

from app.models.user import User # Importación relativa desde el paquete principal

# Crea una instancia de Blueprint para las rutas de usuarios
users_bp = Blueprint('users', __name__)

@users_bp.route('/registro')
def show_registro_form():
    return render_template('registro.html')

@users_bp.route('/registro', methods=['POST'])
def registro():
    # Validaciones
    if not request.form['nombre'] or not request.form['email'] or \
       not request.form['password'] or not request.form['confirm_password']:
        flash('Todos los campos son obligatorios.', 'error')
        return redirect('/registro')

    if '@' not in request.form['email']:
        flash('Formato de correo electrónico inválido.', 'error')
        return redirect('/registro')

    if len(request.form['password']) < 8:
        flash('La contraseña debe tener al menos 8 caracteres.', 'error')
        return redirect('/registro')

    if request.form['password'] != request.form['confirm_password']:
        flash('Las contraseñas no coinciden.', 'error')
        return redirect('/registro')

    user_in_db = User.get_by_email({'email': request.form['email']})
    if user_in_db:
        flash('El correo electrónico ya está registrado.', 'error')
        return redirect('/registro')

    hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

    data = {
        'nombre': request.form['nombre'],
        'email': request.form['email '],
        'password': hashed_password
    }
    user_id = User.create(data)

    if user_id:
        session['user_id'] = user_id
        session['user_name'] = request.form['nombre']
        flash('¡Registro exitoso! Bienvenido.', 'success')
        return redirect('/dashboard')
    else:
        flash('Hubo un problema al registrar el usuario.', 'error')
        return redirect('/registro')

@users_bp.route('/login')
def show_login_form():
    return render_template('login.html')

@users_bp.route('/login', methods=['POST'])
def login():
    if not request.form['email'] or not request.form['password']:
        flash('Ambos campos son obligatorios.', 'error')
        return redirect('/login')

    user_in_db = User.get_by_email({'email': request.form['email']})

    if not user_in_db:
        flash('Credenciales inválidas.', 'error')
        return redirect('/login')

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Credenciales inválidas.', 'error')
        return redirect('/login')

    session['user_id'] = user_in_db.id
    session['user_name'] = user_in_db.nombre
    flash(f'¡Bienvenido de nuevo, {user_in_db.nombre}!', 'success')
    return redirect('/dashboard')

@users_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder al dashboard.', 'error')
        return redirect('/login')
    return render_template('dashboard.html', user_name=session['user_name'])

@users_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect('/login')