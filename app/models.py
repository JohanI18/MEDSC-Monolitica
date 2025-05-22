# models.py
from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    String,
    Text,
    Enum as SA_Enum, # Renombrado para evitar confusión con el tipo Enum estándar de Python
    Boolean,
    DateTime,
    Date,
    Index,
    func,
    ForeignKey,
    UniqueConstraint # Importar UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship as sa_relationship

Base = declarative_base()


# --- TABLAS PRINCIPALES ---

class Patient(Base):
    __tablename__ = "patients"
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci"
    }

    id              = Column(Integer, primary_key=True, autoincrement=True)
    identifierType  = Column(
                        SA_Enum(
                          'Cedula',
                          'Pasaporte',
                          'GeneratedIdentifier',
                          name='patients_identifierType_enum', # Nombre explícito para el tipo ENUM en la BD
                          native_enum=False, validate_strings=True
                        ),
                        nullable=False
                      )
    identifierCode  = Column(String(255, collation="utf8mb4_general_ci"), nullable=False, unique=True, index=True)
    firstName       = Column(String(255, collation="utf8mb4_general_ci"), nullable=False)
    middleName      = Column(String(255, collation="utf8mb4_general_ci"), nullable=True)
    lastName1       = Column(String(255, collation="utf8mb4_general_ci"), nullable=False)
    lastName2       = Column(String(255, collation="utf8mb4_general_ci"), nullable=True)
    nationality     = Column(String(255, collation="utf8mb4_general_ci"), nullable=True)
    address         = Column(Text(collation="utf8mb4_general_ci"), nullable=False)
    phoneNumber     = Column(String(255, collation="utf8mb4_general_ci"), nullable=True)
    birthdate       = Column(Date, nullable=False)
    gender          = Column(
                        SA_Enum(
                          'Masculino',
                          'Femenino',
                          'No Binario',
                          'Otro',
                          'Prefiero no decir',
                          name='patients_gender_enum',
                          native_enum=False, validate_strings=True
                        ),
                        nullable=True
                      )
    sex             = Column(
                        SA_Enum(
                          'Masculino',
                          'Femenino',
                          'Prefiero no decir',
                          name='patients_sex_enum',
                          native_enum=False, validate_strings=True
                        ),
                        nullable=True
                      )
    civilStatus     = Column(
                        SA_Enum(
                          'Soltero/a',
                          'UniónDeHecho',
                          'Casado/a',
                          'Divorciado/a',
                          'Viudo/a',
                          name='patients_civilStatus_enum',
                          native_enum=False, validate_strings=True
                        ),
                        nullable=True
                      )
    job             = Column(Text(collation="utf8mb4_general_ci"), nullable=True)
    bloodType       = Column(
                        SA_Enum(
                          'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-',
                          name='patients_bloodType_enum',
                          native_enum=False, validate_strings=True
                        ),
                        nullable=True
                      )
    email           = Column(Text(collation="utf8mb4_general_ci"), nullable=True) # Considerar String(255) si tiene un límite
    created_at      = Column(DateTime, server_default=func.now(), nullable=False)
    created_by      = Column(String(255), nullable=False)
    updated_at      = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by      = Column(String(255), nullable=False)
    is_deleted      = Column(Boolean, default=False, index=True, nullable=False) # Añadido index

    # Relaciones
    attentions = sa_relationship("Attention", back_populates="patient") # Ajustar cascade según la política de BD
    allergies = sa_relationship("Allergy", back_populates="patient", cascade="all, delete-orphan")
    emergency_contacts = sa_relationship("EmergencyContact", back_populates="patient", cascade="all, delete-orphan")
    family_backgrounds = sa_relationship("FamilyBackground", back_populates="patient", cascade="all, delete-orphan")
    pre_existing_conditions = sa_relationship("PreExistingCondition", back_populates="patient", cascade="all, delete-orphan")

class Doctor(Base):
    __tablename__ = "doctor"
    __table_args__ = {
        "mysql_charset": "utf8mb4", # Consistencia con otras tablas
        "mysql_collate": "utf8mb4_0900_ai_ci" # Consistencia con otras tablas
    }

    id             = Column(Integer, primary_key=True, autoincrement=True)
    identifierCode = Column(String(255), unique=True, nullable=False, index=True)
    firstName      = Column(String(255), nullable=False)
    middleName     = Column(String(255), nullable=True) # Ya estaba nullable=True
    lastName1      = Column(String(255), nullable=False)
    lastName2      = Column(String(255), nullable=True) # Ya estaba nullable=True
    phoneNumber    = Column(String(255), nullable=False)
    address        = Column(Text, nullable=False)
    gender         = Column(
        SA_Enum('Masculino', 'Femenino', 'No Binario', 'Otro', 'Prefiero no decir', name='doctor_gender_enum', native_enum=False, validate_strings=True),
        nullable=False
    )
    sex            = Column(
        SA_Enum('Masculino', 'Femenino', 'Prefiero no decir', name='doctor_sex_enum', native_enum=False, validate_strings=True),
        nullable=False
    )
    speciality     = Column(String(255), nullable=False)
    email          = Column(String(255), nullable=False, unique=True) # unique=True es bueno aquí
    created_at      = Column(DateTime, server_default=func.now(), nullable=False)
    created_by      = Column(String(255), nullable=False)
    updated_at      = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by      = Column(String(255), nullable=False)
    is_deleted      = Column(Boolean, default=False, index=True, nullable=False) # Añadido index

    # Relaciones
    attentions = sa_relationship("Attention", back_populates="doctor")
    credentials = sa_relationship("Credentials", back_populates="doctor", foreign_keys="[Credentials.idUser]",
                                  primaryjoin="and_(Doctor.id == Credentials.idUser, Credentials.userType == 'doctor')")

class Attention(Base):
    __tablename__ = "attention"
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_0900_ai_ci"
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False, index=True) # Añadido index a date
    weight = Column(Numeric(6, 2), nullable=True)
    height = Column(Numeric(5, 2), nullable=True)
    temperature = Column(Numeric(4, 1), nullable=True)
    bloodPressure = Column(String(20), nullable=True) # CAMBIADO: de Integer a String(20)
    heartRate = Column(Integer, nullable=True)
    oxygenSaturation = Column(Integer, nullable=True) # Podría ser Numeric(3,0) o Numeric(5,2) si es %
    breathingFrequency = Column(Integer, nullable=True)
    glucose = Column(Numeric(5, 1), nullable=True)
    hemoglobin = Column(Numeric(4, 1), nullable=True)
    reasonConsultation = Column(String(255), nullable=False)
    currentIllness = Column(String(255), nullable=False)
    evolution = Column(String(255), nullable=False) # Considerar Text si puede ser largo

    # CAMBIADO: idClinicHistory -> idPatient
    idPatient = Column(Integer, ForeignKey('patients.id'), nullable=False, index=True)
    idDoctor = Column(Integer, ForeignKey('doctor.id'), nullable=False, index=True)

    created_at      = Column(DateTime, server_default=func.now(), nullable=False)
    created_by      = Column(String(255), nullable=False)
    updated_at      = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by      = Column(String(255), nullable=False)
    is_deleted      = Column(Boolean, default=False, index=True, nullable=False) # Añadido index

    # Relaciones
    patient = sa_relationship("Patient", back_populates="attentions")
    doctor = sa_relationship("Doctor", back_populates="attentions")

    diagnostics = sa_relationship("Diagnostic", back_populates="attention", cascade="all, delete-orphan")
    histopathologies = sa_relationship("Histopathology", back_populates="attention", cascade="all, delete-orphan")
    imagings = sa_relationship("Imaging", back_populates="attention", cascade="all, delete-orphan")
    laboratories = sa_relationship("Laboratory", back_populates="attention", cascade="all, delete-orphan")
    regional_physical_examinations = sa_relationship("RegionalPhysicalExamination", back_populates="attention", cascade="all, delete-orphan")
    review_organs_systems = sa_relationship("ReviewOrgansSystem", back_populates="attention", cascade="all, delete-orphan")
    treatments = sa_relationship("Treatment", back_populates="attention", cascade="all, delete-orphan")


# --- TABLAS DEPENDIENTES ---

class Allergy(Base):
    __tablename__ = "allergies"
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci"
    }

    id               = Column(Integer, primary_key=True, autoincrement=True)
    allergies        = Column(Text(collation="utf8mb4_general_ci"), nullable=False)
    # CAMBIADO: idClinicHistory -> idPatient
    idPatient        = Column(Integer, ForeignKey('patients.id'), nullable=False, index=True)

    created_at      = Column(DateTime, server_default=func.now(), nullable=False)
    created_by      = Column(String(255), nullable=False)
    updated_at      = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by      = Column(String(255), nullable=False)
    is_deleted      = Column(Boolean, default=False, index=True, nullable=False) # Añadido index

    # Relación
    patient = sa_relationship("Patient", back_populates="allergies")

class Credentials(Base):
    __tablename__ = "credentials"
    __table_args__ = (
        UniqueConstraint('identifierCode', 'userType', name='uq_identifierCode_userType'),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_0900_ai_ci"}
    )

    id               = Column(Integer, primary_key=True, autoincrement=True)
    identifierCode   = Column(String(255), nullable=False, index=True) # No es FK directa aquí para simplicidad
    password         = Column(String(255), nullable=False) # ¡Hashear en la aplicación!
    
    # NUEVAS COLUMNAS para vincular a Patient o Doctor
    idUser           = Column(Integer, nullable=False, index=True) # Referencia a Patient.id o Doctor.id
    userType         = Column(SA_Enum('doctor', 'patient', name='credentials_userType_enum', native_enum=False, validate_strings=True), nullable=False)

    created_at      = Column(DateTime, server_default=func.now(), nullable=False)
    created_by      = Column(String(255), nullable=False)
    updated_at      = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by      = Column(String(255), nullable=False)
    is_deleted      = Column(Boolean, default=False, index=True, nullable=False) # Añadido index

    # Relaciones polimórficas (una forma de implementarlas)
    # Se necesita una lógica adicional en la aplicación para determinar a qué tabla apunta idUser
    # O usar una solución más avanzada de SQLAlchemy para relaciones polimórficas si se desea cargar el objeto Doctor/Patient directamente.
    # Por simplicidad, aquí solo definimos la relación básica con Doctor (si se usa principalmente para ellos)
    # Opcional: Si solo fuera para doctores:
    doctor = sa_relationship("Doctor", foreign_keys=[idUser],
                             primaryjoin="and_(Doctor.id == Credentials.idUser, Credentials.userType == 'doctor')",
                             back_populates="credentials", uselist=False) # Asumiendo una credencial por doctor
    # Si también fuera para pacientes, se necesitaría otra relación o una configuración polimórfica más compleja.

class Diagnostic(Base):
    __tablename__ = "diagnostic"
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci"
    }

    id                     = Column(Integer, primary_key=True, autoincrement=True)
    cie10Code              = Column(String(255, collation="utf8mb4_general_ci"), nullable=False, index=True) # Añadido index
    disease                = Column(String(255, collation="utf8mb4_general_ci"), nullable=False)
    observations           = Column(Text(collation="utf8mb4_general_ci"), nullable=False) # Cambiado a Text
    diagnosticCondition    = Column(String(255, collation="utf8mb4_general_ci"), nullable=False)
    chronology             = Column(String(255, collation="utf8mb4_general_ci"), nullable=False)
    idAttention            = Column(Integer, ForeignKey('attention.id'), nullable=False, index=True)

    created_at      = Column(DateTime, server_default=func.now(), nullable=False)
    created_by      = Column(String(255), nullable=False)
    updated_at      = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by      = Column(String(255), nullable=False)
    is_deleted      = Column(Boolean, default=False, index=True, nullable=False) # Añadido index

    attention = sa_relationship("Attention", back_populates="diagnostics")

class EmergencyContact(Base):
    __tablename__ = "emergencyContact"
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci"
    }

    id               = Column(Integer, primary_key=True, autoincrement=True)
    firstName        = Column(String(255, collation="utf8mb4_general_ci"), nullable=False)
    lastName         = Column(String(255, collation="utf8mb4_general_ci"), nullable=False)
    address          = Column(Text(collation="utf8mb4_general_ci"), nullable=False)
    relationship     = Column(String(255, collation="utf8mb4_general_ci"), nullable=False)
    phoneNumber1     = Column(String(255, collation="utf8mb4_general_ci"), nullable=False)
    phoneNumber2     = Column(String(255, collation="utf8mb4_general_ci"), nullable=True)
    # CAMBIADO: idClinicHistory -> idPatient
    idPatient        = Column(Integer, ForeignKey('patients.id'), nullable=False, index=True)

    created_at      = Column(DateTime, server_default=func.now(), nullable=False)
    created_by      = Column(String(255), nullable=False)
    updated_at      = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by      = Column(String(255), nullable=False)
    is_deleted      = Column(Boolean, default=False, index=True, nullable=False) # Añadido index

    patient = sa_relationship("Patient", back_populates="emergency_contacts")

class FamilyBackground(Base):
    __tablename__ = "familyBackground"
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci"
    }

    id                   = Column(Integer, primary_key=True, autoincrement=True)
    familyBackground     = Column(Text(collation="utf8mb4_general_ci"), nullable=False)
    time                 = Column(Date, nullable=False)
    degreeRelationship   = Column(SA_Enum('1', '2', '3', '4', name='familyBackground_degreeRelationship_enum', native_enum=False, validate_strings=True), nullable=False)
    # CAMBIADO: idClinicHistory -> idPatient
    idPatient            = Column(Integer, ForeignKey('patients.id'), nullable=False, index=True)

    created_at      = Column(DateTime, server_default=func.now(), nullable=False)
    created_by      = Column(String(255), nullable=False)
    updated_at      = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by      = Column(String(255), nullable=False)
    is_deleted      = Column(Boolean, default=False, index=True, nullable=False) # Añadido index

    patient = sa_relationship("Patient", back_populates="family_backgrounds")

class Histopathology(Base):
    __tablename__ = "histopathology"
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci"
    }

    id                = Column(Integer, primary_key=True, autoincrement=True)
    histopathology    = Column(Text(collation="utf8mb4_general_ci"), nullable=False)
    idAttention       = Column(Integer, ForeignKey('attention.id'), nullable=False, index=True)

    created_at      = Column(DateTime, server_default=func.now(), nullable=False)
    created_by      = Column(String(255), nullable=False)
    updated_at      = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by      = Column(String(255), nullable=False)
    is_deleted      = Column(Boolean, default=False, index=True, nullable=False) # Añadido index

    attention = sa_relationship("Attention", back_populates="histopathologies")

class Imaging(Base):
    __tablename__ = "imaging"
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci"
    }

    id             = Column(Integer, primary_key=True, autoincrement=True)
    typeImaging    = Column(String(255, collation="utf8mb4_general_ci"), nullable=False)
    imaging        = Column(Text(collation="utf8mb4_general_ci"), nullable=False)
    idAttention    = Column(Integer, ForeignKey('attention.id'), nullable=False, index=True)

    created_at      = Column(DateTime, server_default=func.now(), nullable=False)
    created_by      = Column(String(255), nullable=False)
    updated_at      = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by      = Column(String(255), nullable=False)
    is_deleted      = Column(Boolean, default=False, index=True, nullable=False) # Añadido index

    attention = sa_relationship("Attention", back_populates="imagings")

class Laboratory(Base):
    __tablename__ = "laboratory"
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci"
    }

    id            = Column(Integer, primary_key=True, autoincrement=True)
    typeExam      = Column(String(255, collation="utf8mb4_general_ci"), nullable=False)
    exam          = Column(Text(collation="utf8mb4_general_ci"), nullable=False)
    idAttention   = Column(Integer, ForeignKey('attention.id'), nullable=False, index=True)

    created_at      = Column(DateTime, server_default=func.now(), nullable=False)
    created_by      = Column(String(255), nullable=False)
    updated_at      = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by      = Column(String(255), nullable=False)
    is_deleted      = Column(Boolean, default=False, index=True, nullable=False) # Añadido index

    attention = sa_relationship("Attention", back_populates="laboratories")

class PreExistingCondition(Base):
    __tablename__ = "preExistingCondition"
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci"
    }

    id               = Column(Integer, primary_key=True, autoincrement=True)
    diseaseName      = Column(String(255, collation="utf8mb4_general_ci"), nullable=False)
    time             = Column(Date, nullable=False)
    medicament       = Column(String(255, collation="utf8mb4_general_ci"), nullable=True)
    treatment        = Column(String(255, collation="utf8mb4_general_ci"), nullable=True)
    # CAMBIADO: idClinicHistory -> idPatient
    idPatient        = Column(Integer, ForeignKey('patients.id'), nullable=False, index=True)

    created_at      = Column(DateTime, server_default=func.now(), nullable=False)
    created_by      = Column(String(255), nullable=False)
    updated_at      = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by      = Column(String(255), nullable=False)
    is_deleted      = Column(Boolean, default=False, index=True, nullable=False) # Añadido index

    patient = sa_relationship("Patient", back_populates="pre_existing_conditions")

class RegionalPhysicalExamination(Base):
    __tablename__ = "regionalPhysicalExamination"
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci"
    }

    id               = Column(Integer, primary_key=True, autoincrement=True)
    typeExamination  = Column(String(255, collation="utf8mb4_general_ci"), nullable=False)
    examination      = Column(Text(collation="utf8mb4_general_ci"), nullable=False)
    idAttention      = Column(Integer, ForeignKey('attention.id'), nullable=False, index=True)

    created_at      = Column(DateTime, server_default=func.now(), nullable=False)
    created_by      = Column(String(255), nullable=False)
    updated_at      = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by      = Column(String(255), nullable=False)
    is_deleted      = Column(Boolean, default=False, index=True, nullable=False) # Añadido index

    attention = sa_relationship("Attention", back_populates="regional_physical_examinations")

class ReviewOrgansSystem(Base): # Nombre de clase singular
    __tablename__ = "reviewOrgansSystems" # Nombre de tabla plural
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci"
    }

    id            = Column(Integer, primary_key=True, autoincrement=True)
    typeReview    = Column(String(255, collation="utf8mb4_general_ci"), nullable=False)
    review        = Column(Text(collation="utf8mb4_general_ci"), nullable=False)
    idAttention   = Column(Integer, ForeignKey('attention.id'), nullable=False, index=True)

    created_at      = Column(DateTime, server_default=func.now(), nullable=False)
    created_by      = Column(String(255), nullable=False)
    updated_at      = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by      = Column(String(255), nullable=False)
    is_deleted      = Column(Boolean, default=False, index=True, nullable=False) # Añadido index

    attention = sa_relationship("Attention", back_populates="review_organs_systems")

class Treatment(Base):
    __tablename__ = "treatment"
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci"
    }

    id           = Column(Integer, primary_key=True, autoincrement=True)
    medicament   = Column(String(255, collation="utf8mb4_general_ci"), nullable=False)
    via          = Column(String(255, collation="utf8mb4_general_ci"), nullable=False)
    dosage       = Column(String(255, collation="utf8mb4_general_ci"), nullable=False)
    unity        = Column(String(255, collation="utf8mb4_general_ci"), nullable=False)
    frequency    = Column(Text(collation="utf8mb4_general_ci"), nullable=False)
    indications  = Column(Text(collation="utf8mb4_general_ci"), nullable=False)
    warning      = Column(Text(collation="utf8mb4_general_ci"), nullable=True) # Confirmado nullable=True
    idAttention  = Column(Integer, ForeignKey('attention.id'), nullable=False, index=True)

    created_at      = Column(DateTime, server_default=func.now(), nullable=False)
    created_by      = Column(String(255), nullable=False)
    updated_at      = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by      = Column(String(255), nullable=False)
    is_deleted      = Column(Boolean, default=False, index=True, nullable=False) # Añadido index

    attention = sa_relationship("Attention", back_populates="treatments")

# --- ÍNDICES ADICIONALES (Ejemplos, algunos ya están por index=True en columnas) ---
# Estos se crean automáticamente si index=True está en la columna.
# Si necesitas índices compuestos, los defines aquí.

Index('idx_patients_name', Patient.firstName, Patient.lastName1, Patient.lastName2)
Index('idx_doctor_name', Doctor.firstName, Doctor.lastName1, Doctor.lastName2)

# Nota sobre cascade en Patient.attentions:
# Lo he dejado como estaba (`cascade="all, delete-orphan"`). Si tu FK en la base de datos
# para `attention.idPatient` -> `patients.id` es `ON DELETE RESTRICT`,
# entonces un borrado de un `Patient` que tenga `Attention`s fallará a nivel de base de datos
# antes de que SQLAlchemy intente el borrado en cascada. Si la FK es `ON DELETE CASCADE`,
# entonces la base de datos y SQLAlchemy trabajarán en conjunto. Ajusta el `cascade`
# o la política `ON DELETE` de la FK para que sean consistentes con tu lógica deseada.
# Para las demás relaciones "hijas" de Patient, he mantenido `cascade="all, delete-orphan"`
# asumiendo que esos elementos sí deben borrarse si el paciente se borra.
# Similar para Attention y sus tablas hijas.