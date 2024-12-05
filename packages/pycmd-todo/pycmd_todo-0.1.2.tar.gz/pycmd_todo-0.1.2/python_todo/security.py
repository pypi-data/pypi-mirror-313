"""Todo app security module."""
from passlib.context import CryptContext  # type: ignore

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # type: ignore


def verify_password(plain_password, hashed_password):
    """Verify user password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password: str):
    """Hash user password."""
    return pwd_context.hash(plain_password)
