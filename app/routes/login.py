from flask import Blueprint, render_template, request, redirect, session, url_for, flash, current_app
from models.models_flask import Credentials
from utils.db import db
import bcrypt
from datetime import datetime, timedelta
import uuid


login = Blueprint('login', __name__)

@login.route('/', methods=['GET'])
def index():
    """Default login page"""
    return render_template('login.html')

@login.route('/login', methods=['GET', 'POST'])
def new_login():
    if request.method == 'POST':
        cedula = request.form['cedula']
        password = request.form['password']

        credential = Credentials.query.filter_by(identifierCode=cedula).first()

        if credential and bcrypt.checkpw(password.encode('utf-8'), credential.password.encode('utf-8')):
            session['autenticado'] = True
            session['cedula'] = cedula
            return redirect(url_for('clinic.home'))
        else:
            flash('Credenciales inválidas', 'danger')
            return redirect(url_for('login.new_login'))

    return render_template('login.html')

@login.route('/logout', methods=['POST', 'GET'])
def logout():
    """Logout route to clear session and redirect to login"""
    try:
        # Clear all session data
        session.clear()
        flash('Sesión cerrada exitosamente', 'success')
        
        # Log the logout action using current_app
        current_app.logger.info("User logged out successfully")
        
    except Exception as e:
        current_app.logger.error(f"Error during logout: {str(e)}")
        flash('Error al cerrar sesión', 'error')
    
    return redirect(url_for('login.index'))




reset_tokens = {}


@login.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        cedula = request.form.get('cedula')
        user = Credentials.query.filter_by(identifierCode=cedula).first()

        if user:
            token = str(uuid.uuid4())
            reset_tokens[token] = {
                'cedula': cedula,
                'exp': datetime.utcnow() + timedelta(hours=1)
            }

            reset_url = url_for('login.reset_password', token=token, _external=True)
            flash(f'Enlace para restablecer la contraseña: <a href="{reset_url}">{reset_url}</a>', 'info')

        else:
            flash('Usuario no encontrado', 'warning')

    return render_template('forgot_password.html')

@login.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    data = reset_tokens.get(token)

    if not data or data['exp'] < datetime.utcnow():
        flash('Token inválido o expirado', 'danger')
        return redirect(url_for('login.forgot_password'))

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        user = Credentials.query.filter_by(identifierCode=data['cedula']).first()

        if user:
            hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user.password = hashed_pw
            db.session.commit()

            # Elimina el token una vez usado
            reset_tokens.pop(token, None)

            flash('Contraseña actualizada exitosamente', 'success')
            return redirect(url_for('login.index'))
        else:
            flash('Usuario no encontrado', 'danger')

    return render_template('reset_password.html')



