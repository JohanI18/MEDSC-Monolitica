-- Usa la base de datos 'clinic'
USE clinic;

-- Desactivar temporalmente las verificaciones de claves foráneas para inserciones iniciales si es necesario
-- SET FOREIGN_KEY_CHECKS=0;

-- Asegurarse de que las operaciones se confirman
-- START TRANSACTION; -- Opcional, si quieres ejecutar todo como una transacción

-- ####################################################################
-- # CREATE (INSERT) Operaciones                                      #
-- ####################################################################

-- --------------------------------------------------------
-- Insertar Doctores
-- --------------------------------------------------------
INSERT INTO doctor (identifierCode, firstName, middleName, lastName1, lastName2, phoneNumber, address, gender, sex, speciality, email, created_by, updated_by) VALUES
('DOC001', 'Carlos', 'Alberto', 'Sanchez', 'Perez', '123456789', 'Av. Siempre Viva 123, Ciudad Capital', 'Masculino', 'Masculino', 'Cardiología', 'carlos.sanchez@example.com', 'admin_script', 'admin_script'),
('DOC002', 'Ana', 'Lucia', 'Gomez', 'Lopez', '987654321', 'Calle Falsa 456, Pueblo Nuevo', 'Femenino', 'Femenino', 'Pediatría', 'ana.gomez@example.com', 'admin_script', 'admin_script');

-- --------------------------------------------------------
-- Insertar Credenciales para Doctores (Ejemplo)
-- ¡EN PRODUCCIÓN, USA HASHES PARA LAS CONTRASEÑAS!
-- --------------------------------------------------------
-- Suponiendo que el constraint credentials_ibfk_1 está activo y relaciona con doctor.identifierCode
INSERT INTO credentials (identifierCode, password, created_by, updated_by) VALUES
('DOC001', 'password123', 'admin_script', 'admin_script'), -- Contraseña para Dr. Sanchez
('DOC002', 'securepass', 'admin_script', 'admin_script'); -- Contraseña para Dra. Gomez

-- --------------------------------------------------------
-- Insertar Pacientes
-- --------------------------------------------------------
INSERT INTO patients (identifierType, identifierCode, firstName, middleName, lastName1, lastName2, nationality, address, phoneNumber, birthdate, gender, sex, civilStatus, job, bloodType, email, created_by, updated_by) VALUES
('Cedula', '1234567890', 'Juan', 'Carlos', 'Perez', 'Gomez', 'Ecuatoriana', 'Calle Sol 123, Quito', '0991234567', '1985-06-15', 'Masculino', 'Masculino', 'Casado/a', 'Ingeniero de Sistemas', 'O+', 'juan.perez@example.com', 'admin_script', 'admin_script'),
('Pasaporte', 'AB123456', 'Maria', 'Elena', 'Lopez', 'Vega', 'Colombiana', 'Av. Luna 456, Guayaquil', '0987654321', '1992-11-20', 'Femenino', 'Femenino', 'Soltero/a', 'Diseñadora Gráfica', 'A+', 'maria.lopez@example.com', 'admin_script', 'admin_script');

-- Asignar IDs de pacientes y doctores a variables para facilitar su uso (opcional, útil si se ejecuta en un entorno que lo permita)
-- SET @patient1_id = LAST_INSERT_ID(); -- Si se insertó el segundo paciente
-- SET @patient1_id = (SELECT id FROM patients WHERE identifierCode = '1234567890');
-- SET @patient2_id = (SELECT id FROM patients WHERE identifierCode = 'AB123456');
-- SET @doctor1_id = (SELECT id FROM doctor WHERE identifierCode = 'DOC001');
-- SET @doctor2_id = (SELECT id FROM doctor WHERE identifierCode = 'DOC002');
-- Para este script, asumiremos que los IDs son 1 y 2 respectivamente para simplificar.

-- --------------------------------------------------------
-- Insertar Alergias para Paciente 1 (Juan Perez, id=1)
-- --------------------------------------------------------
INSERT INTO allergies (allergies, idClinicHistory, created_by, updated_by) VALUES
('Polen, Penicilina', 1, 'admin_script', 'admin_script');

-- --------------------------------------------------------
-- Insertar Contacto de Emergencia para Paciente 1 (Juan Perez, id=1)
-- --------------------------------------------------------
INSERT INTO emergencyContact (firstName, lastName, address, relationship, phoneNumber1, phoneNumber2, idClinicHistory, created_by, updated_by) VALUES
('Luisa', 'Gomez', 'Calle Sol 123, Quito (misma que paciente)', 'Esposa', '0997654321', '022345678', 1, 'admin_script', 'admin_script');

-- --------------------------------------------------------
-- Insertar Antecedentes Familiares para Paciente 1 (Juan Perez, id=1)
-- --------------------------------------------------------
INSERT INTO familyBackground (familyBackground, time, degreeRelationship, idClinicHistory, created_by, updated_by) VALUES
('Padre con Hipertensión, Madre con Diabetes tipo 2', '2000-01-01', '1', 1, 'admin_script', 'admin_script');

-- --------------------------------------------------------
-- Insertar Condiciones Preexistentes para Paciente 1 (Juan Perez, id=1)
-- --------------------------------------------------------
INSERT INTO preExistingCondition (diseaseName, time, medicament, treatment, idClinicHistory, created_by, updated_by) VALUES
('Asma leve intermitente', '2010-05-01', 'Salbutamol inhalador', 'Uso según necesidad', 1, 'admin_script', 'admin_script');

-- --------------------------------------------------------
-- Insertar Atención Médica para Paciente 1 (Juan Perez, id=1) con Doctor 1 (Carlos Sanchez, id=1)
-- --------------------------------------------------------
INSERT INTO attention (date, weight, height, temperature, bloodPressure, heartRate, oxygenSaturation, breathingFrequency, glucose, hemoglobin, reasonConsultation, currentIllness, evolution, idClinicHistory, idDoctor, created_by, updated_by) VALUES
(NOW(), 75, 170, 37, 120, 80, 98, 16, 90, 15, 'Chequeo general anual', 'Paciente asintomático, refiere buen estado general.', 'Estable, sin hallazgos patológicos.', 1, 1, 'admin_script', 'admin_script');
SET @attention1_id = LAST_INSERT_ID();

-- --------------------------------------------------------
-- Insertar Atención Médica para Paciente 2 (Maria Lopez, id=2) con Doctor 2 (Ana Gomez, id=2)
-- --------------------------------------------------------
INSERT INTO attention (date, weight, height, temperature, bloodPressure, heartRate, oxygenSaturation, breathingFrequency, reasonConsultation, currentIllness, evolution, idClinicHistory, idDoctor, created_by, updated_by) VALUES
(NOW() - INTERVAL 1 DAY, 65, 165, 38, 130, 85, 97, 18, 'Dolor de cabeza y malestar general', 'Paciente refiere cefalea intensa desde hace 2 días, acompañada de fatiga.', 'En evaluación.', 2, 2, 'admin_script', 'admin_script');
SET @attention2_id = LAST_INSERT_ID();

-- --------------------------------------------------------
-- Insertar Diagnóstico para Atención 1 (@attention1_id)
-- --------------------------------------------------------
INSERT INTO diagnostic (cie10Code, disease, observations, diagnosticCondition, chronology, idAttention, created_by, updated_by) VALUES
('Z00.0', 'Examen médico general', 'Paciente sano, control de rutina.', 'Definitivo', 'No aplica', @attention1_id, 'admin_script', 'admin_script');

-- --------------------------------------------------------
-- Insertar Diagnóstico para Atención 2 (@attention2_id)
-- --------------------------------------------------------
INSERT INTO diagnostic (cie10Code, disease, observations, diagnosticCondition, chronology, idAttention, created_by, updated_by) VALUES
('R51', 'Cefalea', 'Cefalea tensional probable, descartar otras causas.', 'Presuntivo', 'Aguda', @attention2_id, 'admin_script', 'admin_script');

-- --------------------------------------------------------
-- Insertar Tratamiento para Atención 2 (@attention2_id)
-- --------------------------------------------------------
INSERT INTO treatment (medicament, via, dosage, unity, frequency, indications, warning, idAttention, created_by, updated_by) VALUES
('Ibuprofeno', 'Oral', '400', 'mg', 'Cada 8 horas por 3 días', 'Tomar con alimentos. Si el dolor persiste, reevaluar.', 'No exceder dosis. Alerta a signos de alarma.', @attention2_id, 'admin_script', 'admin_script');

-- --------------------------------------------------------
-- Insertar Examen de Laboratorio para Atención 2 (@attention2_id)
-- --------------------------------------------------------
INSERT INTO laboratory (typeExam, exam, idAttention, created_by, updated_by) VALUES
('Hematología Completa', 'Resultados: Leucocitos 8500/mm³, Hematocrito 42%, Plaquetas 250000/mm³. Todo dentro de rangos normales.', @attention2_id, 'admin_script', 'admin_script');

-- --------------------------------------------------------
-- Insertar Examen Físico Regional para Atención 1 (@attention1_id)
-- --------------------------------------------------------
INSERT INTO regionalPhysicalExamination (typeExamination, examination, idAttention, created_by, updated_by) VALUES
('Cabeza y Cuello', 'Normocéfalo, pupilas isocóricas reactivas a la luz, cuello móvil sin adenopatías.', @attention1_id, 'admin_script', 'admin_script'),
('Tórax', 'Murmullo vesicular conservado bilateralmente, no soplos cardíacos.', @attention1_id, 'admin_script', 'admin_script');

-- --------------------------------------------------------
-- Insertar Revisión de Órganos y Sistemas para Atención 1 (@attention1_id)
-- --------------------------------------------------------
INSERT INTO reviewOrgansSystems (typeReview, review, idAttention, created_by, updated_by) VALUES
('Sistema Cardiovascular', 'Ritmo regular, sin soplos ni galopes. Pulsos periféricos presentes y simétricos.', @attention1_id, 'admin_script', 'admin_script'),
('Sistema Respiratorio', 'Campos pulmonares bien ventilados, sin ruidos agregados.', @attention1_id, 'admin_script', 'admin_script');

-- --------------------------------------------------------
-- Insertar Estudio de Imagen para Atención 2 (@attention2_id)
-- --------------------------------------------------------
INSERT INTO imaging (typeImaging, imaging, idAttention, created_by, updated_by) VALUES
('Radiografía de Senos Paranasales', 'No se observan signos de sinusitis aguda. Velamiento leve del seno maxilar izquierdo, a correlacionar con clínica.', @attention2_id, 'admin_script', 'admin_script');


-- ####################################################################
-- # READ (SELECT) Operaciones                                        #
-- ####################################################################

-- Leer todos los pacientes no borrados
SELECT * FROM patients WHERE is_deleted = FALSE;

-- Leer un paciente específico por ID (suponiendo id=1)
SELECT * FROM patients WHERE id = 1 AND is_deleted = FALSE;

-- Leer todos los doctores no borrados
SELECT * FROM doctor WHERE is_deleted = FALSE;

-- Leer un doctor específico por identifierCode
SELECT * FROM doctor WHERE identifierCode = 'DOC001' AND is_deleted = FALSE;

-- Leer todas las atenciones de un paciente específico (suponiendo patient_id=1) con información del doctor
SELECT
    a.id AS attention_id,
    a.date,
    a.reasonConsultation,
    p.firstName AS patient_firstName,
    p.lastName1 AS patient_lastName1,
    d.firstName AS doctor_firstName,
    d.lastName1 AS doctor_lastName1,
    d.speciality
FROM attention a
JOIN patients p ON a.idClinicHistory = p.id
JOIN doctor d ON a.idDoctor = d.id
WHERE a.idClinicHistory = 1 AND a.is_deleted = FALSE AND p.is_deleted = FALSE AND d.is_deleted = FALSE
ORDER BY a.date DESC;

-- Leer los diagnósticos y tratamientos de una atención específica (suponiendo attention_id=@attention2_id)
SELECT
    diag.cie10Code,
    diag.disease AS diagnostic_disease,
    diag.observations AS diagnostic_observations,
    t.medicament,
    t.dosage,
    t.unity,
    t.frequency AS treatment_frequency
FROM attention a
LEFT JOIN diagnostic diag ON a.id = diag.idAttention AND diag.is_deleted = FALSE
LEFT JOIN treatment t ON a.id = t.idAttention AND t.is_deleted = FALSE
WHERE a.id = @attention2_id AND a.is_deleted = FALSE;

-- Leer alergias de un paciente (suponiendo patient_id=1)
SELECT * FROM allergies WHERE idClinicHistory = 1 AND is_deleted = FALSE;


-- ####################################################################
-- # UPDATE Operaciones                                               #
-- ####################################################################

-- Actualizar número de teléfono de un paciente (suponiendo patient_id=1)
UPDATE patients
SET phoneNumber = '0998887777', updated_by = 'admin_script_update', middleName = 'Andres'
WHERE id = 1;
-- Verificar la actualización
SELECT id, firstName, middleName, lastName1, phoneNumber, updated_at, updated_by FROM patients WHERE id = 1;

-- Actualizar especialidad de un doctor (suponiendo doctor_id=2)
UPDATE doctor
SET speciality = 'Pediatría y Neonatología', updated_by = 'admin_script_update'
WHERE id = 2;
-- Verificar la actualización
SELECT id, firstName, lastName1, speciality, updated_at, updated_by FROM doctor WHERE id = 2;

-- Actualizar la evolución de una atención (suponiendo attention_id=@attention2_id)
UPDATE attention
SET evolution = 'Paciente refiere mejoría de cefalea con ibuprofeno. Se indica continuar tratamiento y control si no hay mejoría completa.',
    updated_by = 'admin_script_update'
WHERE id = @attention2_id;
-- Verificar la actualización
SELECT id, evolution, updated_at, updated_by FROM attention WHERE id = @attention2_id;

-- ####################################################################
-- # DELETE (Soft Delete) Operaciones                                 #
-- ####################################################################
-- "Borrar" (marcar como borrado) un paciente (suponiendo patient_id=2, Maria Lopez)
-- Nota: Esto no borrará las atenciones asociadas, solo marca al paciente.
-- Deberías tener una lógica en tu aplicación para manejar cómo se muestran/acceden estos datos.
UPDATE patients
SET is_deleted = TRUE, updated_by = 'admin_script_delete'
WHERE id = 2;

-- Verificar que el paciente está marcado como borrado
SELECT * FROM patients WHERE id = 2;
SELECT * FROM patients WHERE is_deleted = FALSE; -- Ya no debería aparecer aquí

-- "Borrar" (marcar como borrada) una alergia específica (suponiendo que la alergia con id=1 pertenece al paciente 1)
UPDATE allergies
SET is_deleted = TRUE, updated_by = 'admin_script_delete'
WHERE id = 1 AND idClinicHistory = 1; -- Ser específico es bueno

-- Verificar que la alergia está marcada como borrada
SELECT * FROM allergies WHERE id = 1;
SELECT * FROM allergies WHERE idClinicHistory = 1 AND is_deleted = FALSE; -- Ya no debería aparecer aquí

-- "Borrar" (marcar como borrada) una atención específica (suponiendo attention_id=@attention1_id)
UPDATE attention
SET is_deleted = TRUE, updated_by = 'admin_script_delete'
WHERE id = @attention1_id;

-- Verificar que la atención está marcada como borrada
SELECT * FROM attention WHERE id = @attention1_id;
SELECT * FROM attention WHERE idClinicHistory = 1 AND is_deleted = FALSE; -- Debería mostrar menos atenciones para el paciente 1


-- Reactivar temporalmente las verificaciones de claves foráneas si se desactivaron
-- SET FOREIGN_KEY_CHECKS=1;

-- Confirmar las transacciones si se usó START TRANSACTION
-- COMMIT;
-- O para deshacer en caso de prueba:
-- ROLLBACK;

SELECT 'Script de prueba CRUD ejecutado.' AS Estatus;