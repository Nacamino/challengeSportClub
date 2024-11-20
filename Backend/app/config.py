import os

class Config:
    MONGO_URI = os.getenv('MONGO_URI')  # Cambié el puerto a 27017, el predeterminado de MongoDB
    JWT_KEY = os.getenv('JWT_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = 600 