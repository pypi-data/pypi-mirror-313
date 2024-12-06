import secrets
from typing import Literal
from .algorithms import Pbkdf2, Scrypt


class PasswordHashLibrary:
    """
    A class that provides methods to encode and verify passwords using different hashing algorithms.

    This class supports two widely-used password hashing algorithms: PBKDF2 (Password-Based Key Derivation Function 2)
    and Scrypt. It allows encoding passwords with either of these algorithms, and verifying the encoded password hashes.

    Methods:
        - encode: Encode a password using the selected hashing algorithm (PBKDF2 or Scrypt).
        - verify: Verify if the provided password matches the encoded password hash.
    """

    @classmethod
    def encode(
        cls,
        password: str,
        salt: str = secrets.token_hex(16),
        algorithm: Literal["pbkdf2", "scrypt"] = "scrypt",
        **kwargs,
    ) -> str:
        """
        Encode a password using the specified hashing algorithm (PBKDF2 or Scrypt).

        This method encodes a password by selecting the appropriate algorithm (PBKDF2 or Scrypt), using the parameters
        passed as arguments. The method incorporates a salt for added security. Additional parameters specific to the
        chosen algorithm, such as iterations for PBKDF2 or n, r, p for Scrypt, can be passed using `**kwargs`.

        Args:
            password (str): The password to be encoded.
            salt (str): The salt used in the hashing process. Default is a random 16-byte hex string.
            algorithm (str): The hashing algorithm to use. Either 'pbkdf2' or 'scrypt'. Default is 'scrypt'.
            **kwargs: Additional parameters for the selected algorithm:
                - For PBKDF2: hash_name (e.g., 'sha256'), iterations (e.g., 100000).
                - For Scrypt: n (CPU/memory cost factor), r (block size), p (parallelization factor).

        Returns:
            str: A base64-encoded string that includes the encoded password hash and its parameters,
                 formatted according to the chosen algorithm. The format depends on whether PBKDF2 or Scrypt is used.

        Example:
            encoded_password = PasswordHashLibrary.encode('password', algorithm='pbkdf2', hash_name='sha256', iterations=100000)
        """
        if algorithm == "pbkdf2":
            return Pbkdf2.encode(
                password=password,
                salt=salt,
                hash_name=kwargs.get("hash_name", "sha256"),
                iterations=kwargs.get("iterations", 600000),
            )
        if algorithm == "scrypt":
            return Scrypt.encode(
                password=password,
                salt=salt,
                n=kwargs.get("n", 16384),
                r=kwargs.get("r", 8),
                p=kwargs.get("p", 1),
            )

    @classmethod
    def verify(cls, password: str, encoded_password: str) -> bool:
        """
        Verify if the provided password matches the encoded password hash.

        This method first determines the hashing algorithm used in the encoded password by inspecting its prefix
        (either "pbkdf2" or "scrypt"). It then calls the respective verification method for PBKDF2 or Scrypt
        to compare the password with the stored hash.

        Args:
            password (str): The password to be verified.
            encoded_password (str): The encoded password string to compare against.

        Returns:
            bool: True if the password matches the encoded password hash, False otherwise.

        Example:
            is_valid = PasswordHashLibrary.verify('my_password', encoded_password)
        """
        if encoded_password.startswith("pbkdf2", 1):
            return Pbkdf2.verify(password=password, encoded_password=encoded_password)
        if encoded_password.startswith("scrypt", 1):
            return Scrypt.verify(password=password, encoded_password=encoded_password)
        return False
