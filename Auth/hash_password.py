from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")


def hash_password_user(password:str):
    return pwd.hash(password)

def verify_password(current_password,hashed_password):
    return pwd.verify(current_password,hashed_password)