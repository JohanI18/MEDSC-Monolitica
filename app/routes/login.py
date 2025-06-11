from flask import Blueprint, render_template, request, redirect, session, url_for, flash, current_app
from models.models_flask import Credentials
from utils.db import db
import bcrypt

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


