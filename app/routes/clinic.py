from flask import Blueprint, render_template, session, request, redirect, url_for
from models.models_flask import Patient
from utils.db import db

clinic = Blueprint('clinic', __name__)

@clinic.route('/')
def index():
    session['autenticado'] = False
    return render_template('login.html')

@clinic.route('/home', methods=['GET', 'POST'])
def home():
    view = request.args.get('view', 'home')

    if not session.get('autenticado'):
        return redirect(url_for('clinic.index'))


    if view == 'home':
        patients = Patient.query.all()
        return render_template('home.html', view=view, patients=patients)
    elif view == 'addPatient':
        sec_view = request.args.get("sec_view", "addPatient")
        if sec_view == 'addPatient':
            return render_template('home.html', view=view, sec_view=sec_view)
        elif sec_view == 'addPatientInfo':
            return render_template('home.html', view=view, sec_view=sec_view)            
    elif view == 'addAttention':
        return render_template('home.html', view=view)
    # return redirect(url_for('clinic.home'))
    return render_template('home.html')