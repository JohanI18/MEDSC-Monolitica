from flask import Flask
from models.models_flask import db, Doctor, Credentials
import bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://usuario:pass123@127.0.0.1:3306/clinic"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def create_hashed_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

with app.app_context():
    try:
        # Crear doctor
        doctor = Doctor(
            identifierCode="DOC002",
            firstName="Lucía",
            middleName="Fernanda",
            lastName1="Mora",
            lastName2="Ramírez",
            phoneNumber="0999999999",
            address="Calle 100 #50-25",
            gender="Femenino",
            sex="Femenino",
            speciality="Neurología",
            email="lucia.mora@example.com",
            created_by="admin",
            updated_by="admin"
        )
        db.session.add(doctor)
        db.session.commit()

        # Crear credenciales
        credentials = Credentials(
            identifierCode="DOC002",
            password=create_hashed_password("clave_segura"),  # Asegúrate de hashear en producción
            idUser=doctor.id,
            userType="doctor",
            created_by="admin",
            updated_by="admin"
        )
        db.session.add(credentials)
        db.session.commit()

        print("✅ Doctor y credenciales creados correctamente.")
    
    except Exception as e:
        db.session.rollback()
        print("❌ Error al insertar:", str(e))
