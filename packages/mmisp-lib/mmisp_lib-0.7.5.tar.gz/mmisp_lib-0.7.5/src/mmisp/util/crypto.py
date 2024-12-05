from functools import lru_cache

from passlib.context import CryptContext


@lru_cache(maxsize=128)
def verify_secret(secret: str, secret_hash: str) -> bool:
    context = CryptContext(schemes=["bcrypt", "argon2"])
    return context.verify(secret, secret_hash)


def hash_secret(secret: str) -> str:
    context = CryptContext(schemes=["bcrypt", "argon2"], bcrypt__ident="2y")
    return context.hash(secret)
