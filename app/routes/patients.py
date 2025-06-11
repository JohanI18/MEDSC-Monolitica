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

@patients.route('/add-patients', methods=['POST'])
def add_patients():
    """Add new patient with comprehensive error handling and complete registration"""
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
            
            # Save any temporary additional data if exists
            _save_additional_data(new_patient.id, sessionID)
            
            # Clear temporary data
            allergies.clear()
            familyBack.clear()
            preExistingConditions.clear()
            emergencyContacts.clear()
            current_patient_id = None
            
            logger.info(f"Patient created and registration completed: {new_patient.identifierCode} with ID: {new_patient.id}")
            flash(f'Paciente {new_patient.firstName} {new_patient.lastName1} registrado exitosamente', 'success')
            return redirect(url_for('clinic.home'))

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

def _save_additional_data(patient_id, session_id):
    """Helper function to save any temporary additional data"""
    try:
        # Save allergies if any
        for allergy_text in allergies:
            if allergy_text.strip():
                new_allergy = Allergy(
                    allergies=allergy_text.strip(),
                    idPatient=patient_id,
                    created_by=session_id,
                    updated_by=session_id
                )
                db.session.add(new_allergy)
        
        # Save emergency contacts if any
        for contact_data in emergencyContacts:
            new_contact = EmergencyContact(
                firstName=contact_data['firstName'],
                lastName=contact_data['lastName'],
                address=contact_data['address'],
                relationship=contact_data['relationship'],
                phoneNumber1=contact_data['phoneNumber1'],
                phoneNumber2=contact_data.get('phoneNumber2'),
                idPatient=patient_id,
                created_by=session_id,
                updated_by=session_id
            )
            db.session.add(new_contact)
        
        # Save family backgrounds if any
        for family_data in familyBack:
            if family_data.get('background') and family_data.get('time') and family_data.get('degree'):
                new_family_bg = FamilyBackground(
                    familyBackground=family_data['background'],
                    time=family_data['time'],
                    degreeRelationship=family_data['degree'],
                    idPatient=patient_id,
                    created_by=session_id,
                    updated_by=session_id
                )
                db.session.add(new_family_bg)
        
        # Save pre-existing conditions if any
        for condition_data in preExistingConditions:
            if condition_data.get('diseaseName') and condition_data.get('time'):
                new_condition = PreExistingCondition(
                    diseaseName=condition_data['diseaseName'],
                    time=condition_data['time'],
                    medicament=condition_data.get('medicament'),
                    treatment=condition_data.get('treatment'),
                    idPatient=patient_id,
                    created_by=session_id,
                    updated_by=session_id
                )
                db.session.add(new_condition)
        
        db.session.commit()
        logger.info(f"Additional data saved for patient {patient_id}")
        
    except Exception as e:
        logger.error(f"Error saving additional data: {str(e)}")
        # Don't raise the exception as the patient is already created
        pass

@patients.route('/add-allergies', methods=['GET', 'POST'])
def add_allergies():
    """Add allergies with improved error handling and persistence"""
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    sessionID = session['cedula']
    
    if request.method == 'POST':
        try:
            new_allergy = request.form.get('allergy')
            patient_id = request.form.get('patient_id')  # Get patient ID if available
            
            if not new_allergy or not new_allergy.strip():
                flash('Por favor ingrese una alergia válida', 'error')
                return render_template('home.html', view='addPatient', sec_view="addPatientInfo", 
                                     allergies=allergies, emergencyContacts=emergencyContacts, 
                                     familyBack=familyBack, preExistingConditions=preExistingConditions)
            
            # If we have a patient ID, save directly to database
            if patient_id:
                new_allergy_record = Allergy(
                    allergies=new_allergy.strip(),
                    idPatient=patient_id,
                    created_by=sessionID,
                    updated_by=sessionID
                )
                db.session.add(new_allergy_record)
                db.session.commit()
                flash('Alergia agregada exitosamente', 'success')
                logger.info(f"Allergy added for patient {patient_id}: {new_allergy}")
            else:
                # Store temporarily if no patient ID
                if new_allergy.strip() not in allergies:
                    allergies.append(new_allergy.strip())
                    flash('Alergia agregada temporalmente', 'info')
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error adding allergy: {str(e)}")
            flash('Error al agregar alergia', 'error')
    
    return render_template('home.html', view='addPatient', sec_view="addPatientInfo", 
                         allergies=allergies, emergencyContacts=emergencyContacts, 
                         familyBack=familyBack, preExistingConditions=preExistingConditions)

@patients.route('/remove-allergy', methods=['POST'])
def remove_allergy():
    """Remove allergy from temporary list"""
    try:
        allergy_to_remove = request.form.get('allergy')
        if allergy_to_remove in allergies:
            allergies.remove(allergy_to_remove)
            flash('Alergia eliminada', 'success')
        else:
            flash('Alergia no encontrada', 'error')
    except Exception as e:
        logger.error(f"Error removing allergy: {str(e)}")
        flash('Error al eliminar alergia', 'error')
    
    return render_template('home.html', view='addPatient', sec_view="addPatientInfo", 
                         allergies=allergies, emergencyContacts=emergencyContacts, 
                         familyBack=familyBack, preExistingConditions=preExistingConditions)

@patients.route('/add-contact', methods=['GET', 'POST'])
def add_contact():
    """Add emergency contact with improved error handling"""
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    sessionID = session['cedula']
    
    if request.method == 'POST':
        try:
            first_name = request.form.get('firstName')
            last_name = request.form.get('lastName')
            address = request.form.get('address')
            relationship = request.form.get('relationship')
            phone_number1 = request.form.get('phoneNumber1')
            phone_number2 = request.form.get('phoneNumber2')
            patient_id = request.form.get('patient_id')
            
            # Validate required fields
            if not all([first_name, last_name, address, relationship, phone_number1]):
                flash('Por favor complete todos los campos requeridos del contacto de emergencia', 'error')
                return render_template('home.html', view='addPatient', sec_view="addPatientInfo", emergencyContacts=emergencyContacts)
            
            # If we have a patient ID, save directly to database
            if patient_id:
                new_emergency_contact = EmergencyContact(
                    firstName=first_name.strip(),
                    lastName=last_name.strip(),
                    address=address.strip(),
                    relationship=relationship.strip(),
                    phoneNumber1=phone_number1.strip(),
                    phoneNumber2=phone_number2.strip() if phone_number2 else None,
                    idPatient=patient_id,
                    created_by=sessionID,
                    updated_by=sessionID
                )
                db.session.add(new_emergency_contact)
                db.session.commit()
                flash('Contacto de emergencia agregado exitosamente', 'success')
                logger.info(f"Emergency contact added for patient {patient_id}: {first_name} {last_name}")
            else:
                # Store temporarily
                contact_data = {
                    'firstName': first_name.strip(),
                    'lastName': last_name.strip(),
                    'address': address.strip(),
                    'relationship': relationship.strip(),
                    'phoneNumber1': phone_number1.strip(),
                    'phoneNumber2': phone_number2.strip() if phone_number2 else None
                }
                if contact_data not in emergencyContacts:
                    emergencyContacts.append(contact_data)
                    flash('Contacto de emergencia agregado temporalmente', 'info')
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error adding emergency contact: {str(e)}")
            flash('Error al agregar contacto de emergencia', 'error')
    
    # Handle GET request (when called from URL with parameters)
    elif request.method == 'GET' and request.args:
        try:
            # Extract parameters from URL
            first_name = request.args.get('firstName')
            last_name = request.args.get('lastName')
            address = request.args.get('address')
            relationship = request.args.get('relationship')
            phone_number1 = request.args.get('phoneNumber1')
            phone_number2 = request.args.get('phoneNumber2')
            
            if all([first_name, last_name, address, relationship, phone_number1]):
                contact_data = {
                    'firstName': first_name.strip(),
                    'lastName': last_name.strip(),
                    'address': address.strip(),
                    'relationship': relationship.strip(),
                    'phoneNumber1': phone_number1.strip(),
                    'phoneNumber2': phone_number2.strip() if phone_number2 else None
                }
                if contact_data not in emergencyContacts:
                    emergencyContacts.append(contact_data)
                    flash('Contacto de emergencia agregado temporalmente', 'info')
                else:
                    flash('Contacto de emergencia ya existe', 'warning')
            else:
                flash('Datos incompletos para el contacto de emergencia', 'error')
                
        except Exception as e:
            logger.error(f"Error processing emergency contact from GET: {str(e)}")
            flash('Error al procesar contacto de emergencia', 'error')
    
    return render_template('home.html', view='addPatient', sec_view="addPatientInfo", 
                         emergencyContacts=emergencyContacts, allergies=allergies, 
                         familyBack=familyBack, preExistingConditions=preExistingConditions)

@patients.route('/remove-contact', methods=['POST'])
def remove_contact():
    """Remove emergency contact from temporary list"""
    try:
        index = int(request.form.get('index', -1))
        if 0 <= index < len(emergencyContacts):
            removed_item = emergencyContacts.pop(index)
            flash('Contacto de emergencia eliminado', 'success')
        else:
            flash('Contacto de emergencia no encontrado', 'error')
    except Exception as e:
        logger.error(f"Error removing emergency contact: {str(e)}")
        flash('Error al eliminar contacto de emergencia', 'error')
    
    return render_template('home.html', view='addPatient', sec_view="addPatientInfo", 
                         emergencyContacts=emergencyContacts, allergies=allergies, 
                         familyBack=familyBack, preExistingConditions=preExistingConditions)

@patients.route('/complete-patient-registration', methods=['POST'])
def complete_patient_registration():
    """Save all temporary data to database and complete patient registration"""
    global allergies, familyBack, preExistingConditions, emergencyContacts, current_patient_id
    
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    sessionID = session['cedula']
    
    try:
        # First try to use the tracked current patient ID
        latest_patient = None
        if current_patient_id:
            latest_patient = Patient.query.filter_by(
                id=current_patient_id,
                is_deleted=False
            ).first()
            logger.info(f"Using tracked patient ID: {current_patient_id}")
        
        # Fallback: Get the most recently created patient if current_patient_id is not available
        if not latest_patient:
            latest_patient = Patient.query.filter_by(
                created_by=sessionID,
                is_deleted=False
            ).order_by(Patient.created_at.desc()).first()
            logger.info(f"Fallback: Using most recent patient created by {sessionID}")
        
        if not latest_patient:
            flash('No se encontró el paciente para completar el registro', 'error')
            return redirect(url_for('clinic.home', view='addPatient', sec_view='addPatient'))
        
        logger.info(f"Adding additional data for patient ID: {latest_patient.id}, Code: {latest_patient.identifierCode}, Created by: {latest_patient.created_by}")
        
        # Save allergies
        for allergy_text in allergies:
            if allergy_text.strip():
                new_allergy = Allergy(
                    allergies=allergy_text.strip(),
                    idPatient=latest_patient.id,
                    created_by=sessionID,
                    updated_by=sessionID
                )
                db.session.add(new_allergy)
                logger.info(f"Adding allergy: {allergy_text} for patient {latest_patient.id}")
        
        # Save emergency contacts
        for contact_data in emergencyContacts:
            new_contact = EmergencyContact(
                firstName=contact_data['firstName'],
                lastName=contact_data['lastName'],
                address=contact_data['address'],
                relationship=contact_data['relationship'],
                phoneNumber1=contact_data['phoneNumber1'],
                phoneNumber2=contact_data.get('phoneNumber2'),
                idPatient=latest_patient.id,
                created_by=sessionID,
                updated_by=sessionID
            )
            db.session.add(new_contact)
            logger.info(f"Adding emergency contact: {contact_data['firstName']} {contact_data['lastName']} for patient {latest_patient.id}")
        
        # Save family backgrounds
        for family_data in familyBack:
            if family_data.get('background') and family_data.get('time') and family_data.get('degree'):
                new_family_bg = FamilyBackground(
                    familyBackground=family_data['background'],
                    time=family_data['time'],
                    degreeRelationship=family_data['degree'],
                    idPatient=latest_patient.id,
                    created_by=sessionID,
                    updated_by=sessionID
                )
                db.session.add(new_family_bg)
                logger.info(f"Adding family background: {family_data['background']} for patient {latest_patient.id}")
        
        # Save pre-existing conditions
        for condition_data in preExistingConditions:
            if condition_data.get('diseaseName') and condition_data.get('time'):
                new_condition = PreExistingCondition(
                    diseaseName=condition_data['diseaseName'],
                    time=condition_data['time'],
                    medicament=condition_data.get('medicament'),
                    treatment=condition_data.get('treatment'),
                    idPatient=latest_patient.id,
                    created_by=sessionID,
                    updated_by=sessionID
                )
                db.session.add(new_condition)
                logger.info(f"Adding pre-existing condition: {condition_data['diseaseName']} for patient {latest_patient.id}")
        
        # Commit all changes
        db.session.commit()
        
        # Clear temporary data and reset current patient ID
        allergies.clear()
        familyBack.clear()
        preExistingConditions.clear()
        emergencyContacts.clear()
        current_patient_id = None
        
        flash(f'Registro del paciente {latest_patient.firstName} {latest_patient.lastName1} completado exitosamente', 'success')
        logger.info(f"Patient registration completed for: {latest_patient.identifierCode} (ID: {latest_patient.id})")
        
        return redirect(url_for('clinic.home'))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error completing patient registration: {str(e)}")
        flash('Error al completar el registro del paciente', 'error')
        return redirect(url_for('clinic.home', view='addPatient', sec_view='addPatientInfo'))

@patients.route('/clear-temp-data', methods=['POST'])
def clear_temp_data():
    """Clear all temporary data"""
    global allergies, familyBack, preExistingConditions, emergencyContacts, current_patient_id
    allergies.clear()
    familyBack.clear()
    preExistingConditions.clear()
    emergencyContacts.clear()
    current_patient_id = None  # Reset current patient ID
    flash('Datos temporales limpiados', 'info')
    return redirect(url_for('clinic.home', view='addPatient', sec_view='addPatient'))

@patients.route('/edit-patient/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    """Edit existing patient"""
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    sessionID = session['cedula']
    
    try:
        patient = Patient.query.filter_by(id=patient_id, is_deleted=False).first()
        if not patient:
            flash('Paciente no encontrado', 'error')
            return redirect(url_for('clinic.home'))
        
        if request.method == 'POST':
            # Update patient data
            patient.firstName = request.form.get('firstName', patient.firstName)
            patient.middleName = request.form.get('middleName', patient.middleName)
            patient.lastName1 = request.form.get('lastName1', patient.lastName1)
            patient.lastName2 = request.form.get('lastName2', patient.lastName2)
            patient.nationality = request.form.get('nationality', patient.nationality)
            patient.address = request.form.get('address', patient.address)
            patient.phoneNumber = request.form.get('phoneNumber', patient.phoneNumber)
            patient.gender = request.form.get('gender', patient.gender)
            patient.sex = request.form.get('sex', patient.sex)
            patient.civilStatus = request.form.get('civilStatus', patient.civilStatus)
            patient.job = request.form.get('job', patient.job)
            patient.bloodType = request.form.get('bloodType', patient.bloodType)
            patient.email = request.form.get('email', patient.email)
            patient.updated_by = sessionID
            
            db.session.commit()
            flash('Paciente actualizado exitosamente', 'success')
            logger.info(f"Patient updated: {patient.identifierCode}")
            return redirect(url_for('patients.show_patients'))
        
        return render_template('edit_patient.html', patient=patient)
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error editing patient: {str(e)}")
        flash('Error al editar paciente', 'error')
        return redirect(url_for('patients.show_patients'))

@patients.route('/delete-patient/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    """Soft delete patient"""
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    sessionID = session['cedula']
    
    try:
        patient = Patient.query.filter_by(id=patient_id, is_deleted=False).first()
        if not patient:
            flash('Paciente no encontrado', 'error')
            return redirect(url_for('patients.show_patients'))
        
        # Soft delete
        patient.is_deleted = True
        patient.updated_by = sessionID
        db.session.commit()
        
        flash('Paciente eliminado exitosamente', 'success')
        logger.info(f"Patient soft deleted: {patient.identifierCode}")
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting patient: {str(e)}")
        flash('Error al eliminar paciente', 'error')
    
    return redirect(url_for('patients.show_patients'))

@patients.route('/add-familyBack', methods=['GET', 'POST'])
def add_familyBack():
    """Add family background with improved error handling"""
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    sessionID = session['cedula']
    
    if request.method == 'POST':
        try:
            background = request.form.get('familyBackground')
            time = request.form.get('time')
            degree_relationship = request.form.get('degreeRelationship')
            patient_id = request.form.get('patient_id')
            
            if not background or not background.strip():
                flash('Por favor ingrese un antecedente familiar válido', 'error')
                return render_template('home.html', view='addPatient', sec_view="addPatientInfo", 
                                     familyBack=familyBack, emergencyContacts=emergencyContacts, 
                                     allergies=allergies, preExistingConditions=preExistingConditions)
            
            # Always store temporarily for now - will save to DB at final step
            family_data = {
                'background': background.strip(),
                'time': time,
                'degree': degree_relationship
            }
            if family_data not in familyBack:
                familyBack.append(family_data)
                flash('Antecedente familiar agregado temporalmente', 'info')
            
        except Exception as e:
            logger.error(f"Error adding family background: {str(e)}")
            flash('Error al agregar antecedente familiar', 'error')
    
    return render_template('home.html', view='addPatient', sec_view="addPatientInfo", 
                         familyBack=familyBack, emergencyContacts=emergencyContacts, 
                         allergies=allergies, preExistingConditions=preExistingConditions)

@patients.route('/remove-familyBack', methods=['POST'])
def remove_familyBack():
    """Remove family background from temporary list"""
    try:
        index = int(request.form.get('index', -1))
        if 0 <= index < len(familyBack):
            removed_item = familyBack.pop(index)
            flash('Antecedente familiar eliminado', 'success')
        else:
            flash('Antecedente familiar no encontrado', 'error')
    except Exception as e:
        logger.error(f"Error removing family background: {str(e)}")
        flash('Error al eliminar antecedente familiar', 'error')
    
    return render_template('home.html', view='addPatient', sec_view="addPatientInfo", 
                         familyBack=familyBack, emergencyContacts=emergencyContacts, 
                         allergies=allergies, preExistingConditions=preExistingConditions)

@patients.route('/add-conditions', methods=['GET', 'POST'])
def add_conditions():
    """Add pre-existing conditions with improved error handling"""
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    sessionID = session['cedula']
    
    if request.method == 'POST':
        try:
            disease_name = request.form.get('diseaseName')
            time = request.form.get('time')
            medicament = request.form.get('medicament')
            treatment = request.form.get('treatment')
            patient_id = request.form.get('patient_id')
            
            if not disease_name or not disease_name.strip():
                flash('Por favor ingrese un nombre de enfermedad válido', 'error')
                return render_template('home.html', view='addPatient', sec_view="addPatientInfo", 
                                     preExistingConditions=preExistingConditions, emergencyContacts=emergencyContacts, 
                                     allergies=allergies, familyBack=familyBack)
            
            # Always store temporarily for now - will save to DB at final step
            condition_data = {
                'diseaseName': disease_name.strip(),
                'time': time,
                'medicament': medicament,
                'treatment': treatment
            }
            if condition_data not in preExistingConditions:
                preExistingConditions.append(condition_data)
                flash('Condición preexistente agregada temporalmente', 'info')
            
        except Exception as e:
            logger.error(f"Error adding pre-existing condition: {str(e)}")
            flash('Error al agregar condición preexistente', 'error')
    
    return render_template('home.html', view='addPatient', sec_view="addPatientInfo", 
                         preExistingConditions=preExistingConditions, emergencyContacts=emergencyContacts, 
                         allergies=allergies, familyBack=familyBack)
