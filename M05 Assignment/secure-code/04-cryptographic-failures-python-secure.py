from argon2 import PasswordHasher

ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(password: str, stored_hash: str) -> bool:
    try:
        return ph.verify(stored_hash, password)
    except Exception:
        return False