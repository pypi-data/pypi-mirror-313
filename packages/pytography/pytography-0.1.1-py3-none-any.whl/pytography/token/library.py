import json
import hmac
import base64
from typing import Any, Literal
from secrets import compare_digest
from .segments import DigestMod, Header, Payload


class JsonWebToken:
    """
    A class to handle the creation, decoding, and verification of JSON Web Tokens (JWT).

    JSON Web Tokens (JWT) are a compact, URL-safe means of representing claims to be transferred between two parties.
    This class provides methods to encode, decode, and verify JWTs using a specified signing algorithm (HS256, HS384, HS512).

    Methods:
        - encode: Encode a JWT from a header, payload, and secret key.
        - decode: Decode a JWT string into its header, payload, and signature.
        - verify: Verify the validity of a JWT by checking the signature, header, and payload.
    """

    @classmethod
    def _verify_signature(
        cls, header: dict, payload: dict, key: str, algorithm: str, signature: str
    ) -> bool:
        """
        Verify the signature of the JWT.

        This method generates the signature by encoding the header and payload, then compares it with the provided
        signature using the specified algorithm and secret key.

        Args:
            header (dict): The header part of the JWT.
            payload (dict): The payload part of the JWT.
            key (str): The secret key used for signing.
            algorithm (str): The signing algorithm to use (e.g., 'HS256', 'HS384', 'HS512').
            signature (str): The provided signature to verify.

        Returns:
            bool: True if the signature is valid, False otherwise.

        Example:
            is_valid_signature = JsonWebToken._verify_signature(header, payload, key, 'HS256', signature)
        """
        base64_header = base64.b64encode(json.dumps(header).encode("utf-8")).decode(
            "utf-8"
        )
        base64_payload = base64.b64encode(json.dumps(payload).encode("utf-8")).decode(
            "utf-8"
        )
        msg = base64.b64encode(f"{base64_header}.{base64_payload}".encode("utf-8"))
        generated_signature = base64.b64encode(
            hmac.new(
                key=key.encode("utf-8"), msg=msg, digestmod=DigestMod[algorithm]
            ).digest()
        ).decode("utf-8")

        return compare_digest(signature, generated_signature)

    @classmethod
    def encode(
        cls,
        payload: dict,
        key: str,
        algorithm: Literal["HS256", "HS384", "HS512"] = "HS256",
        header: dict | None = None,
    ) -> str:
        """
        Encode a payload into a JWT.

        This method encodes the payload and header into a JWT using the specified algorithm and secret key.
        It creates a base64-encoded JWT in the format:
        header.payload.signature.

        Args:
            payload (dict): The payload to include in the JWT.
            key (str): The secret key used for signing the JWT.
            algorithm (str): The signing algorithm to use ('HS256', 'HS384', 'HS512'). Default is 'HS256'.
            header (dict, optional): The header of the JWT. If None, the default header with 'alg' and 'typ' is used.

        Returns:
            str: The JWT string in the format 'header.payload.signature'.

        Example:
            token = JsonWebToken.encode(payload, key, 'HS256')
        """
        header = {**{"alg": algorithm, "typ": "JWT"}, **(header or {})}
        base64_header = base64.b64encode(json.dumps(header).encode("utf-8")).decode(
            "utf-8"
        )
        base64_payload = base64.b64encode(json.dumps(payload).encode("utf-8")).decode(
            "utf-8"
        )
        msg = base64.b64encode(f"{base64_header}.{base64_payload}".encode("utf-8"))
        signature = base64.b64encode(
            hmac.new(
                key=key.encode("utf-8"), msg=msg, digestmod=DigestMod[algorithm]
            ).digest()
        ).decode("utf-8")
        return f"{base64_header}.{base64_payload}.{signature}"

    @classmethod
    def decode(cls, token: str) -> tuple[Any, Any, str]:
        """
        Decode a JWT string into its components.

        This method splits the JWT into its header, payload, and signature parts, then decodes the header and payload
        from base64 and returns them along with the signature.

        Args:
            token (str): The JWT string to decode.

        Returns:
            tuple: A tuple containing the decoded header (dict), decoded payload (dict), and signature (str).

        Example:
            header, payload, signature = JsonWebToken.decode(token)
        """
        header, payload, signature = token.split(".")
        header = json.loads(base64.b64decode(header.encode("utf-8")))
        payload = json.loads(base64.b64decode(payload.encode("utf-8")))
        return header, payload, signature

    @classmethod
    def verify(
        cls,
        token: str,
        key: str,
        algorithm: Literal["HS256", "HS384", "HS512"] = "HS256",
        iss: str | None = None,
        sub: str | None = None,
        aud: str | None = None,
    ) -> bool:
        """
        Verify the validity of a JWT.

        This method verifies the JWT by checking the signature, header, and payload. It ensures that the header is valid,
        the payload contains the expected claims (such as 'iss', 'sub', and 'aud'), and the signature is correct.

        Args:
            token (str): The JWT string to verify.
            key (str): The secret key used to verify the signature.
            algorithm (str): The signing algorithm used for verification ('HS256', 'HS384', 'HS512').
            iss (str, optional): The expected issuer of the JWT. If None, no check is performed.
            sub (str, optional): The expected subject of the JWT. If None, no check is performed.
            aud (str, optional): The expected audience of the JWT. If None, no check is performed.

        Returns:
            bool: True if the JWT is valid (signature, header, and payload are verified), False otherwise.

        Example:
            is_valid = JsonWebToken.verify(token, key, 'HS256', iss='issuer', sub='subject', aud='audience')
        """
        header, payload, signature = cls.decode(token=token)

        is_header_verified = Header(**header).verify(algorithm=algorithm)
        if not is_header_verified:
            return False

        is_payload_verified = Payload(**payload).verify(iss=iss, sub=sub, aud=aud)
        if not is_payload_verified:
            return False

        is_signature_verified = cls._verify_signature(
            header=header,
            payload=payload,
            key=key,
            algorithm=algorithm,
            signature=signature,
        )
        if not is_signature_verified:
            return False

        return True
