from dotenv import load_dotenv
import os
import secrets

load_dotenv()

user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
port = os.getenv("MYSQL_PORT")
database = os.getenv("MYSQL_DATABASE")

DATABASE_CONNECTION_URI = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"

# En Producción, asegúrate de generar una clave secreta segura
# SECRET_KEY = secrets.token_urlsafe(32)
SECRET_KEY = "1234"