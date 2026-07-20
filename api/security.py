import secrets


def create_api_key():
    return secrets.token_urlsafe(32)