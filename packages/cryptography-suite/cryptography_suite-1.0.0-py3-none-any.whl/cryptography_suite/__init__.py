"""
Cryptography Suite Package Initialization.

Provides a comprehensive suite of cryptographic functions including symmetric encryption,
asymmetric encryption, hashing, key management, digital signatures, secret sharing,
password-authenticated key exchange, and one-time passwords.

Now includes additional algorithms and enhanced features for cutting-edge security applications.
"""

__version__ = "1.0.0"

from .encryption import (
    aes_encrypt,
    aes_decrypt,
    chacha20_encrypt,
    chacha20_decrypt,
    scrypt_encrypt,
    scrypt_decrypt,
    encrypt_file,
    decrypt_file,
    pbkdf2_encrypt,
    pbkdf2_decrypt,
)

from .asymmetric import (
    generate_rsa_keypair,
    rsa_encrypt,
    rsa_decrypt,
    serialize_private_key,
    serialize_public_key,
    load_private_key,
    load_public_key,
    generate_x25519_keypair,
    derive_x25519_shared_key,
    generate_ec_keypair,
)

from .signatures import (
    generate_ed25519_keypair,
    sign_message,
    verify_signature,
    serialize_ed25519_private_key,
    serialize_ed25519_public_key,
    load_ed25519_private_key,
    load_ed25519_public_key,
    generate_ecdsa_keypair,
    sign_message_ecdsa,
    verify_signature_ecdsa,
    serialize_ecdsa_private_key,
    serialize_ecdsa_public_key,
    load_ecdsa_private_key,
    load_ecdsa_public_key,
)

from .hashing import (
    sha384_hash,
    sha256_hash,
    sha512_hash,
    blake2b_hash,
    derive_key_scrypt,
    derive_key_pbkdf2,
    verify_derived_key_scrypt,
    verify_derived_key_pbkdf2,
    generate_salt,
)

from .key_management import (
    generate_aes_key,
    rotate_aes_key,
    secure_save_key_to_file,
    load_private_key_from_file,
    load_public_key_from_file,
    key_exists,
    generate_rsa_keypair_and_save,
    generate_ec_keypair_and_save,
)

from .secret_sharing import (
    create_shares,
    reconstruct_secret,
)

from .pake import (
    SPAKE2Client,
    SPAKE2Server,
)

from .otp import (
    generate_totp,
    verify_totp,
    generate_hotp,
    verify_hotp,
)

from .utils import (
    base62_encode,
    base62_decode,
    secure_zero,
    generate_secure_random_string,
)

__all__ = [
    # Encryption
    "aes_encrypt",
    "aes_decrypt",
    "chacha20_encrypt",
    "chacha20_decrypt",
    "scrypt_encrypt",
    "scrypt_decrypt",
    "pbkdf2_encrypt",
    "pbkdf2_decrypt",
    "encrypt_file",
    "decrypt_file",
    # Asymmetric
    "generate_rsa_keypair",
    "rsa_encrypt",
    "rsa_decrypt",
    "serialize_private_key",
    "serialize_public_key",
    "load_private_key",
    "load_public_key",
    "generate_x25519_keypair",
    "derive_x25519_shared_key",
    "generate_ec_keypair",
    # Signatures
    "generate_ed25519_keypair",
    "sign_message",
    "verify_signature",
    "serialize_ed25519_private_key",
    "serialize_ed25519_public_key",
    "load_ed25519_private_key",
    "load_ed25519_public_key",
    "generate_ecdsa_keypair",
    "sign_message_ecdsa",
    "verify_signature_ecdsa",
    "serialize_ecdsa_private_key",
    "serialize_ecdsa_public_key",
    "load_ecdsa_private_key",
    "load_ecdsa_public_key",
    # Hashing
    "sha384_hash",
    "sha256_hash",
    "sha512_hash",
    "blake2b_hash",
    "derive_key_scrypt",
    "derive_key_pbkdf2",
    "verify_derived_key_scrypt",
    "verify_derived_key_pbkdf2",
    "generate_salt",
    # Key Management
    "generate_aes_key",
    "rotate_aes_key",
    "secure_save_key_to_file",
    "load_private_key_from_file",
    "load_public_key_from_file",
    "key_exists",
    "generate_rsa_keypair_and_save",
    "generate_ec_keypair_and_save",
    # Secret Sharing
    "create_shares",
    "reconstruct_secret",
    # PAKE
    "SPAKE2Client",
    "SPAKE2Server",
    # OTP
    "generate_totp",
    "verify_totp",
    "generate_hotp",
    "verify_hotp",
    # Utils
    "base62_encode",
    "base62_decode",
    "secure_zero",
    "generate_secure_random_string",
]
