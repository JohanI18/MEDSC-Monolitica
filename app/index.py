from app import create_app, socketio
from models.models_flask import ChatMessage, Doctor
from utils.db import db
from flask import session
from flask_socketio import emit, join_room, leave_room
import logging

app = create_app()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@socketio.on('connect')
def handle_connect():
    if 'doctor_id' in session:
        doctor_id = session['doctor_id']
        join_room(f"doctor_{doctor_id}")
        logger.info(f"Doctor {doctor_id} connected")
        
        # Notify others that doctor is online
        emit('doctor_status', {
            'doctor_id': doctor_id,
            'status': 'online'
        }, broadcast=True, include_self=False)

@socketio.on('disconnect')
def handle_disconnect():
    if 'doctor_id' in session:
        doctor_id = session['doctor_id']
        leave_room(f"doctor_{doctor_id}")
        logger.info(f"Doctor {doctor_id} disconnected")
        
        # Notify others that doctor is offline
        emit('doctor_status', {
            'doctor_id': doctor_id,
            'status': 'offline'
        }, broadcast=True, include_self=False)

@socketio.on('send_message')
def handle_message(data):
    if 'doctor_id' not in session:
        return
    
    sender_id = session['doctor_id']
    receiver_id = data.get('receiver_id')
    message_text = data.get('message')
    
    if not receiver_id or not message_text:
        return
    
    try:
        # Save message to database
        new_message = ChatMessage(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message=message_text
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        # Get sender info
        sender = Doctor.query.get(sender_id)
        
        # Send to receiver's room
        emit('new_message', {
            'id': new_message.id,
            'sender_id': sender_id,
            'sender_name': f"{sender.firstName} {sender.lastName1}",
            'message': message_text,
            'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'is_mine': False
        }, room=f"doctor_{receiver_id}")
        
        # Send confirmation to sender
        emit('message_sent', {
            'id': new_message.id,
            'receiver_id': receiver_id,
            'message': message_text,
            'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
        
        logger.info(f"Message sent from {sender_id} to {receiver_id}")
        
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        emit('message_error', {'error': 'Error al enviar mensaje'})

if __name__ == '__main__':
    app.run(debug=True)