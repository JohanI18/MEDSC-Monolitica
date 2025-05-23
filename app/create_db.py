# create_db.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import time

# Carga las variables de entorno desde el archivo .env
load_dotenv()
 
# ----------------------------------------------------------------------
# Importa tu Base y todos los modelos desde models.py
# Al importar Base desde models.py, todos los modelos definidos en 
# ese archivo que heredan de Base se registrarán en Base.metadata.
# ----------------------------------------------------------------------
from models import Base  # <--- THIS IS THE CRUCIAL CHANGE/CORRECTION

# Obtiene las variables de entorno
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST") # For script on host, should be 'localhost' or '127.0.0.1'.
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

# Valida que las variables de entorno necesarias estén presentes
required_env_vars = {
    "MYSQL_USER": MYSQL_USER,
    "MYSQL_PASSWORD": MYSQL_PASSWORD,
    "MYSQL_HOST": MYSQL_HOST,
    "MYSQL_PORT": MYSQL_PORT,
    "MYSQL_DATABASE": MYSQL_DATABASE,
}

missing_vars = [key for key, value in required_env_vars.items() if value is None]
if missing_vars:
    print(f"Error: Faltan las siguientes variables de entorno en el archivo .env: {', '.join(missing_vars)}")
    exit(1)

# Construye la cadena de conexión
# Usamos mysql+mysqlconnector como dialecto para una mejor compatibilidad con MySQL 8
DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# Para depuración, muestra la URL de conexión (sin contraseña)
DATABASE_URL_DISPLAY = f"mysql+mysqlconnector://{MYSQL_USER}:********@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# Número de intentos para conectar a la base de datos
MAX_RETRIES = 10
RETRY_DELAY = 5 # segundos

def create_database_tables():
    engine = None
    print(f"Usando la URL de conexión: {DATABASE_URL_DISPLAY}") # Moved for earlier visibility
    
    for i in range(MAX_RETRIES):
        try:
            print(f"Intentando conectar a la base de datos MySQL (intento {i+1}/{MAX_RETRIES})...")
            engine = create_engine(DATABASE_URL)
            
            # Intenta una conexión para verificar que el servidor MySQL está levantado
            with engine.connect() as connection:
                connection.execute(text("SELECT 1")) 
            
            print(f"Conexión exitosa a la base de datos '{MYSQL_DATABASE}' en {MYSQL_HOST}:{MYSQL_PORT}.")
            
            # Crea todas las tablas definidas en Base.metadata
            # Base.metadata ahora contendrá todas las tablas de tu models.py
            print("Creando tablas (esto puede tomar un momento si hay muchas tablas)...")
            Base.metadata.create_all(bind=engine) 
            print("¡Tablas creadas exitosamente!")
            break # Sale del bucle si la conexión y creación son exitosas
        except OperationalError as e:
            print(f"Error de conexión o durante la operación con la base de datos: {e}")
            if "Access denied" in str(e):
                print("Verifica tus credenciales de MySQL (usuario, contraseña) y los permisos del usuario.")
            if "Unknown database" in str(e):
                print(f"La base de datos '{MYSQL_DATABASE}' no existe. MySQL no la creará automáticamente con estas credenciales.")
                print("Asegúrate de que la base de datos exista o que el usuario tenga permisos para crearla si el driver lo soporta (generalmente no con create_engine directamente).")
                print("El docker-compose crea la base de datos especificada en MYSQL_DATABASE al iniciar el contenedor de MySQL por primera vez.")

            if i < MAX_RETRIES - 1:
                print(f"Reintentando en {RETRY_DELAY} segundos...")
                time.sleep(RETRY_DELAY)
            else:
                print("Máximo número de reintentos alcanzado. Fallo al conectar o crear tablas.")
                exit(1) # Termina el script con un código de error
        except ImportError as e:
            print(f"Error de importación: {e}")
            print("Asegúrate de que 'models.py' exista en el mismo directorio o que la ruta de importación sea correcta.")
            print("También verifica que todas las dependencias de 'models.py' (como sqlalchemy) estén instaladas.")
            exit(1)
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            import traceback
            traceback.print_exc() # Imprime el stack trace completo para errores inesperados
            exit(1)
    
    if engine:
        engine.dispose() # Cierra las conexiones al finalizar

if __name__ == "__main__":
    # Asegúrate de que models.py está en el mismo directorio que create_db.py
    # o que está en el PYTHONPATH para que la importación "from models import Base" funcione
    print("Iniciando script para crear tablas de la base de datos...")
    create_database_tables()