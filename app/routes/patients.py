from flask import Blueprint, render_template, session, request, redirect, url_for
from models.models_flask import Patient, Allergy
from utils.db import db

patients = Blueprint('patients', __name__)
allergies = []
familyBack = []
preExistingConditions = []

@patients.route('/patients')
def show_patients():
    return "desde patients"

@patients.route('/add-patients', methods=['POST'])
def add_patients():
    sessionID = session['cedula']
    # print("ESTOY EN ADD PATIENTS")

    if request.method == 'POST':
        # print(f" Estoy dentro de POST")
    
        new_patient = Patient(
            identifierType = request.form.get('identifierType'),
            identifierCode = request.form.get('identifierCode'),
            firstName = request.form.get('firstName'),
            middleName = request.form.get('middleName'),
            lastName1 = request.form.get('lastName1'),
            lastName2 = request.form.get('lastName2'),
            nationality = request.form.get('nationality'),
            address = request.form.get('address'),
            phoneNumber = request.form.get('phoneNumber'),
            birthdate = request.form.get('birthdate'),
            gender = request.form.get('gender'),
            sex = request.form.get('sex'),
            civilStatus = request.form.get('civilStatus'),
            job = request.form.get('job'),
            bloodType = request.form.get('bloodType'),
            email = request.form.get('email'),
            created_by = sessionID,
            updated_by = sessionID 
        )

        # print(f"Nuevo paciente recibido: {new_patient}")

        db.session.add(new_patient)
        db.session.commit()    

    return "paciente agregado"

@patients.route('/add-allergies', methods=['GET', 'POST'])
def add_allergies():
    if request.method == 'POST':
        new_allergy = request.form.get('allergy')
        if new_allergy:
            # print(f"Nuevo item recibido: {new_item}")
            allergies.append(new_allergy)
        # return redirect(url_for('clinic.home',  view='addPatient', sec_view="addPatientInfo", items=items))  # Redirige para evitar reenvío al recargar
    return render_template('home.html', view='addPatient', sec_view="addPatientInfo", allergies=allergies)


    # Agregar funcion para eliminar alergias

    # Agregar funcion para agrgar antecedentes familiares (family background)
@patients.route('/add-familyBack', methods=['GET', 'POST'])
def add_familyBack():
    if request.method == 'POST':
        background = request.form.get('familyBackground')
        print(f"Nuevo item recibido: {background}")
        if background:
            print(f"Nuevo item recibido: {background}")
            familyBack.append(background)
        # return redirect(url_for('clinic.home',  view='addPatient', sec_view="addPatientInfo", items=items))  # Redirige para evitar reenvío al recargar
        return render_template('home.html', view='addPatient', sec_view="addPatientInfo", familyBack=familyBack)

    # Agregar funcion para eliminar antecedentes familiares (family background)

    # Agregar funcion para agregar condiciones prexistentes
@patients.route('/add-conditions', methods=['GET', 'POST'])
def add_conditions():
    if request.method == 'POST':
        condition = request.form.get('diseaseName')
        print(f"Nuevo item recibido: {condition}")
        if condition:
            print(f"Nuevo item recibido: {condition}")
            preExistingConditions.append(condition)
        # return redirect(url_for('clinic.home',  view='addPatient', sec_view="addPatientInfo", items=items))  # Redirige para evitar reenvío al recargar
        return render_template('home.html', view='addPatient', sec_view="addPatientInfo", preExistingConditions=preExistingConditions)

    # Agregar funcion para eliminar condiciones prexistentes
    