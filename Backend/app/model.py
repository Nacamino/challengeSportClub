import bcrypt
from .dataBase import get_db
from datetime import datetime

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.crate_date = datetime.utcnow()
        
    def hash_password(self, password):
        """Hashea la contraseña usando bcrypt"""
        salt = bcrypt.gensalt()  
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.hash_password(self.password),
            "crate_date": self.crate_date,
        }
        
        # Obtener la colección de usuarios
        
    def get_user_collection():
        db = get_db()
        return db.users
    
    def find_by_email(email):
        users_collection = User.get_user_collection()
        return users_collection.find_one({"email": email})
    
    def authenticate_user(email, password):
        # Buscamos al usuario por su email
        user_data = User.find_by_email(email)
        
        if user_data:
            user = User(user_data['name'], user_data['email'], user_data['password'])
            # Comparamos la contraseña proporcionada con la almacenada
            print(user.check_password(password))
            if user.check_password(password):
                
                return user
        return None
