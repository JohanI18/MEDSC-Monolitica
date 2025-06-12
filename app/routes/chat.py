from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
from models.models_flask import Doctor, ChatMessage
from utils.db import db
import logging

chat = Blueprint('chat', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@chat.route('/chat')
def chat_view():
    """Display chat interface"""
    if 'cedula' not in session:
        return redirect(url_for('clinic.index'))
    
    # Get doctor information from session
    doctor_info = None
    doctors = []
    
    try:
        doctor = Doctor.query.filter_by(
            identifierCode=session['cedula'], 
            is_deleted=False
        ).first()
        
        if doctor:
            # Store doctor ID in session for socket authentication
            session['doctor_id'] = doctor.id
            
            doctor_info = {
                'id': doctor.id,
                'firstName': doctor.firstName,
                'lastName1': doctor.lastName1,
                'speciality': doctor.speciality
            }
            
            # Get all other doctors
            doctors = Doctor.query.filter(
                Doctor.id != doctor.id,
                Doctor.is_deleted == False
            ).all()
    except Exception as e:
        logger.error(f"Error fetching doctor info: {str(e)}")
    
    return render_template('chat.html', 
                          doctor_info=doctor_info, 
                          doctors=doctors,
                          view='chat')

@chat.route('/get-messages/<int:doctor_id>', methods=['GET'])
def get_messages(doctor_id):
    """Get messages between current doctor and selected doctor"""
    if 'doctor_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    current_doctor_id = session['doctor_id']
    
    try:
        # Get messages between the two doctors
        messages = ChatMessage.query.filter(
            ((ChatMessage.sender_id == current_doctor_id) & 
             (ChatMessage.receiver_id == doctor_id)) |
            ((ChatMessage.sender_id == doctor_id) & 
             (ChatMessage.receiver_id == current_doctor_id))
        ).order_by(ChatMessage.timestamp).all()
        
        # Mark messages as read
        unread_messages = ChatMessage.query.filter_by(
            sender_id=doctor_id,
            receiver_id=current_doctor_id,
            is_read=False
        ).all()
        
        for msg in unread_messages:
            msg.is_read = True
        
        db.session.commit()
        
        # Format messages for JSON response
        messages_data = []
        for msg in messages:
            messages_data.append({
                'id': msg.id,
                'sender_id': msg.sender_id,
                'receiver_id': msg.receiver_id,
                'message': msg.message,
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'is_mine': msg.sender_id == current_doctor_id
            })
        
        return jsonify({'messages': messages_data})
    
    except Exception as e:
        logger.error(f"Error getting messages: {str(e)}")
        return jsonify({'error': 'Error al obtener mensajes'}), 500

@chat.route('/send-message', methods=['POST'])
def send_message():
    """Send a message to another doctor (fallback for socket)"""
    if 'doctor_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    sender_id = session['doctor_id']
    receiver_id = request.json.get('receiver_id')
    message_text = request.json.get('message')
    
    if not receiver_id or not message_text:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    try:
        # Save message to database
        new_message = ChatMessage(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message=message_text
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        # Return success response
        return jsonify({
            'id': new_message.id,
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'message': message_text,
            'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'is_mine': True
        })
        
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        return jsonify({'error': 'Error al enviar mensaje'}), 500

@chat.route('/get-unread-counts', methods=['GET'])
def get_unread_counts():
    """Get unread message counts for all doctors"""
    if 'doctor_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    current_doctor_id = session['doctor_id']
    
    try:
        # Get all doctors
        doctors = Doctor.query.filter(
            Doctor.id != current_doctor_id,
            Doctor.is_deleted == False
        ).all()
        
        # Get unread counts for each doctor
        unread_counts = {}
        for doctor in doctors:
            count = ChatMessage.query.filter_by(
                sender_id=doctor.id,
                receiver_id=current_doctor_id,
                is_read=False
            ).count()
            
            unread_counts[str(doctor.id)] = count
        
        return jsonify({'unread_counts': unread_counts})
        
    except Exception as e:
        logger.error(f"Error getting unread counts: {str(e)}")
        return jsonify({'error': 'Error al obtener conteos de mensajes'}), 500

