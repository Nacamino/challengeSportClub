from pymongo import MongoClient
import os

# Conexión a la base de datos MongoDB
def get_db():
    client = MongoClient(os.getenv('MONGO_URI'))
    db = client['users']  # Cambia 'sportClub' por el nombre de tu base de datos
    return db
