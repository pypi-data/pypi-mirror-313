"""Todo app security module."""

from passlib.hash import pbkdf2_sha256


def verify_password(plain_password, hashed_password):
    """Verify user password."""
    return pbkdf2_sha256.verify(plain_password, hashed_password)


def get_password_hash(plain_password: str):
    """Hash user password."""
    return pbkdf2_sha256.hash(plain_password)
