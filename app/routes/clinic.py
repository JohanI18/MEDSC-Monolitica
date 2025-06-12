from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from models.models_flask import Patient, Doctor, Attention
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
            # Obtener el modo edición desde los argumentos GET o sesión
            edit_mode = request.args.get('edit_mode', 'false') == 'true'
            patient_id = request.args.get('current_patient_id') or session.get('current_patient_id')


            if not patient_id:
                flash("Error: No hay paciente activo para agregar información adicional.", "error")
                return redirect(url_for('clinic.home', view='addPatient'))

            patient = Patient.query.get(patient_id)
            if not patient:
                flash("Error: El paciente no existe.", "error")
                return redirect(url_for('clinic.home', view='addPatient'))

            # Guardar en sesión por consistencia
            session['current_patient_id'] = patient.id
            session['edit_mode'] = edit_mode

            # Obtener relaciones (o listas vacías por seguridad)
            allergies = patient.allergies if patient.allergies else []
            emergencyContacts = patient.emergency_contacts if patient.emergency_contacts else []
            familyBack = patient.family_backgrounds if patient.family_backgrounds else []
            preExistingConditions = patient.pre_existing_conditions if patient.pre_existing_conditions else []

            return render_template(
                'home.html',
                view=view,
                sec_view=sec_view,
                doctor_info=doctor_info,
                edit_mode=edit_mode,
                patient=patient,
                current_patient_id=patient.id
            )

            # Obtener datos desde GET
            edit_mode = request.args.get('edit_mode', 'false') == 'true'
            patient_id = request.args.get('current_patient_id') or session.get('current_patient_id')

            if not patient_id:
                flash("Error: No hay paciente activo para agregar información adicional.", "error")
                return redirect(url_for('clinic.home', view='addPatient'))

            patient = Patient.query.get(patient_id)
            if not patient:
                flash("Error: El paciente no existe.", "error")
                return redirect(url_for('clinic.home', view='addPatient'))

            # Guardar en sesión por si se necesita en otros pasos
            session['current_patient_id'] = patient.id
            session['edit_mode'] = edit_mode

            # Obtener datos relacionados
            allergies = patient.allergies or []
            emergencyContacts = patient.emergency_contacts or []
            familyBack = patient.family_backgrounds or []
            preExistingConditions = patient.pre_existing_conditions or []

            return render_template(
                'home.html',
                view=view,
                sec_view=sec_view,
                doctor_info=doctor_info,
                edit_mode=edit_mode,
                patient=patient,
                current_patient_id=patient.id,
                allergies=allergies,
                emergencyContacts=emergencyContacts,
                familyBack=familyBack,
                preExistingConditions=preExistingConditions
            )

            edit_mode = session.get('edit_mode', False)
            patient = None
            if session.get('current_patient_id'):
                patient = Patient.query.get(session['current_patient_id'])
            return render_template(
                'home.html',
                view=view,
                sec_view=sec_view,
                doctor_info=doctor_info,
                edit_mode=edit_mode,
                patient=patient,
                current_patient_id=session.get('current_patient_id')
            )
            
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
    
        edit_mode = session.get('edit_mode', False)
        return render_template(
        'home.html',
        view=view,
        sec_view=sec_view,
        doctor_info=doctor_info,
        edit_mode=edit_mode,
        patient=patient,
        current_patient_id=patient.id,
        allergies=allergies,
        emergencyContacts=emergencyContacts,
        familyBack=familyBack,
        preExistingConditions=preExistingConditions
)

    elif view == 'attentionHistory':
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
        attentions = []
        if selected_patient_id:
            selected_patient = Patient.query.filter_by(id=selected_patient_id, is_deleted=False).first()
            if selected_patient:
                attentions = (
                    Attention.query
                    .filter_by(idPatient=selected_patient.id)
                    .order_by(Attention.date.desc())
                    .all()
                )
                # Attach doctor name to each attention
                for att in attentions:
                    doctor = Doctor.query.filter_by(id=att.idDoctor, is_deleted=False).first()
                    att.doctor_name = f"Dr. {doctor.firstName} {doctor.lastName1}" if doctor else "-"
                
                # Batch doctor lookup for all attentions
                doctor_ids = list(set(att.idDoctor for att in attentions if att.idDoctor))
                doctor_map = {}
                if doctor_ids:
                    doctors = Doctor.query.filter(Doctor.id.in_(doctor_ids), Doctor.is_deleted == False).all()
                    doctor_map = {doc.id: f"Dr. {doc.firstName} {doc.lastName1}" for doc in doctors}
                for att in attentions:
                    att.doctor_name = doctor_map.get(att.idDoctor, "-")
        
        # Get selected attention detail if requested
        selected_attention = None
        selected_attention_patient = None
        selected_attention_doctor = None
        selected_attention_id = request.args.get('selected_attention_id')
        if selected_attention_id:
            selected_attention = Attention.query.filter_by(id=selected_attention_id).first()
            if selected_attention:
                selected_attention_patient = Patient.query.filter_by(id=selected_attention.idPatient, is_deleted=False).first()
                selected_attention_doctor = Doctor.query.filter_by(id=selected_attention.idDoctor, is_deleted=False).first()
        
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
                             attentions=attentions,
                             current_step=current_step,
                             doctor_info=doctor_info,
                             selected_attention=selected_attention,
                             patient=selected_attention_patient,
                             doctor=selected_attention_doctor)
    
    return render_template('home.html', doctor_info=doctor_info)