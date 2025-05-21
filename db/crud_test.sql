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

-- Obtener IDs de los doctores insertados
SET @doctor1_id = (SELECT id FROM doctor WHERE identifierCode = 'DOC001');
SET @doctor2_id = (SELECT id FROM doctor WHERE identifierCode = 'DOC002');

-- --------------------------------------------------------
-- Insertar Credenciales para Doctores
-- ¡EN PRODUCCIÓN, USA HASHES PARA LAS CONTRASEÑAS!
-- --------------------------------------------------------
INSERT INTO credentials (identifierCode, password, idUser, userType, created_by, updated_by) VALUES
('DOC001', 'password123', @doctor1_id, 'doctor', 'admin_script', 'admin_script'), -- Contraseña para Dr. Sanchez
('DOC002', 'securepass', @doctor2_id, 'doctor', 'admin_script', 'admin_script'); -- Contraseña para Dra. Gomez

-- --------------------------------------------------------
-- Insertar Pacientes
-- --------------------------------------------------------
INSERT INTO patients (identifierType, identifierCode, firstName, middleName, lastName1, lastName2, nationality, address, phoneNumber, birthdate, gender, sex, civilStatus, job, bloodType, email, created_by, updated_by) VALUES
('Cedula', '1234567890', 'Juan', 'Carlos', 'Perez', 'Gomez', 'Ecuatoriana', 'Calle Sol 123, Quito', '0991234567', '1985-06-15', 'Masculino', 'Masculino', 'Casado/a', 'Ingeniero de Sistemas', 'O+', 'juan.perez@example.com', 'admin_script', 'admin_script'),
('Pasaporte', 'AB123456', 'Maria', 'Elena', 'Lopez', 'Vega', 'Colombiana', 'Av. Luna 456, Guayaquil', '0987654321', '1992-11-20', 'Femenino', 'Femenino', 'Soltero/a', 'Diseñadora Gráfica', 'A+', 'maria.lopez@example.com', 'admin_script', 'admin_script');

-- Obtener IDs de los pacientes insertados
SET @patient1_id = (SELECT id FROM patients WHERE identifierCode = '1234567890');
SET @patient2_id = (SELECT id FROM patients WHERE identifierCode = 'AB123456');

-- --------------------------------------------------------
-- Insertar Alergias para Paciente 1 (@patient1_id)
-- --------------------------------------------------------
INSERT INTO allergies (allergies, idPatient, created_by, updated_by) VALUES
('Polen, Penicilina', @patient1_id, 'admin_script', 'admin_script');

-- --------------------------------------------------------
-- Insertar Contacto de Emergencia para Paciente 1 (@patient1_id)
-- --------------------------------------------------------
INSERT INTO emergencyContact (firstName, lastName, address, relationship, phoneNumber1, phoneNumber2, idPatient, created_by, updated_by) VALUES
('Luisa', 'Gomez', 'Calle Sol 123, Quito (misma que paciente)', 'Esposa', '0997654321', '022345678', @patient1_id, 'admin_script', 'admin_script');

-- --------------------------------------------------------
-- Insertar Antecedentes Familiares para Paciente 1 (@patient1_id)
-- --------------------------------------------------------
INSERT INTO familyBackground (familyBackground, time, degreeRelationship, idPatient, created_by, updated_by) VALUES
('Padre con Hipertensión, Madre con Diabetes tipo 2', '2000-01-01', '1', @patient1_id, 'admin_script', 'admin_script');

-- --------------------------------------------------------
-- Insertar Condiciones Preexistentes para Paciente 1 (@patient1_id)
-- --------------------------------------------------------
INSERT INTO preExistingCondition (diseaseName, time, medicament, treatment, idPatient, created_by, updated_by) VALUES
('Asma leve intermitente', '2010-05-01', 'Salbutamol inhalador', 'Uso según necesidad', @patient1_id, 'admin_script', 'admin_script');

-- --------------------------------------------------------
-- Insertar Atención Médica para Paciente 1 (@patient1_id) con Doctor 1 (@doctor1_id)
-- --------------------------------------------------------
INSERT INTO attention (date, weight, height, temperature, bloodPressure, heartRate, oxygenSaturation, breathingFrequency, glucose, hemoglobin, reasonConsultation, currentIllness, evolution, idPatient, idDoctor, created_by, updated_by) VALUES
(NOW(), 75, 170, 37, '120/80', 80, 98, 16, 90, 15, 'Chequeo general anual', 'Paciente asintomático, refiere buen estado general.', 'Estable, sin hallazgos patológicos.', @patient1_id, @doctor1_id, 'admin_script', 'admin_script');
SET @attention1_id = LAST_INSERT_ID();

-- --------------------------------------------------------
-- Insertar Atención Médica para Paciente 2 (@patient2_id) con Doctor 2 (@doctor2_id)
-- --------------------------------------------------------
INSERT INTO attention (date, weight, height, temperature, bloodPressure, heartRate, oxygenSaturation, breathingFrequency, reasonConsultation, currentIllness, evolution, idPatient, idDoctor, created_by, updated_by) VALUES
(NOW() - INTERVAL 1 DAY, 65, 165, 38, '130/85', 85, 97, 18, 'Dolor de cabeza y malestar general', 'Paciente refiere cefalea intensa desde hace 2 días, acompañada de fatiga.', 'En evaluación.', @patient2_id, @doctor2_id, 'admin_script', 'admin_script');
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

-- Leer un paciente específico por ID (@patient1_id)
SELECT * FROM patients WHERE id = @patient1_id AND is_deleted = FALSE;

-- Leer todos los doctores no borrados
SELECT * FROM doctor WHERE is_deleted = FALSE;

-- Leer un doctor específico por identifierCode
SELECT * FROM doctor WHERE identifierCode = 'DOC001' AND is_deleted = FALSE;

-- Leer todas las atenciones de un paciente específico (@patient1_id) con información del doctor
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
JOIN patients p ON a.idPatient = p.id -- CAMBIADO
JOIN doctor d ON a.idDoctor = d.id
WHERE a.idPatient = @patient1_id AND a.is_deleted = FALSE AND p.is_deleted = FALSE AND d.is_deleted = FALSE -- CAMBIADO
ORDER BY a.date DESC;

-- Leer los diagnósticos y tratamientos de una atención específica (@attention2_id)
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

-- Leer alergias de un paciente (@patient1_id)
SELECT * FROM allergies WHERE idPatient = @patient1_id AND is_deleted = FALSE; -- CAMBIADO


-- ####################################################################
-- # UPDATE Operaciones                                               #
-- ####################################################################

-- Actualizar número de teléfono y nombre medio de un paciente (@patient1_id)
UPDATE patients
SET phoneNumber = '0998887777', updated_by = 'admin_script_update', middleName = 'Andres'
WHERE id = @patient1_id;
-- Verificar la actualización
SELECT id, firstName, middleName, lastName1, phoneNumber, updated_at, updated_by FROM patients WHERE id = @patient1_id;

-- Actualizar especialidad de un doctor (@doctor2_id)
UPDATE doctor
SET speciality = 'Pediatría y Neonatología', updated_by = 'admin_script_update'
WHERE id = @doctor2_id;
-- Verificar la actualización
SELECT id, firstName, lastName1, speciality, updated_at, updated_by FROM doctor WHERE id = @doctor2_id;

-- Actualizar la evolución de una atención (@attention2_id)
UPDATE attention
SET evolution = 'Paciente refiere mejoría de cefalea con ibuprofeno. Se indica continuar tratamiento y control si no hay mejoría completa.',
    updated_by = 'admin_script_update'
WHERE id = @attention2_id;
-- Verificar la actualización
SELECT id, evolution, updated_at, updated_by FROM attention WHERE id = @attention2_id;

-- ####################################################################
-- # DELETE (Soft Delete) Operaciones                                 #
-- ####################################################################
-- "Borrar" (marcar como borrado) un paciente (@patient2_id, Maria Lopez)
UPDATE patients
SET is_deleted = TRUE, updated_by = 'admin_script_delete'
WHERE id = @patient2_id;

-- Verificar que el paciente está marcado como borrado
SELECT * FROM patients WHERE id = @patient2_id;
SELECT * FROM patients WHERE is_deleted = FALSE; -- Ya no debería aparecer aquí

-- "Borrar" (marcar como borrada) una alergia específica (suponiendo que la alergia con id=1 pertenece al paciente @patient1_id)
-- Primero obtenemos el ID de la alergia para ser más precisos, si no lo conocemos de antemano
SET @allergy_id_to_delete = (SELECT id FROM allergies WHERE idPatient = @patient1_id AND allergies LIKE '%Penicilina%' LIMIT 1);

UPDATE allergies
SET is_deleted = TRUE, updated_by = 'admin_script_delete'
WHERE id = @allergy_id_to_delete AND idPatient = @patient1_id; -- CAMBIADO y usando variable

-- Verificar que la alergia está marcada como borrada
SELECT * FROM allergies WHERE id = @allergy_id_to_delete;
SELECT * FROM allergies WHERE idPatient = @patient1_id AND is_deleted = FALSE; -- Ya no debería aparecer aquí

-- "Borrar" (marcar como borrada) una atención específica (@attention1_id)
UPDATE attention
SET is_deleted = TRUE, updated_by = 'admin_script_delete'
WHERE id = @attention1_id;

-- Verificar que la atención está marcada como borrada
SELECT * FROM attention WHERE id = @attention1_id;
SELECT * FROM attention WHERE idPatient = @patient1_id AND is_deleted = FALSE; -- CAMBIADO


-- Reactivar temporalmente las verificaciones de claves foráneas si se desactivaron
-- SET FOREIGN_KEY_CHECKS=1;

-- Confirmar las transacciones si se usó START TRANSACTION
-- COMMIT;
-- O para deshacer en caso de prueba:
-- ROLLBACK;

SELECT 'Script de prueba CRUD ejecutado.' AS Estatus;