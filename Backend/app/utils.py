import bcrypt
from flask_jwt_extended import decode_token, get_jwt_identity

def decode_jwt(token):
    return decode_token(token)
