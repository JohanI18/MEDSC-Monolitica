from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from models.models_flask import Credentials
from utils.db import db
import bcrypt

login = Blueprint('login', __name__)

@login.route('/login', methods=['GET','POST'])
def new_login():
    credential = Credentials.query.get(1)
    # credential = session.get('Credentials', 1)

    cedula = request.form['cedula']
    password = request.form['password']

    if cedula == credential.identifierCode and bcrypt.checkpw(password.encode('utf-8'), credential.password.encode('utf-8')):
        session['autenticado'] = True
        return redirect(url_for('clinic.home'))
    else:
        flash('Invalid credentials')
        

    db.session.commit()

    # return render_template('login.html', error='Invalid credentials')
    return redirect(url_for('clinic.index'))

