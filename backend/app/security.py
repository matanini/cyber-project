import hmac
import hashlib
import secrets

def hash_password(salt, password):
    return hmac.new(
        key=salt.encode('utf-8'),
        msg=password.encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

def check_password(salt, hashed_password, password):
    return hmac.compare_digest(
        hashed_password,
        hash_password(salt, password)
    )

def generate_token():
    # generate a 16 byte hex token using sha1
    return hashlib.sha1(secrets.token_bytes(16)).hexdigest()
    