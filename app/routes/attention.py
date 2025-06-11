from flask import Blueprint, render_template, session, request, redirect, url_for, flash, jsonify
from models.models_flask import (
    Attention, Patient, Doctor, Diagnostic, Histopathology, Imaging, 
    Laboratory, RegionalPhysicalExamination, ReviewOrgansSystem, Treatment
)
from utils.db import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import logging

attention = Blueprint('attention', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global lists for temporary storage during attention creation
vital_signs_data = {}
evaluation_data = {}
physical_exams = []
organ_system_reviews = []
diagnostics = []
treatments = []
histopathologies = []
imagings = []
laboratories = []
current_attention_id = None
selected_patient_id = None

@attention.route('/add-vital-signs', methods=['POST'])
def add_vital_signs():
    """Save vital signs data temporarily"""
    global vital_signs_data
    
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    try:
        # Store vital signs data temporarily
        vital_signs_data = {
            'weight': request.form.get('weight'),
            'height': request.form.get('height'),
            'temperature': request.form.get('temperature'),
            'bloodPressure': request.form.get('bloodPressure'),
            'heartRate': request.form.get('heartRate'),
            'oxygenSaturation': request.form.get('oxygenSaturation'),
            'breathingFrequency': request.form.get('breathingFrequency'),
            'glucose': request.form.get('glucose'),
            'hemoglobin': request.form.get('hemoglobin')
        }
        
        flash('Signos vitales guardados temporalmente', 'success')
        logger.info("Vital signs data saved temporarily")
        
    except Exception as e:
        logger.error(f"Error saving vital signs: {str(e)}")
        flash('Error al guardar signos vitales', 'error')
    
    return render_template('home.html', view='addAttention', 
                         vital_signs_data=vital_signs_data)

@attention.route('/add-initial-evaluation', methods=['POST'])
def add_initial_evaluation():
    """Save initial evaluation data temporarily"""
    global evaluation_data
    
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    try:
        # Validate required fields
        reason_consultation = request.form.get('reasonConsultation')
        current_illness = request.form.get('currentIllness')
        
        if not reason_consultation or not current_illness:
            flash('Motivo de consulta y enfermedad actual son requeridos', 'error')
            return render_template('home.html', view='addAttention')
        
        # Store evaluation data temporarily
        evaluation_data = {
            'reasonConsultation': reason_consultation.strip(),
            'currentIllness': current_illness.strip()
        }
        
        flash('Evaluación inicial guardada temporalmente', 'success')
        logger.info("Initial evaluation data saved temporarily")
        
    except Exception as e:
        logger.error(f"Error saving initial evaluation: {str(e)}")
        flash('Error al guardar evaluación inicial', 'error')
    
    return render_template('home.html', view='addAttention', 
                         evaluation_data=evaluation_data)

@attention.route('/add-physical-exam', methods=['POST'])
def add_physical_exam():
    """Add physical examination to temporary list"""
    global physical_exams
    
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    try:
        type_examination = request.form.get('typeExamination')
        examination = request.form.get('examination')
        
        if not type_examination or not examination:
            flash('Tipo de examen y hallazgos son requeridos', 'error')
            return render_template('home.html', view='addAttention', physicalExams=physical_exams)
        
        exam_data = {
            'typeExamination': type_examination.strip(),
            'examination': examination.strip()
        }
        
        if exam_data not in physical_exams:
            physical_exams.append(exam_data)
            flash('Examen físico agregado', 'success')
        else:
            flash('Este examen ya existe', 'warning')
        
        logger.info(f"Physical exam added: {type_examination}")
        
    except Exception as e:
        logger.error(f"Error adding physical exam: {str(e)}")
        flash('Error al agregar examen físico', 'error')
    
    return render_template('home.html', view='addAttention', physicalExams=physical_exams)

@attention.route('/remove-physical-exam', methods=['POST'])
def remove_physical_exam():
    """Remove physical examination from temporary list"""
    global physical_exams
    
    try:
        index = int(request.form.get('index', -1))
        if 0 <= index < len(physical_exams):
            removed_item = physical_exams.pop(index)
            flash('Examen físico eliminado', 'success')
        else:
            flash('Examen no encontrado', 'error')
    except Exception as e:
        logger.error(f"Error removing physical exam: {str(e)}")
        flash('Error al eliminar examen', 'error')
    
    return render_template('home.html', view='addAttention', physicalExams=physical_exams)

@attention.route('/add-organ-system-review', methods=['POST'])
def add_organ_system_review():
    """Add organ system review to temporary list"""
    global organ_system_reviews
    
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    try:
        type_review = request.form.get('typeReview')
        review = request.form.get('review')
        
        if not type_review or not review:
            flash('Tipo de revisión y hallazgos son requeridos', 'error')
            return render_template('home.html', view='addAttention', organSystemReviews=organ_system_reviews)
        
        review_data = {
            'typeReview': type_review.strip(),
            'review': review.strip()
        }
        
        if review_data not in organ_system_reviews:
            organ_system_reviews.append(review_data)
            flash('Revisión de sistema agregada', 'success')
        else:
            flash('Esta revisión ya existe', 'warning')
        
        logger.info(f"Organ system review added: {type_review}")
        
    except Exception as e:
        logger.error(f"Error adding organ system review: {str(e)}")
        flash('Error al agregar revisión de sistema', 'error')
    
    return render_template('home.html', view='addAttention', organSystemReviews=organ_system_reviews)

@attention.route('/remove-organ-system-review', methods=['POST'])
def remove_organ_system_review():
    """Remove organ system review from temporary list"""
    global organ_system_reviews
    
    try:
        index = int(request.form.get('index', -1))
        if 0 <= index < len(organ_system_reviews):
            removed_item = organ_system_reviews.pop(index)
            flash('Revisión de sistema eliminada', 'success')
        else:
            flash('Revisión no encontrada', 'error')
    except Exception as e:
        logger.error(f"Error removing organ system review: {str(e)}")
        flash('Error al eliminar revisión', 'error')
    
    return render_template('home.html', view='addAttention', organSystemReviews=organ_system_reviews)

@attention.route('/add-diagnostic', methods=['POST'])
def add_diagnostic():
    """Add diagnostic to temporary list"""
    global diagnostics
    
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    try:
        cie10_code = request.form.get('cie10Code')
        disease = request.form.get('disease')
        observations = request.form.get('observations')
        diagnostic_condition = request.form.get('diagnosticCondition')
        chronology = request.form.get('chronology')
        
        if not all([cie10_code, disease, observations, diagnostic_condition, chronology]):
            flash('Todos los campos del diagnóstico son requeridos', 'error')
            return render_template('home.html', view='addAttention', diagnostics=diagnostics)
        
        diagnostic_data = {
            'cie10Code': cie10_code.strip(),
            'disease': disease.strip(),
            'observations': observations.strip(),
            'diagnosticCondition': diagnostic_condition.strip(),
            'chronology': chronology.strip()
        }
        
        if diagnostic_data not in diagnostics:
            diagnostics.append(diagnostic_data)
            flash('Diagnóstico agregado', 'success')
        else:
            flash('Este diagnóstico ya existe', 'warning')
        
        logger.info(f"Diagnostic added: {cie10_code} - {disease}")
        
    except Exception as e:
        logger.error(f"Error adding diagnostic: {str(e)}")
        flash('Error al agregar diagnóstico', 'error')
    
    return render_template('home.html', view='addAttention', diagnostics=diagnostics)

@attention.route('/remove-diagnostic', methods=['POST'])
def remove_diagnostic():
    """Remove diagnostic from temporary list"""
    global diagnostics
    
    try:
        index = int(request.form.get('index', -1))
        if 0 <= index < len(diagnostics):
            removed_item = diagnostics.pop(index)
            flash('Diagnóstico eliminado', 'success')
        else:
            flash('Diagnóstico no encontrado', 'error')
    except Exception as e:
        logger.error(f"Error removing diagnostic: {str(e)}")
        flash('Error al eliminar diagnóstico', 'error')
    
    return render_template('home.html', view='addAttention', diagnostics=diagnostics)

@attention.route('/add-treatment', methods=['POST'])
def add_treatment():
    """Add treatment to temporary list"""
    global treatments
    
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    try:
        medicament = request.form.get('medicament')
        via = request.form.get('via')
        dosage = request.form.get('dosage')
        unity = request.form.get('unity')
        frequency = request.form.get('frequency')
        indications = request.form.get('indications')
        warning = request.form.get('warning')
        
        if not all([medicament, via, dosage, unity, frequency, indications]):
            flash('Todos los campos requeridos del tratamiento deben completarse', 'error')
            return render_template('home.html', view='addAttention', treatments=treatments)
        
        treatment_data = {
            'medicament': medicament.strip(),
            'via': via.strip(),
            'dosage': dosage.strip(),
            'unity': unity.strip(),
            'frequency': frequency.strip(),
            'indications': indications.strip(),
            'warning': warning.strip() if warning else None
        }
        
        if treatment_data not in treatments:
            treatments.append(treatment_data)
            flash('Tratamiento agregado', 'success')
        else:
            flash('Este tratamiento ya existe', 'warning')
        
        logger.info(f"Treatment added: {medicament}")
        
    except Exception as e:
        logger.error(f"Error adding treatment: {str(e)}")
        flash('Error al agregar tratamiento', 'error')
    
    return render_template('home.html', view='addAttention', treatments=treatments)

@attention.route('/remove-treatment', methods=['POST'])
def remove_treatment():
    """Remove treatment from temporary list"""
    global treatments
    
    try:
        index = int(request.form.get('index', -1))
        if 0 <= index < len(treatments):
            removed_item = treatments.pop(index)
            flash('Tratamiento eliminado', 'success')
        else:
            flash('Tratamiento no encontrado', 'error')
    except Exception as e:
        logger.error(f"Error removing treatment: {str(e)}")
        flash('Error al eliminar tratamiento', 'error')
    
    return render_template('home.html', view='addAttention', treatments=treatments)

@attention.route('/add-histopathology', methods=['POST'])
def add_histopathology():
    """Add histopathology to temporary list"""
    global histopathologies
    
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    try:
        histopathology = request.form.get('histopathology')
        
        if not histopathology or not histopathology.strip():
            flash('El resultado histopatológico es requerido', 'error')
            return render_template('home.html', view='addAttention', histopathologies=histopathologies)
        
        histo_data = {
            'histopathology': histopathology.strip()
        }
        
        if histo_data not in histopathologies:
            histopathologies.append(histo_data)
            flash('Histopatología agregada', 'success')
        else:
            flash('Esta histopatología ya existe', 'warning')
        
        logger.info("Histopathology added")
        
    except Exception as e:
        logger.error(f"Error adding histopathology: {str(e)}")
        flash('Error al agregar histopatología', 'error')
    
    return render_template('home.html', view='addAttention', histopathologies=histopathologies)

@attention.route('/remove-histopathology', methods=['POST'])
def remove_histopathology():
    """Remove histopathology from temporary list"""
    global histopathologies
    
    try:
        index = int(request.form.get('index', -1))
        if 0 <= index < len(histopathologies):
            removed_item = histopathologies.pop(index)
            flash('Histopatología eliminada', 'success')
        else:
            flash('Histopatología no encontrada', 'error')
    except Exception as e:
        logger.error(f"Error removing histopathology: {str(e)}")
        flash('Error al eliminar histopatología', 'error')
    
    return render_template('home.html', view='addAttention', histopathologies=histopathologies)

@attention.route('/add-imaging', methods=['POST'])
def add_imaging():
    """Add imaging to temporary list"""
    global imagings
    
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    try:
        type_imaging = request.form.get('typeImaging')
        imaging = request.form.get('imaging')
        
        if not type_imaging or not imaging:
            flash('Tipo de imagen y resultado son requeridos', 'error')
            return render_template('home.html', view='addAttention', imagings=imagings)
        
        imaging_data = {
            'typeImaging': type_imaging.strip(),
            'imaging': imaging.strip()
        }
        
        if imaging_data not in imagings:
            imagings.append(imaging_data)
            flash('Imagen agregada', 'success')
        else:
            flash('Esta imagen ya existe', 'warning')
        
        logger.info(f"Imaging added: {type_imaging}")
        
    except Exception as e:
        logger.error(f"Error adding imaging: {str(e)}")
        flash('Error al agregar imagen', 'error')
    
    return render_template('home.html', view='addAttention', imagings=imagings)

@attention.route('/remove-imaging', methods=['POST'])
def remove_imaging():
    """Remove imaging from temporary list"""
    global imagings
    
    try:
        index = int(request.form.get('index', -1))
        if 0 <= index < len(imagings):
            removed_item = imagings.pop(index)
            flash('Imagen eliminada', 'success')
        else:
            flash('Imagen no encontrada', 'error')
    except Exception as e:
        logger.error(f"Error removing imaging: {str(e)}")
        flash('Error al eliminar imagen', 'error')
    
    return render_template('home.html', view='addAttention', imagings=imagings)

@attention.route('/add-laboratory', methods=['POST'])
def add_laboratory():
    """Add laboratory to temporary list"""
    global laboratories
    
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    try:
        type_exam = request.form.get('typeExam')
        exam = request.form.get('exam')
        
        if not type_exam or not exam:
            flash('Tipo de examen y resultado son requeridos', 'error')
            return render_template('home.html', view='addAttention', laboratories=laboratories)
        
        lab_data = {
            'typeExam': type_exam.strip(),
            'exam': exam.strip()
        }
        
        if lab_data not in laboratories:
            laboratories.append(lab_data)
            flash('Laboratorio agregado', 'success')
        else:
            flash('Este laboratorio ya existe', 'warning')
        
        logger.info(f"Laboratory added: {type_exam}")
        
    except Exception as e:
        logger.error(f"Error adding laboratory: {str(e)}")
        flash('Error al agregar laboratorio', 'error')
    
    return render_template('home.html', view='addAttention', laboratories=laboratories)

@attention.route('/remove-laboratory', methods=['POST'])
def remove_laboratory():
    """Remove laboratory from temporary list"""
    global laboratories
    
    try:
        index = int(request.form.get('index', -1))
        if 0 <= index < len(laboratories):
            removed_item = laboratories.pop(index)
            flash('Laboratorio eliminado', 'success')
        else:
            flash('Laboratorio no encontrado', 'error')
    except Exception as e:
        logger.error(f"Error removing laboratory: {str(e)}")
        flash('Error al eliminar laboratorio', 'error')
    
    return render_template('home.html', view='addAttention', laboratories=laboratories)

@attention.route('/add-evolution', methods=['POST'])
def add_evolution():
    """Save evolution data temporarily"""
    global evaluation_data
    
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    try:
        evolution = request.form.get('evolution')
        
        if not evolution or not evolution.strip():
            flash('La evolución es requerida', 'error')
            return render_template('home.html', view='addAttention')
        
        # Update evaluation data with evolution
        evaluation_data['evolution'] = evolution.strip()
        
        flash('Evolución guardada temporalmente', 'success')
        logger.info("Evolution data saved temporarily")
        
    except Exception as e:
        logger.error(f"Error saving evolution: {str(e)}")
        flash('Error al guardar evolución', 'error')
    
    return render_template('home.html', view='addAttention')

@attention.route('/select-patient-for-attention', methods=['POST'])
def select_patient_for_attention():
    """Select patient for current attention"""
    global selected_patient_id
    
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    try:
        patient_id = request.form.get('selectedPatient')
        
        if not patient_id:
            flash('Debe seleccionar un paciente', 'error')
            return redirect(url_for('clinic.home', view='addAttention'))
        
        # Validate that patient exists
        patient = Patient.query.filter_by(id=patient_id, is_deleted=False).first()
        if not patient:
            flash('Paciente no encontrado', 'error')
            return redirect(url_for('clinic.home', view='addAttention'))
        
        selected_patient_id = int(patient_id)
        flash(f'Paciente {patient.firstName} {patient.lastName1} seleccionado. Puede proceder con los signos vitales.', 'success')
        logger.info(f"Patient {patient_id} selected for attention")
        
    except Exception as e:
        logger.error(f"Error selecting patient: {str(e)}")
        flash('Error al seleccionar paciente', 'error')
    
    return redirect(url_for('clinic.home', view='addAttention'))

@attention.route('/change-selected-patient', methods=['POST'])
def change_selected_patient():
    """Change selected patient for attention"""
    global selected_patient_id
    
    # Clear selected patient
    selected_patient_id = None
    flash('Selección de paciente cancelada. Seleccione un nuevo paciente', 'info')
    
    return redirect(url_for('clinic.home', view='addAttention'))

@attention.route('/complete-attention', methods=['POST'])
def complete_attention():
    """Save all attention data to database"""
    global vital_signs_data, evaluation_data, physical_exams, organ_system_reviews
    global diagnostics, treatments, histopathologies, imagings, laboratories, current_attention_id
    global selected_patient_id
    
    if 'cedula' not in session:
        flash('Sesión no válida', 'error')
        return redirect(url_for('clinic.index'))
    
    sessionID = session['cedula']
    
    try:
        # Validate selected patient
        if not selected_patient_id:
            flash('Debe seleccionar un paciente antes de finalizar la atención', 'error')
            return redirect(url_for('clinic.home', view='addAttention'))
        
        # Validate required data
        if not evaluation_data.get('reasonConsultation') or not evaluation_data.get('currentIllness'):
            flash('Debe completar la evaluación inicial antes de finalizar', 'error')
            return redirect(url_for('clinic.home', view='addAttention'))
        
        if not evaluation_data.get('evolution'):
            flash('Debe completar la evolución antes de finalizar', 'error')
            return redirect(url_for('clinic.home', view='addAttention'))
        
        # Get doctor information
        doctor = Doctor.query.filter_by(identifierCode=sessionID, is_deleted=False).first()
        if not doctor:
            flash('Doctor no encontrado', 'error')
            return redirect(url_for('clinic.home', view='addAttention'))
        
        # Get selected patient
        patient = Patient.query.filter_by(id=selected_patient_id, is_deleted=False).first()
        if not patient:
            flash('Paciente seleccionado no encontrado', 'error')
            return redirect(url_for('clinic.home', view='addAttention'))
        
        # Create new attention
        new_attention = Attention(
            date=datetime.now(),
            weight=vital_signs_data.get('weight') if vital_signs_data.get('weight') else None,
            height=vital_signs_data.get('height') if vital_signs_data.get('height') else None,
            temperature=vital_signs_data.get('temperature') if vital_signs_data.get('temperature') else None,
            bloodPressure=vital_signs_data.get('bloodPressure'),
            heartRate=vital_signs_data.get('heartRate') if vital_signs_data.get('heartRate') else None,
            oxygenSaturation=vital_signs_data.get('oxygenSaturation') if vital_signs_data.get('oxygenSaturation') else None,
            breathingFrequency=vital_signs_data.get('breathingFrequency') if vital_signs_data.get('breathingFrequency') else None,
            glucose=vital_signs_data.get('glucose') if vital_signs_data.get('glucose') else None,
            hemoglobin=vital_signs_data.get('hemoglobin') if vital_signs_data.get('hemoglobin') else None,
            reasonConsultation=evaluation_data['reasonConsultation'],
            currentIllness=evaluation_data['currentIllness'],
            evolution=evaluation_data['evolution'],
            idPatient=patient.id,
            idDoctor=doctor.id,
            created_by=sessionID,
            updated_by=sessionID
        )
        
        db.session.add(new_attention)
        db.session.commit()
        
        attention_id = new_attention.id
        current_attention_id = attention_id
        
        # Save all related data
        _save_attention_related_data(attention_id, sessionID)
        
        # Clear temporary data
        _clear_temp_attention_data()
        
        flash(f'Atención registrada exitosamente para {patient.firstName} {patient.lastName1}', 'success')
        logger.info(f"Attention completed for patient {patient.id} by doctor {doctor.id}")
        
        return redirect(url_for('clinic.home'))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error completing attention: {str(e)}")
        flash('Error al completar la atención', 'error')
        return redirect(url_for('clinic.home', view='addAttention'))

def _save_attention_related_data(attention_id, session_id):
    """Helper function to save all related attention data"""
    try:
        # Save physical examinations
        for exam_data in physical_exams:
            new_exam = RegionalPhysicalExamination(
                typeExamination=exam_data['typeExamination'],
                examination=exam_data['examination'],
                idAttention=attention_id,
                created_by=session_id,
                updated_by=session_id
            )
            db.session.add(new_exam)
        
        # Save organ system reviews
        for review_data in organ_system_reviews:
            new_review = ReviewOrgansSystem(
                typeReview=review_data['typeReview'],
                review=review_data['review'],
                idAttention=attention_id,
                created_by=session_id,
                updated_by=session_id
            )
            db.session.add(new_review)
        
        # Save diagnostics
        for diagnostic_data in diagnostics:
            new_diagnostic = Diagnostic(
                cie10Code=diagnostic_data['cie10Code'],
                disease=diagnostic_data['disease'],
                observations=diagnostic_data['observations'],
                diagnosticCondition=diagnostic_data['diagnosticCondition'],
                chronology=diagnostic_data['chronology'],
                idAttention=attention_id,
                created_by=session_id,
                updated_by=session_id
            )
            db.session.add(new_diagnostic)
        
        # Save treatments
        for treatment_data in treatments:
            new_treatment = Treatment(
                medicament=treatment_data['medicament'],
                via=treatment_data['via'],
                dosage=treatment_data['dosage'],
                unity=treatment_data['unity'],
                frequency=treatment_data['frequency'],
                indications=treatment_data['indications'],
                warning=treatment_data['warning'],
                idAttention=attention_id,
                created_by=session_id,
                updated_by=session_id
            )
            db.session.add(new_treatment)
        
        # Save histopathologies
        for histo_data in histopathologies:
            new_histo = Histopathology(
                histopathology=histo_data['histopathology'],
                idAttention=attention_id,
                created_by=session_id,
                updated_by=session_id
            )
            db.session.add(new_histo)
        
        # Save imagings
        for imaging_data in imagings:
            new_imaging = Imaging(
                typeImaging=imaging_data['typeImaging'],
                imaging=imaging_data['imaging'],
                idAttention=attention_id,
                created_by=session_id,
                updated_by=session_id
            )
            db.session.add(new_imaging)
        
        # Save laboratories
        for lab_data in laboratories:
            new_lab = Laboratory(
                typeExam=lab_data['typeExam'],
                exam=lab_data['exam'],
                idAttention=attention_id,
                created_by=session_id,
                updated_by=session_id
            )
            db.session.add(new_lab)
        
        db.session.commit()
        logger.info(f"All related data saved for attention {attention_id}")
        
    except Exception as e:
        logger.error(f"Error saving related attention data: {str(e)}")
        raise e

def _clear_temp_attention_data():
    """Clear all temporary attention data"""
    global vital_signs_data, evaluation_data, physical_exams, organ_system_reviews
    global diagnostics, treatments, histopathologies, imagings, laboratories, current_attention_id
    global selected_patient_id
    
    vital_signs_data.clear()
    evaluation_data.clear()
    physical_exams.clear()
    organ_system_reviews.clear()
    diagnostics.clear()
    treatments.clear()
    histopathologies.clear()
    imagings.clear()
    laboratories.clear()
    current_attention_id = None
    selected_patient_id = None

@attention.route('/reset-attention-session', methods=['POST'])
def reset_attention_session():
    """Reset attention session when entering add attention view"""
    _clear_temp_attention_data()
    flash('Nueva sesión de atención iniciada', 'info')
    return redirect(url_for('clinic.home', view='addAttention'))

@attention.route('/clear-temp-attention-data', methods=['POST'])
def clear_temp_attention_data():
    """Clear all temporary attention data"""
    _clear_temp_attention_data()
    flash('Datos temporales de atención limpiados', 'info')
    return redirect(url_for('clinic.home', view='addAttention'))

@attention.route('/get-patients', methods=['GET'])
def get_patients():
    """Get all patients for selection in forms"""
    try:
        patients = Patient.query.filter_by(is_deleted=False).all()
        patient_list = []
        for patient in patients:
            patient_list.append({
                'id': patient.id,
                'name': f"{patient.firstName} {patient.lastName1}",
                'identifierCode': patient.identifierCode
            })
        return jsonify({'patients': patient_list})
    except Exception as e:
        logger.error(f"Error getting patients: {str(e)}")
        return jsonify({'error': 'Error al obtener pacientes'}), 500

@attention.route('/get-doctors', methods=['GET'])
def get_doctors():
    """Get all doctors for selection in forms"""
    try:
        doctors = Doctor.query.filter_by(is_deleted=False).all()
        doctor_list = []
        for doctor in doctors:
            doctor_list.append({
                'id': doctor.id,
                'name': f"Dr. {doctor.firstName} {doctor.lastName1}",
                'speciality': doctor.speciality
            })
        return jsonify({'doctors': doctor_list})
    except Exception as e:
        logger.error(f"Error getting doctors: {str(e)}")
        return jsonify({'error': 'Error al obtener doctores'}), 500
