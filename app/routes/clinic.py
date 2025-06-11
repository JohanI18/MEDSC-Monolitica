from flask import Blueprint, render_template, session, request, redirect, url_for
from models.models_flask import Patient, Doctor
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

    # Get doctor information from session
    doctor_info = None
    if 'cedula' in session:
        try:
            doctor = Doctor.query.filter_by(
                identifierCode=session['cedula'], 
                is_deleted=False
            ).first()
            if doctor:
                doctor_info = {
                    'firstName': doctor.firstName,
                    'lastName1': doctor.lastName1,
                    'speciality': doctor.speciality
                }
        except Exception as e:
            print(f"Error fetching doctor info: {str(e)}")
            doctor_info = None

    if view == 'home':
        patients = Patient.query.all()
        sessionID = session['cedula']
        return render_template('home.html', view=view, patients=patients, doctor_info=doctor_info)
    elif view == 'addPatient':
        sec_view = request.args.get("sec_view", "addPatient")
        if sec_view == 'addPatient':
            return render_template('home.html', view=view, sec_view=sec_view, doctor_info=doctor_info)
        elif sec_view == 'addPatientInfo':
            return render_template('home.html', view=view, sec_view=sec_view, doctor_info=doctor_info)            
    elif view == 'addAttention':
        # Import here to avoid circular imports
        from routes.attention import (
            vital_signs_data, evaluation_data, physical_exams, organ_system_reviews,
            diagnostics, treatments, histopathologies, imagings, laboratories, selected_patient_id
        )
        
        # Only clear attention data when first entering (not when patient is already selected)
        if selected_patient_id is None:
            from routes.attention import _clear_temp_attention_data
            _clear_temp_attention_data()
        
        # Get available patients and selected patient info
        available_patients = Patient.query.filter_by(is_deleted=False).all()
        selected_patient = None
        if selected_patient_id:
            selected_patient = Patient.query.filter_by(id=selected_patient_id, is_deleted=False).first()
        
        # Get current step for navigation
        current_step = request.args.get('step', 'vitales')
        
        return render_template('home.html', view=view,
                             vital_signs_data=vital_signs_data,
                             evaluation_data=evaluation_data,
                             physicalExams=physical_exams,
                             organSystemReviews=organ_system_reviews,
                             diagnostics=diagnostics,
                             treatments=treatments,
                             histopathologies=histopathologies,
                             imagings=imagings,
                             laboratories=laboratories,
                             available_patients=available_patients,
                             selected_patient=selected_patient,
                             selected_patient_id=selected_patient_id,
                             current_step=current_step,
                             doctor_info=doctor_info)
    
    return render_template('home.html', doctor_info=doctor_info)