from dotenv import load_dotenv
load_dotenv()
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Obtener la configuración de MongoDB de las variables de entorno
mongo_user = os.environ.get("MONGO_USER")
mongo_password = os.environ.get("MONGO_PASSWORD")
mongo_port = int(os.environ.get("MONGO_PORT"))

# Construir la cadena de conexión
mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@localhost:{mongo_port}/"

try:
    # Intentar establecer la conexión a MongoDB
    client = MongoClient(mongo_uri)
    database = client.db_fastapi

    print("Conexión a MongoDB exitosa")
except ConnectionFailure as e:
    print(f"Error de conexión: {e}")
