import hashlib
import secrets

users = {}

def register(username, password):
    if username in users:
        return False

    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256(
        (password + salt).encode()
    ).hexdigest()

    users[username] = {
        "salt": salt,
        "password_hash": password_hash
    }
    return True


def login(username, password):
    if username not in users:
        return False

    salt = users[username]["salt"]
    password_hash = hashlib.sha256(
        (password + salt).encode()
    ).hexdigest()

    return secrets.compare_digest(
        password_hash,
        users[username]["password_hash"]
    )