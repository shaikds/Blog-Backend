from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plaintext, hashed):
    return pwd_context.verify(plaintext, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)