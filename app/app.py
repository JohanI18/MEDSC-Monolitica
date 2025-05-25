from flask import Flask
from utils.db import db
from config import DATABASE_CONNECTION_URI, SECRET_KEY
from routes.clinic import clinic
from routes.login import login
from routes.patients import patients

def create_app():
    app = Flask(__name__)

    app.secret_key = SECRET_KEY
    
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(clinic)
    app.register_blueprint(login)
    app.register_blueprint(patients)

    return app