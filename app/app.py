from flask import Flask
from flask_socketio import SocketIO
from utils.db import db
from config import DATABASE_CONNECTION_URI, SECRET_KEY
from routes.clinic import clinic
from routes.login import login
from routes.patients import patients
from routes.attention import attention
from routes.chat import chat  # Importar el nuevo blueprint

# Crear instancia de SocketIO
socketio = SocketIO()

def create_app():
    app = Flask(__name__)

    app.secret_key = SECRET_KEY
    
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # Register blueprints
    app.register_blueprint(clinic)
    app.register_blueprint(login)
    app.register_blueprint(patients)
    app.register_blueprint(attention)
    app.register_blueprint(chat)  # Registrar el nuevo blueprint

    return app

# Agregar esta función para ejecutar la aplicación con SocketIO
def run_app():
    from app import socketio, app
    socketio.run(app, debug=True, host='0.0.0.0')

if __name__ == '__main__':
    run_app()
