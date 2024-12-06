from dataclasses import dataclass
from datetime import datetime, timezone


DigestMod = {
    "HS256": "sha256",
    "HS384": "sha384",
    "HS512": "sha512",
}


@dataclass
class Header:
    """
    A class representing the header of a JWT (JSON Web Token).

    The header typically consists of two parts:
    1. The signing algorithm used, such as 'HS256'.
    2. The type of token (usually "JWT").

    Methods:
        - _is_alg_verified: Helper method to verify if the 'alg' matches the expected algorithm.
        - verify: Verifies if the header is valid, especially the algorithm ('alg').
    """

    alg: str
    typ: str

    def __init__(self, **kwargs):
        """
        Initializes the JWT header.

        Args:
            **kwargs: Additional parameters to populate the 'alg' and 'typ' fields.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _is_alg_verified(self, algorithm: str) -> bool:
        """
        Verifies if the 'alg' in the header matches the expected signing algorithm.

        Args:
            algorithm (str): The algorithm to verify against.

        Returns:
            bool: True if the 'alg' matches the expected algorithm, False otherwise.
        """
        if (
            isinstance(self.alg, str)
            and isinstance(algorithm, str)
            and self.alg in DigestMod
            and algorithm in DigestMod
        ):
            return self.alg == algorithm
        return False

    def verify(self, algorithm: str) -> bool:
        """
        Verifies if the 'alg' field in the header matches the expected algorithm.

        Args:
            algorithm (str): The algorithm to verify against.

        Returns:
            bool: True if the header is valid, False otherwise.
        """
        return self._is_alg_verified(algorithm=algorithm)


@dataclass
class Payload:
    """
    A class representing the payload of a JWT (JSON Web Token).

    The payload contains the claims or information (e.g., 'iss', 'sub', 'aud') and can optionally
    include metadata like 'exp' (expiration time), 'nbf' (not before), 'iat' (issued at), and 'jti' (JWT ID).

    Methods:
        - _is_iss_verified: Verifies the 'iss' (issuer) claim.
        - _is_sub_verified: Verifies the 'sub' (subject) claim.
        - _is_aud_verified: Verifies the 'aud' (audience) claim.
        - _is_exp_verified: Verifies the 'exp' (expiration time) claim.
        - _is_nbf_verified: Verifies the 'nbf' (not before) claim.
        - _is_iat_verified: Verifies the 'iat' (issued at) claim.
        - verify: Verifies all claims, including 'iss', 'sub', 'aud', and time-based claims ('exp', 'nbf', 'iat').
    """

    iss: str | None = None
    sub: str | None = None
    aud: str | None = None
    exp: float | None = None
    nbf: float | None = None
    iat: float | None = None
    jti: str | None = None

    def __init__(self, **kwargs):
        """
        Initializes the JWT payload with claims and optional metadata.

        Args:
            **kwargs: Additional parameters to populate the claims like 'iss', 'sub', 'aud', etc.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _is_iss_verified(self, iss: str | None) -> bool:
        """
        Verifies if the 'iss' (issuer) claim matches the provided value.

        Args:
            iss (str | None): The expected issuer value.

        Returns:
            bool: True if the 'iss' claim matches the expected issuer, False otherwise.
        """
        if self.iss is None and iss is None:
            return True
        if isinstance(self.iss, str) and isinstance(iss, str):
            return self.iss == iss
        return False

    def _is_sub_verified(self, sub: str | None) -> bool:
        """
        Verifies if the 'sub' (subject) claim matches the provided value.

        Args:
            sub (str | None): The expected subject value.

        Returns:
            bool: True if the 'sub' claim matches the expected subject, False otherwise.
        """
        if self.sub is None and sub is None:
            return True
        if isinstance(self.sub, str) and isinstance(sub, str):
            return self.sub == sub
        return False

    def _is_aud_verified(self, aud: str | None) -> bool:
        """
        Verifies if the 'aud' (audience) claim matches the provided value.

        Args:
            aud (str | None): The expected audience value.

        Returns:
            bool: True if the 'aud' claim matches the expected audience, False otherwise.
        """
        if self.aud is None and aud is None:
            return True
        if isinstance(self.aud, str) and isinstance(aud, str):
            return self.aud == aud
        return False

    def _is_exp_verified(self, now: float) -> bool:
        """
        Verifies if the 'exp' (expiration time) claim is valid (i.e., it has not expired).

        Args:
            now (float): The current timestamp.

        Returns:
            bool: True if the 'exp' claim is valid, False if expired.
        """
        if self.exp is None:
            return True
        if isinstance(self.exp, float):
            return self.exp > now
        return False

    def _is_nbf_verified(self, now: float) -> bool:
        """
        Verifies if the 'nbf' (not before) claim is valid (i.e., the token is not being used before its allowed time).

        Args:
            now (float): The current timestamp.

        Returns:
            bool: True if the 'nbf' claim is valid, False otherwise.
        """
        if self.nbf is None:
            return True
        if isinstance(self.nbf, float):
            return self.nbf < now
        return False

    def _is_iat_verified(self, now: float) -> bool:
        """
        Verifies if the 'iat' (issued at) claim is valid (i.e., the token is not issued in the future).

        Args:
            now (float): The current timestamp.

        Returns:
            bool: True if the 'iat' claim is valid, False otherwise.
        """
        if self.iat is None:
            return True
        if isinstance(self.iat, float):
            return self.iat < now
        return False

    def verify(
        self, iss: str | None = None, sub: str | None = None, aud: str | None = None
    ) -> bool:
        """
        Verifies the claims in the JWT payload, including 'iss', 'sub', 'aud', and time-based claims.

        Args:
            iss (str | None): The expected issuer of the JWT.
            sub (str | None): The expected subject of the JWT.
            aud (str | None): The expected audience of the JWT.

        Returns:
            bool: True if all the claims are verified, False otherwise.
        """
        now = datetime.now(timezone.utc).timestamp()
        is_iss_verified = self._is_iss_verified(iss=iss)
        is_sub_verified = self._is_sub_verified(sub=sub)
        is_aud_verified = self._is_aud_verified(aud=aud)
        is_exp_verified = self._is_exp_verified(now=now)
        is_nbf_verified = self._is_nbf_verified(now=now)
        is_iat_verified = self._is_iat_verified(now=now)

        return (
            is_iss_verified
            and is_sub_verified
            and is_aud_verified
            and is_exp_verified
            and is_nbf_verified
            and is_iat_verified
        )
