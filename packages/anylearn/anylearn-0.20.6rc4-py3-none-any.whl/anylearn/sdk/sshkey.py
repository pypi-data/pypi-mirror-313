from dataclasses import dataclass

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


@dataclass
class SSHKey:
    public_key: bytes
    private_key: bytes


RSA_PUBLIC_EXPONENT = 65537
RSA_KEY_SIZE = 4096


def generate_ssh_key_pair() -> SSHKey:
    # ref: https://stackoverflow.com/a/39126754/1720770
    key = rsa.generate_private_key(
        public_exponent=RSA_PUBLIC_EXPONENT,
        key_size=RSA_KEY_SIZE,
    )
    public_key = key.public_key().public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH,
    )
    private_key = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return SSHKey(public_key=public_key, private_key=private_key)
