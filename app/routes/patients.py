from flask import Blueprint, render_template, session, request, redirect, url_for, flash, jsonify
from models.models_flask import Patient, Allergy, FamilyBackground, PreExistingCondition, EmergencyContact
from utils.db import db
from sqlalchemy.exc import IntegrityError
import logging

patients = Blueprint('patients', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global lists for temporary storage (consider using session storage instead)
allergies = []
familyBack = []
preExistingConditions = []
emergencyContacts = []  # Add missing emergency contacts list
current_patient_id = None  # Add this to track the current patient being processed

@patients.route('/patients')
def show_patients():
    """Display all patients with proper error handling"""
    try:
        all_patients = Patient.query.filter_by(is_deleted=False).all()
        return render_template('patients_list.html', patients=all_patients)
    except Exception as e:
        logger.error(f"Error fetching patients: {str(e)}")
        flash('Error al cargar la lista de pacientes', 'error')
        return redirect(url_for('clinic.home'))


@patients.route('/editar-paciente/<int:patient_id>', methods=['GET', 'POST'])
def editar_paciente(patient_id):
    """
    Editar un paciente existente desde la misma interfaz de agregar
    y continuar con información adicional.
    """
    from models.models_flask import Doctor
    global current_patient_id  # 🔴 Importante para usar la variable global

    patient = Patient.query.get_or_404(patient_id)

    # Obtener doctor_info desde la sesión
    doctor_info = None
    if 'cedula' in session:
        doctor = Doctor.query.filter_by(identifierCode=session['cedula'], is_deleted=False).first()
        if doctor:
            doctor_info = {
                'firstName': doctor.firstName,
                'lastName1': doctor.lastName1,
                'speciality': doctor.speciality
            }

    if request.method == 'POST':
        try:
            # Actualizar los campos del paciente desde el formulario
            patient.identifierType = request.form.get('identifierType')
            patient.identifierCode = request.form.get('identifierCode')
            patient.firstName = request.form.get('firstName')
            patient.middleName = request.form.get('middleName')
            patient.lastName1 = request.form.get('lastName1')
            patient.lastName2 = request.form.get('lastName2')
            patient.nationality = request.form.get('nationality')
            patient.address = request.form.get('address')
            patient.phoneNumber = request.form.get('phoneNumber')
            patient.birthdate = request.form.get('birthdate')
            patient.gender = request.form.get('gender')
            patient.sex = request.form.get('sex')
            patient.civilStatus = request.form.get('civilStatus')
            patient.job = request.form.get('job')
            patient.bloodType = request.form.get('bloodType')
            patient.email = request.form.get('email')
            patient.updated_by = session.get('cedula')

            db.session.commit()

            # 🔴 Guardar en variable global y sesión
            current_patient_id = patient.id
            session['current_patient_id'] = patient.id
            session['edit_mode'] = True

            flash('Paciente actualizado exitosamente. Puede continuar con la información adicional.', 'success')
            return redirect(url_for(
                'clinic.home',
                view='addPatient',
                sec_view='addPatientInfo',
                edit_mode='true',
                current_patient_id=patient.id
            ))


        except Exception as e:
            db.session.rollback()
            logger.error(f"Error actualizando paciente: {str(e)}")
            flash('Error al actualizar el paciente', 'error')

    return render_template(
        'home.html',
        view='addPatient',
        sec_view='addPatient',
        patient=patient,
        edit_mode=True,
        doctor_info=doctor_info,
        current_patient_id=patient.id
    )






@patients.route('/historial-paciente/<int:patient_id>')
def patient_details(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    # Consulta los datos relacionados desde la base de datos
    allergies = Allergy.query.filter_by(idPatient=patient_id).all()
    contacts = EmergencyContact.query.filter_by(idPatient=patient_id).all()
    conditions = PreExistingCondition.query.filter_by(idPatient=patient_id).all()
    backgrounds = FamilyBackground.query.filter_by(idPatient=patient_id).all()

    return render_template(
        'partials/_patient_detail.html',
        patient=patient,
        allergies=allergies,
        contacts=contacts,
        conditions=conditions,
        backgrounds=backgrounds
    )

@patients.route('/add-patients', methods=['POST'])
def add_patients():
    """Add new patient and continue to additional info step"""
    global current_patient_id, allergies, familyBack, preExistingConditions, emergencyContacts
    
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    sessionID = session['cedula']
    
    if request.method == 'POST':
        try:
            # Validate required fields
            required_fields = ['identifierType', 'identifierCode', 'firstName', 'lastName1', 'address', 'birthdate']
            for field in required_fields:
                if not request.form.get(field):
                    flash(f'El campo {field} es requerido', 'error')
                    return redirect(url_for('clinic.home', view='addPatient', sec_view='addPatient'))
            
            # Check if patient already exists
            existing_patient = Patient.query.filter_by(
                identifierCode=request.form.get('identifierCode'),
                is_deleted=False
            ).first()
            
            if existing_patient:
                flash('Ya existe un paciente con este código de identificación', 'error')
                return redirect(url_for('clinic.home', view='addPatient', sec_view='addPatient'))
            
            # Create new patient
            new_patient = Patient(
                identifierType=request.form.get('identifierType'),
                identifierCode=request.form.get('identifierCode'),
                firstName=request.form.get('firstName'),
                middleName=request.form.get('middleName'),
                lastName1=request.form.get('lastName1'),
                lastName2=request.form.get('lastName2'),
                nationality=request.form.get('nationality'),
                address=request.form.get('address'),
                phoneNumber=request.form.get('phoneNumber'),
                birthdate=request.form.get('birthdate'),
                gender=request.form.get('gender'),
                sex=request.form.get('sex'),
                civilStatus=request.form.get('civilStatus'),
                job=request.form.get('job'),
                bloodType=request.form.get('bloodType'),
                email=request.form.get('email'),
                created_by=sessionID,
                updated_by=sessionID
            )

            db.session.add(new_patient)
            db.session.commit()
            
            # Store the ID of the newly created patient
            current_patient_id = new_patient.id
            
            # Clear any existing temporary data
            allergies.clear()
            familyBack.clear()
            preExistingConditions.clear()
            emergencyContacts.clear()
            
            logger.info(f"Patient created successfully: {new_patient.identifierCode} with ID: {new_patient.id}")
            flash(f'Datos básicos de {new_patient.firstName} {new_patient.lastName1} guardados. Ahora agregue información adicional.', 'success')
            
            # Redirect to additional info step
            return redirect(url_for('clinic.home', view='addPatient', sec_view='addPatientInfo'))

        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Integrity error creating patient: {str(e)}")
            flash('Error: Código de identificación ya existe', 'error')
            return redirect(url_for('clinic.home', view='addPatient', sec_view='addPatient'))
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating patient: {str(e)}")
            flash('Error al agregar paciente', 'error')
            return redirect(url_for('clinic.home', view='addPatient', sec_view='addPatient'))

# ALLERGIES ROUTES
@patients.route('/add-allergies', methods=['POST'])
def add_allergies():
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))

    patient_id = session.get('current_patient_id')
    if not patient_id:
        flash('Error: No hay paciente activo para agregar alergia', 'error')
        return redirect(url_for('clinic.home', view='addPatient', sec_view='addPatientInfo'))

    try:
        new_allergy = request.form.get('allergy')
        if not new_allergy or not new_allergy.strip():
            flash('Por favor ingrese una alergia válida', 'error')
        elif new_allergy.strip() not in allergies:
            allergies.append(new_allergy.strip())
            flash('Alergia agregada temporalmente', 'info')
        else:
            flash('Esta alergia ya existe', 'warning')

    except Exception as e:
        logger.error(f"Error adding allergy: {str(e)}")
        flash('Error al agregar alergia', 'error')

    return redirect(url_for('clinic.home', view='addPatient', sec_view='addPatientInfo'))

@patients.route('/remove-allergy', methods=['POST'])
def remove_allergy():
    """Remove allergy from temporary storage"""
    try:
        index = int(request.form.get('index', -1))
        if 0 <= index < len(allergies):
            removed_allergy = allergies.pop(index)
            flash(f'Alergia "{removed_allergy}" eliminada temporalmente', 'success')
        else:
            flash('Alergia no encontrada', 'error')
    except Exception as e:
        logger.error(f"Error removing allergy: {str(e)}")
        flash('Error al eliminar alergia', 'error')
    
    return render_template('home.html', view='addPatient', sec_view="addPatientInfo", 
                         allergies=allergies, emergencyContacts=emergencyContacts, 
                         familyBack=familyBack, preExistingConditions=preExistingConditions,
                         current_patient_id=current_patient_id)

# EMERGENCY CONTACT ROUTES
@patients.route('/add-contact', methods=['GET', 'POST'])
def add_contact():
    """Add emergency contact to temporary storage"""
    global current_patient_id, emergencyContacts
    
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    if request.method == 'POST':
        try:
            first_name = request.form.get('firstName')
            last_name = request.form.get('lastName')
            address = request.form.get('address')
            relationship = request.form.get('relationship')
            phone_number1 = request.form.get('phoneNumber1')
            phone_number2 = request.form.get('phoneNumber2')
            
            # Validate required fields
            if not all([first_name, last_name, address, relationship, phone_number1]):
                flash('Por favor complete todos los campos requeridos del contacto de emergencia', 'error')
                return redirect(url_for('clinic.home', view='addPatient', sec_view='addPatientInfo'))
            
            # Store temporarily - don't save to database yet
            if current_patient_id:
                contact_data = {
                    'firstName': first_name.strip(),
                    'lastName': last_name.strip(),
                    'address': address.strip(),
                    'relationship': relationship.strip(),
                    'phoneNumber1': phone_number1.strip(),
                    'phoneNumber2': phone_number2.strip() if phone_number2 else None
                }
                
                # Check if contact already exists
                contact_exists = any(
                    c['firstName'] == contact_data['firstName'] and 
                    c['lastName'] == contact_data['lastName'] and
                    c['phoneNumber1'] == contact_data['phoneNumber1']
                    for c in emergencyContacts
                )
                
                if not contact_exists:
                    emergencyContacts.append(contact_data)
                    flash('Contacto de emergencia agregado temporalmente', 'info')
                else:
                    flash('Este contacto ya existe', 'warning')
            else:
                flash('Error: No hay paciente activo para agregar contacto', 'error')
            
        except Exception as e:
            logger.error(f"Error adding emergency contact: {str(e)}")
            flash('Error al agregar contacto de emergencia', 'error')
    
    return render_template('home.html', view='addPatient', sec_view="addPatientInfo", 
                         emergencyContacts=emergencyContacts, allergies=allergies, 
                         familyBack=familyBack, preExistingConditions=preExistingConditions,
                         current_patient_id=current_patient_id)

@patients.route('/remove-contact', methods=['POST'])
def remove_contact():
    """Remove emergency contact from temporary storage"""
    try:
        index = int(request.form.get('index', -1))
        if 0 <= index < len(emergencyContacts):
            removed_contact = emergencyContacts.pop(index)
            flash(f'Contacto "{removed_contact["firstName"]} {removed_contact["lastName"]}" eliminado temporalmente', 'success')
        else:
            flash('Contacto no encontrado', 'error')
    except Exception as e:
        logger.error(f"Error removing emergency contact: {str(e)}")
        flash('Error al eliminar contacto de emergencia', 'error')
    
    return render_template('home.html', view='addPatient', sec_view="addPatientInfo", 
                         emergencyContacts=emergencyContacts, allergies=allergies, 
                         familyBack=familyBack, preExistingConditions=preExistingConditions,
                         current_patient_id=current_patient_id)

# FAMILY BACKGROUND ROUTES
@patients.route('/add-familyBack', methods=['GET', 'POST'])
def add_familyBack():
    """Add family background to temporary storage"""
    global current_patient_id, familyBack
    
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    if request.method == 'POST':
        try:
            background = request.form.get('familyBackground')
            time = request.form.get('time')
            degree_relationship = request.form.get('degreeRelationship')
            
            if not background or not background.strip():
                flash('Por favor ingrese un antecedente familiar válido', 'error')
                return redirect(url_for('clinic.home', view='addPatient', sec_view='addPatientInfo'))
            
            # Store temporarily - don't save to database yet
            if current_patient_id:
                family_data = {
                    'background': background.strip(),
                    'time': time,
                    'degree': degree_relationship
                }
                
                # Check if family background already exists
                bg_exists = any(
                    f['background'] == family_data['background'] and 
                    f['time'] == family_data['time']
                    for f in familyBack
                )
                
                if not bg_exists:
                    familyBack.append(family_data)
                    flash('Antecedente familiar agregado temporalmente', 'info')
                else:
                    flash('Este antecedente familiar ya existe', 'warning')
            else:
                flash('Error: No hay paciente activo para agregar antecedente', 'error')
            
        except Exception as e:
            logger.error(f"Error adding family background: {str(e)}")
            flash('Error al agregar antecedente familiar', 'error')
    
    return render_template('home.html', view='addPatient', sec_view="addPatientInfo", 
                         familyBack=familyBack, emergencyContacts=emergencyContacts, 
                         allergies=allergies, preExistingConditions=preExistingConditions,
                         current_patient_id=current_patient_id)

@patients.route('/remove-familyBack', methods=['POST'])
def remove_familyBack():
    """Remove family background from temporary storage"""
    try:
        index = int(request.form.get('index', -1))
        if 0 <= index < len(familyBack):
            removed_bg = familyBack.pop(index)
            flash(f'Antecedente familiar "{removed_bg["background"]}" eliminado temporalmente', 'success')
        else:
            flash('Antecedente familiar no encontrado', 'error')
    except Exception as e:
        logger.error(f"Error removing family background: {str(e)}")
        flash('Error al eliminar antecedente familiar', 'error')
    
    return render_template('home.html', view='addPatient', sec_view="addPatientInfo", 
                         familyBack=familyBack, emergencyContacts=emergencyContacts, 
                         allergies=allergies, preExistingConditions=preExistingConditions,
                         current_patient_id=current_patient_id)

# PRE-EXISTING CONDITIONS ROUTES
@patients.route('/add-conditions', methods=['GET', 'POST'])
def add_conditions():
    """Add pre-existing conditions to temporary storage"""
    global current_patient_id, preExistingConditions
    
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    if request.method == 'POST':
        try:
            disease_name = request.form.get('diseaseName')
            time = request.form.get('time')
            medicament = request.form.get('medicament')
            treatment = request.form.get('treatment')
            
            if not disease_name or not disease_name.strip():
                flash('Por favor ingrese un nombre de enfermedad válido', 'error')
                return redirect(url_for('clinic.home', view='addPatient', sec_view='addPatientInfo'))
            
            # Store temporarily - don't save to database yet
            if current_patient_id:
                condition_data = {
                    'diseaseName': disease_name.strip(),
                    'time': time,
                    'medicament': medicament.strip() if medicament else None,
                    'treatment': treatment.strip() if treatment else None
                }
                
                # Check if condition already exists
                condition_exists = any(
                    c['diseaseName'] == condition_data['diseaseName'] and 
                    c['time'] == condition_data['time']
                    for c in preExistingConditions
                )
                
                if not condition_exists:
                    preExistingConditions.append(condition_data)
                    flash('Condición preexistente agregada temporalmente', 'info')
                else:
                    flash('Esta condición ya existe', 'warning')
            else:
                flash('Error: No hay paciente activo para agregar condición', 'error')
            
        except Exception as e:
            logger.error(f"Error adding pre-existing condition: {str(e)}")
            flash('Error al agregar condición preexistente', 'error')
    
    return render_template('home.html', view='addPatient', sec_view="addPatientInfo", 
                         preExistingConditions=preExistingConditions, emergencyContacts=emergencyContacts, 
                         allergies=allergies, familyBack=familyBack,
                         current_patient_id=current_patient_id)

@patients.route('/remove-condition', methods=['POST'])
def remove_condition():
    """Remove pre-existing condition from temporary storage"""
    try:
        index = int(request.form.get('index', -1))
        if 0 <= index < len(preExistingConditions):
            removed_condition = preExistingConditions.pop(index)
            flash(f'Condición "{removed_condition["diseaseName"]}" eliminada temporalmente', 'success')
        else:
            flash('Condición no encontrada', 'error')
    except Exception as e:
        logger.error(f"Error removing pre-existing condition: {str(e)}")
        flash('Error al eliminar condición preexistente', 'error')
    
    return render_template('home.html', view='addPatient', sec_view="addPatientInfo", 
                         preExistingConditions=preExistingConditions, emergencyContacts=emergencyContacts, 
                         allergies=allergies, familyBack=familyBack,
                         current_patient_id=current_patient_id)

# COMPLETION AND MANAGEMENT ROUTES
@patients.route('/complete-patient-registration', methods=['POST'])
def complete_patient_registration():
    """Save all temporary data to database and complete patient registration"""
    global allergies, familyBack, preExistingConditions, emergencyContacts, current_patient_id
    
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    sessionID = session['cedula']
    
    try:
        if not current_patient_id:
            flash('No hay paciente activo para completar', 'error')
            return redirect(url_for('clinic.home', view='addPatient', sec_view='addPatient'))
        
        patient = Patient.query.filter_by(id=current_patient_id, is_deleted=False).first()
        if not patient:
            flash('Paciente no encontrado', 'error')
            return redirect(url_for('clinic.home', view='addPatient', sec_view='addPatient'))
        
        # Save allergies
        saved_count = {'allergies': 0, 'contacts': 0, 'backgrounds': 0, 'conditions': 0}
        
        for allergy_text in allergies:
            if allergy_text.strip():
                new_allergy = Allergy(
                    allergies=allergy_text.strip(),
                    idPatient=current_patient_id,
                    created_by=sessionID,
                    updated_by=sessionID
                )
                db.session.add(new_allergy)
                saved_count['allergies'] += 1
        
        # Save emergency contacts
        for contact_data in emergencyContacts:
            new_contact = EmergencyContact(
                firstName=contact_data['firstName'],
                lastName=contact_data['lastName'],
                address=contact_data['address'],
                relationship=contact_data['relationship'],
                phoneNumber1=contact_data['phoneNumber1'],
                phoneNumber2=contact_data.get('phoneNumber2'),
                idPatient=current_patient_id,
                created_by=sessionID,
                updated_by=sessionID
            )
            db.session.add(new_contact)
            saved_count['contacts'] += 1
        
        # Save family backgrounds
        for family_data in familyBack:
            if family_data.get('background') and family_data.get('time') and family_data.get('degree'):
                new_family_bg = FamilyBackground(
                    familyBackground=family_data['background'],
                    time=family_data['time'],
                    degreeRelationship=family_data['degree'],
                    idPatient=current_patient_id,
                    created_by=sessionID,
                    updated_by=sessionID
                )
                db.session.add(new_family_bg)
                saved_count['backgrounds'] += 1
        
        # Save pre-existing conditions
        for condition_data in preExistingConditions:
            if condition_data.get('diseaseName') and condition_data.get('time'):
                new_condition = PreExistingCondition(
                    diseaseName=condition_data['diseaseName'],
                    time=condition_data['time'],
                    medicament=condition_data.get('medicament'),
                    treatment=condition_data.get('treatment'),
                    idPatient=current_patient_id,
                    created_by=sessionID,
                    updated_by=sessionID
                )
                db.session.add(new_condition)
                saved_count['conditions'] += 1
        
        # Commit all changes
        db.session.commit()
        
        # Clear temporary data and reset current patient ID
        allergies.clear()
        familyBack.clear()
        preExistingConditions.clear()
        emergencyContacts.clear()
        current_patient_id = None
        
        # Create summary message
        summary_parts = []
        if saved_count['allergies'] > 0:
            summary_parts.append(f"{saved_count['allergies']} alergia(s)")
        if saved_count['contacts'] > 0:
            summary_parts.append(f"{saved_count['contacts']} contacto(s) de emergencia")
        if saved_count['backgrounds'] > 0:
            summary_parts.append(f"{saved_count['backgrounds']} antecedente(s) familiar(es)")
        if saved_count['conditions'] > 0:
            summary_parts.append(f"{saved_count['conditions']} condición(es) preexistente(s)")
        
        if summary_parts:
            summary = " • ".join(summary_parts)
            flash(f'Registro del paciente {patient.firstName} {patient.lastName1} completado exitosamente con: {summary}', 'success')
        else:
            flash(f'Registro del paciente {patient.firstName} {patient.lastName1} completado exitosamente (sin información adicional)', 'success')
        
        logger.info(f"Patient registration completed for: {patient.identifierCode} (ID: {patient.id}) with additional data")
        
        return redirect(url_for('clinic.home'))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error completing patient registration: {str(e)}")
        flash('Error al completar el registro del paciente', 'error')
        return redirect(url_for('clinic.home', view='addPatient', sec_view='addPatientInfo'))
