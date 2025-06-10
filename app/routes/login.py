from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from models.models_flask import Credentials
from utils.db import db
import bcrypt

login = Blueprint('login', __name__)

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


