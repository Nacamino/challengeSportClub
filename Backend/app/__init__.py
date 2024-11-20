from flask import Flask
from pymongo import MongoClient
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()
    
    app = Flask(__name__, template_folder="./templates")

    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    
    app.config["JWT_KEY"] = os.getenv("JWT_KEY")
    
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    
    app.config['WTF_CSRF_SECRET_KEY'] = os.getenv('SECRET_KEY') 
    
    app.config['JWT_TOKEN_LOCATION'] = ['cookies'] 
    
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False  
    
    app.config['WTF_CSRF_CHECK_DEFAULT'] = False 
    
    app.config['WTF_CSRF_ENABLED'] = False
    
    csrf = CSRFProtect(app)  
    # from app.routes import auth_bp 
    from app.routes import register_routes
    register_routes(app)


    mongo = MongoClient(app.config["MONGO_URI"])
    jwt = JWTManager(app)

    return app
