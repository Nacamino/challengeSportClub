from flask import Blueprint, request, render_template, jsonify, Flask, redirect, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
from .model import User
from app.validForms import RegistrationForm, LoginForm, UpdateProfileForm
from .dataBase import get_db
from flask_wtf.csrf import generate_csrf
from datetime import timedelta

auth_bp = Blueprint('user', __name__)

# Registrar un nuevo usuario
@auth_bp.route('/register', methods=['POST', 'GET'])
def register_user():
    form = RegistrationForm()  

    if form.validate_on_submit():  
        name = form.name.data
        email = form.email.data
        password = form.password.data

        user_collection = get_db().users
        if user_collection.find_one({"email": email}):
            return jsonify({"error": "Correo electrónico ya registrado"}), 400

        new_user = User(name=name, email=email, password=password)

        user_collection.insert_one(new_user.to_dict())

        access_token = create_access_token(identity=email)

        jsonify({
            "message": "Usuario registrado exitosamente"
        }), 201
        return redirect(url_for('user.login'))
         

    return render_template('register.html', form=form)

# Iniciar sesión
@auth_bp.route('/login', methods=['POST', 'GET'])

def login():
    form = LoginForm()
    if form.validate_on_submit():  # Asegúrate de validar correctamente el formulario
        email = form.email.data
        password = form.password.data

        user = User.authenticate_user(email, password)
        if user:
            access_token = create_access_token(identity=user.email)
            response = jsonify({"message": "Login exitoso"})
            set_access_cookies(response, access_token)            

            return response.data
        
        return jsonify({"error": "Credenciales incorrectas"}), 401

    return render_template('login.html', form=form)

def register_routes(app):
    app.register_blueprint(auth_bp)
    return auth_bp


@auth_bp.route('/profile', methods=['GET'],  endpoint='profile')
@jwt_required(locations=["cookies"]) 
def get_profile():
    current_user_email = get_jwt_identity()  
    user = get_db().users.find_one({"email": current_user_email})
    
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    return render_template('profile.html', user=user)


# Actualizar perfil
@auth_bp.route('/profile/update', methods=['GET', 'POST'])
@jwt_required(locations=["cookies"])  # Autenticación basada en JWT en cookies
def update_profile():
    current_user_email = get_jwt_identity()
    form = UpdateProfileForm()
    
    user_collection = get_db().users

    user = user_collection.find_one({"email": current_user_email})
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if form.validate_on_submit():
        
        name = form.name.data
        email = form.email.data

        if email != current_user_email:
            if user_collection.find_one({"email": email}):
                return jsonify({"error": "Correo electrónico ya registrado"}), 400

            user_collection.update_one(
                {"email": current_user_email},
                {"$set": {"name": name, "email": email}}
            )
            
            access_token = create_access_token(identity=email)

            # Establece el nuevo JWT en las cookies (sin CSRF)
            response = jsonify({"message": "Perfil actualizado con éxito"})
            set_access_cookies(response, access_token)  # Establece el JWT en las cookies

            # Retorna la respuesta con el nuevo JWT
            return redirect(url_for('user.profile'))


        # Si no ha cambiado el correo, solo actualiza el nombre
        user_collection.update_one(
            {"email": current_user_email},
            {"$set": {"name": name}}
        )

        jsonify({"message": "Perfil actualizado con éxito"}), 200
        return redirect(url_for('user.profile'))
             
    return render_template('update.html', form=form)



@auth_bp.route('/logout', methods=['POST'])
@jwt_required(locations=["cookies"])  # Se requiere un JWT válido para cerrar sesión
def logout():
    response = jsonify({"message": "Logout exitoso"})
    
    unset_jwt_cookies(response)
    
    return redirect(url_for('user.login'))


