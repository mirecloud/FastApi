from passlib.context import CryptContext

# Crée un contexte pour le hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash un mot de passe en utilisant bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie qu’un mot de passe correspond à son hash"""
    return pwd_context.verify(plain_password, hashed_password)
