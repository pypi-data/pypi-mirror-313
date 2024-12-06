import base64
import secrets
import hashlib


class Pbkdf2:
    """
    A class to handle password hashing using the PBKDF2 (Password-Based Key Derivation Function 2) algorithm.

    PBKDF2 is a key derivation function that applies a cryptographic hash function (e.g., SHA-256) to a password
    and a salt multiple times (iterations) to produce a secure derived key. This class provides methods to encode, decode,
    and verify password hashes using the PBKDF2 algorithm.
    """

    @classmethod
    def encode(cls, password: str, salt: str, hash_name: str, iterations: int) -> str:
        """
        Encode a password using PBKDF2 with the specified parameters.

        This method derives a password hash using the PBKDF2 algorithm with the specified salt, hash function,
        and iteration count. The result is returned as a base64-encoded string, which includes the PBKDF2 parameters
        for later verification.

        Args:
            password (str): The password to be encoded.
            salt (str): The salt used for the hashing process.
            hash_name (str): The hash function to use (e.g., 'sha256', 'sha512').
            iterations (int): The number of iterations to use for key derivation.

        Returns:
            str: A base64-encoded string that includes the encoded password hash and its parameters. The format of the returned
                 string is as follows:

                 $pbkdf2-{hash_name}$i={iterations}${base64_salt}${base64_password_hash}

                 Where:
                 - `{hash_name}`: The hash function used (e.g., 'sha256').
                 - `{iterations}`: The number of iterations used for key derivation.
                 - `{salt}`: The base64-encoded salt used for hashing.
                 - `{password_hash}`: The base64-encoded derived password hash.

        Example:
            encoded_password = Pbkdf2.encode('password', 'salt', 'sha256', 600000)
        """
        password_hash = hashlib.pbkdf2_hmac(
            hash_name=hash_name,
            password=password.encode("utf-8"),
            salt=salt.encode("utf-8"),
            iterations=iterations,
        )

        base64_salt = base64.b64encode(salt.encode("utf-8")).decode("utf-8")
        base64_password_hash = base64.b64encode(password_hash).decode("utf-8")

        return (
            f"$pbkdf2-{hash_name}$i={iterations}${base64_salt}${base64_password_hash}"
        )

    @classmethod
    def decode(cls, encoded_password: str) -> tuple:
        """
        Decode a previously encoded PBKDF2 password string into its components.

        This method splits the encoded password string into its individual components: hash name, salt, iteration count,
        and the password hash. The decoded components are returned as a tuple.

        Args:
            encoded_password (str): The base64-encoded PBKDF2 password string.

        Returns:
            tuple: A tuple containing the decoded hash name, salt, iterations, and password hash.

        Example:
            hash_name, salt, iterations, password_hash = Pbkdf2.decode(encoded_password)
        """
        components = encoded_password.split("$")
        hash_name = components[1].split("-")[1]
        iterations = int(components[2].split("=")[1])
        salt = base64.b64decode(components[3].encode("utf-8")).decode("utf-8")
        password_hash = base64.b64decode(components[4].encode("utf-8"))

        return (
            hash_name,
            salt,
            iterations,
            password_hash,
        )

    @classmethod
    def verify(cls, password: str, encoded_password: str) -> bool:
        """
        Verify that a given password matches the encoded password hash.

        This method compares the hash of the provided password with the stored password hash to confirm if they match.
        It uses the PBKDF2 algorithm with the same hash function, salt, and iteration count that were used to generate
        the password hash.

        Args:
            password (str): The password to be verified.
            encoded_password (str): The previously encoded password string to compare against.

        Returns:
            bool: True if the password matches the encoded password hash, False otherwise.

        Example:
            is_valid = Pbkdf2.verify('password', encoded_password)
        """
        decoded_data = cls.decode(encoded_password=encoded_password)

        password_hash = hashlib.pbkdf2_hmac(
            hash_name=decoded_data[0],
            password=password.encode("utf-8"),
            salt=decoded_data[1].encode("utf-8"),
            iterations=decoded_data[2],
        )

        return secrets.compare_digest(password_hash, decoded_data[3])


class Scrypt:
    """
    A class to handle password hashing using the Scrypt algorithm.

    Scrypt is a memory-hard key derivation function designed to make brute-force attacks more difficult by requiring
    significant amounts of memory and computational power. It uses a combination of a salt, cost factor, block size,
    and parallelization factor to generate a derived key. This class provides methods to encode, decode, and verify
    password hashes using the Scrypt algorithm.
    """

    @classmethod
    def encode(cls, password: str, salt: str, n: int, r: int, p: int) -> str:
        """
        Encode a password using Scrypt with the specified parameters.

        This method derives a password hash using the Scrypt algorithm with the specified salt, cost factor, block size,
        and parallelization factor. The result is returned as a base64-encoded string, which includes the Scrypt parameters
        for later verification.

        Args:
            password (str): The password to be encoded.
            salt (str): The salt used for the hashing process.
            n (int): The CPU/memory cost factor.
            r (int): The block size.
            p (int): The parallelization factor.

        Returns:
            str: A base64-encoded string that includes the encoded password hash and its parameters. The format of the returned
                 string is as follows:

                 $scrypt$ln={n}$r={r}$p={p}${salt}${password_hash}

                 Where:
                 - `{n}`: The CPU/memory cost factor used in the Scrypt algorithm (e.g., `16384`).
                 - `{r}`: The block size used in the Scrypt algorithm (e.g., `8`).
                 - `{p}`: The parallelization factor used in the Scrypt algorithm (e.g., `1`).
                 - `{salt}`: The base64-encoded salt used for hashing.
                 - `{password_hash}`: The base64-encoded derived password hash.

        Example:
            encoded_password = Scrypt.encode('password', 'salt', 16384, 8, 1)
        """
        password_hash = hashlib.scrypt(
            password=password.encode("utf-8"),
            salt=salt.encode("utf-8"),
            n=n,
            r=r,
            p=p,
        )

        base64_salt = base64.b64encode(salt.encode("utf-8")).decode("utf-8")
        base64_password_hash = base64.b64encode(password_hash).decode("utf-8")

        return f"$scrypt$ln={n}$r={r}$p={p}${base64_salt}${base64_password_hash}"

    @classmethod
    def decode(cls, encoded_password: str) -> tuple:
        """
        Decode a previously encoded Scrypt password string into its components.

        This method splits the encoded password string into its individual components: the salt, n, r, p,
        and password hash. The decoded components are returned as a tuple.

        Args:
            encoded_password (str): The base64-encoded Scrypt password string.

        Returns:
            tuple: A tuple containing the decoded salt, n, r, p, and password hash.

        Example:
            salt, n, r, p, password_hash = Scrypt.decode(encoded_password)
        """
        components = encoded_password.split("$")
        n = int(components[2].split("=")[1])
        r = int(components[3].split("=")[1])
        p = int(components[4].split("=")[1])
        salt = base64.b64decode(components[5].encode("utf-8")).decode("utf-8")
        password_hash = base64.b64decode(components[6].encode("utf-8"))

        return (
            salt,
            n,
            r,
            p,
            password_hash,
        )

    @classmethod
    def verify(cls, password: str, encoded_password: str) -> bool:
        """
        Verify that a given password matches the encoded password hash.

        This method compares the hash of the provided password with the stored password hash to confirm if they match.
        It uses the Scrypt algorithm with the same salt, n, r, and p parameters that were used to generate
        the password hash.

        Args:
            password (str): The password to be verified.
            encoded_password (str): The previously encoded password string to compare against.

        Returns:
            bool: True if the password matches the encoded password hash, False otherwise.

        Example:
            is_valid = Scrypt.verify('password', encoded_password)
        """
        decoded_password = cls.decode(encoded_password)

        password_hash = hashlib.scrypt(
            password=password.encode("utf-8"),
            salt=decoded_password[0].encode("utf-8"),
            n=decoded_password[1],
            r=decoded_password[2],
            p=decoded_password[3],
        )

        return secrets.compare_digest(password_hash, decoded_password[4])
