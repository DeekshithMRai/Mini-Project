import bcrypt
from .db import db
STATIC_SALT = b'$2b$12$Vna77RppwOUGikSHnQrcLu'

def verify_password(plain_password, hashed_password):
    return hash_password_bcrypt(plain_password) == hashed_password

def hash_password_bcrypt(password: str) -> str:
    """Hashes a password using bcrypt."""
    hashed = bcrypt.hashpw(password.encode(), STATIC_SALT)
    return hashed.decode()

def user_exists( email: str,password:str) -> bool:
    # user = db.query(User).filter( User.email == email).first()
    cursor=db.cursor()
    query='''select password from users where email=%s'''
    cursor.execute(query,(email,))
    result=cursor.fetchone()
    print(result)
    if result is None:
        return False
    else:
        return verify_password(password,result[0])