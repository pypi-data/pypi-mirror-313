from cryptography.fernet import Fernet


def fernet_generate_key() -> str:
    return Fernet.generate_key().decode()


def fernet_encrypt(*, data: str, key: str) -> str:
    return Fernet(key).encrypt(data.encode()).decode()


def fernet_decrypt(*, encoded_data: str, key: str) -> str:
    return Fernet(key).decrypt(encoded_data).decode()
