from typing import Dict, List, Optional, Any

class KeyStore:
    def __init__(self) -> None:
        """
        Create a new KeyStore instance.
        """
        ...

    def get_kid(self, kid: Optional[str] = None) -> str:
        """
        Get the key ID (KID) for the specified key. If no key ID is provided, the default KID is returned.
        """
        ...

    def get_private_key(self, kid: Optional[str] = None) -> str:
        """
        Retrieve the private key PEM for the specified key ID (KID).
        If no KID is specified, the default private key is returned.
        """
        ...

    def get_public_key(self, kid: Optional[str] = None) -> str:
        """
        Retrieve the public key PEM for the specified key ID (KID).
        If no KID is specified, the default public key is returned.
        """
        ...

    def get_algorithm(self, kid: Optional[str] = None) -> str:
        """
        Get the algorithm associated with the specified key ID (KID).
        If no KID is specified, the default key's algorithm is returned.
        """
        ...

    def register_private_key(self, kid: str, private_pem: str, algorithm: str) -> None:
        """
        Register a private key with the specified key ID (KID) and algorithm.
        """
        ...

    def register_public_key(self, kid: str, public_pem: str, algorithm: str) -> None:
        """
        Register a public key with the specified key ID (KID) and algorithm.
        """
        ...

    def register_algorithm(self, kid: str, algorithm: str) -> None:
        """
        Register an algorithm for the specified key ID (KID).
        """
        ...

    def register_keys(
        self,
        kid: str,
        private_pem: str,
        public_pem: str,
        algorithm: str,
        is_default: bool,
    ) -> None:
        """
        Register both private and public keys with the specified key ID (KID) and algorithm.
        If `is_default` is True, this key pair will be set as the default.
        """
        ...

    def load_keys(
        self,
        kid: str,
        private_key_path: str,
        public_key_path: str,
        algorithm: str,
        is_default: bool,
    ) -> None:
        """
        Load keys from files and register them with the specified key ID (KID) and algorithm.
        If `is_default` is True, this key pair will be set as the default.
        """
        ...

class TokenHeader:
    """
    Represents the headers for a JSON Web Token (JWT).
    """

    alg: str
    typ: Optional[str]
    kid: Optional[str]
    cty: Optional[str]
    x5t: Optional[str]
    x5c: Optional[List[str]]
    jku: Optional[str]

    def __init__(
        self,
        alg: str = "RS256",
        kid: Optional[str] = None,
        cty: Optional[str] = None,
        x5t: Optional[str] = None,
        x5c: Optional[List[str]] = None,
        jku: Optional[str] = None,
    ) -> None:
        """
        Initialize a new TokenHeader instance.

        :param alg: The algorithm used for signing the JWT (e.g., "RS256", "HS256").
        :param kid: The key ID, used to identify the key used to sign the token.
        :param cty: The content type, used for nested tokens (e.g., "JWT").
        :param x5t: The X.509 certificate thumbprint.
        :param x5c: The X.509 certificate chain.
        :param jku: The URL for the JWK set.
        """
        ...

    def __repr__(self) -> str:
        """
        Return a string representation of the TokenHeader.
        """
        ...

class TokenValidation:
    """
    Represents validation rules for a JWT payload.
    """

    required_spec_claims: List[str]
    leeway: int
    reject_tokens_expiring_in_less_than: int
    validate_exp: bool
    validate_nbf: bool
    validate_aud: bool
    aud: List[str]
    iss: List[str]
    sub: Optional[str]
    algorithms: List[str]
    validate_signature: bool
    exclude_headers: List[str]
    block: Dict[str, List[str]]
    claims: Dict[str, str]
    ttl: Optional[int]

    def __init__(
        self,
        required_spec_claims: Optional[List[str]] = None,
        leeway: Optional[int] = None,
        reject_tokens_expiring_in_less_than: Optional[int] = None,
        validate_exp: Optional[bool] = None,
        validate_nbf: Optional[bool] = None,
        validate_aud: Optional[bool] = None,
        aud: Optional[List[str]] = None,
        iss: Optional[List[str]] = None,
        sub: Optional[str] = None,
        algorithms: Optional[List[str]] = None,
        validate_signature: Optional[bool] = None,
        exclude_headers: Optional[List[str]] = None,
        block: Optional[Dict[str, List[str]]] = None,
        claims: Optional[Dict[str, str]] = None,
        ttl: Optional[int] = None,
    ) -> None:
        """
        Initialize a new TokenValidation instance with optional validation parameters.

        :param required_spec_claims: Claims required to be present in the JWT.
        :param leeway: Allowed leeway (in seconds) when validating timestamps like `exp` or `nbf`.
        :param reject_tokens_expiring_in_less_than: Reject tokens with short expiration time (in seconds).
        :param validate_exp: Whether to validate the `exp` claim.
        :param validate_nbf: Whether to validate the `nbf` claim.
        :param validate_aud: Whether to validate the `aud` claim.
        :param aud: List of acceptable audiences.
        :param iss: List of acceptable issuers.
        :param sub: Expected subject value.
        :param algorithms: List of acceptable algorithms (e.g., ["RS256", "HS256"]).
        :param validate_signature: Whether to validate the signature of the JWT.
        :param exclude_headers: Headers to exclude from validation.
        :param block: Map of claims to block specific values.
        :param claims: Map of claims and their expected values.
        :param ttl: Maximum allowable time-to-live (in seconds) for the token.
        """
        ...

    def rest_block(self, block: Dict[str, List[str]]) -> None:
        """
        Reset the blocking rules with a new set of claim-value pairs.

        :param block: A dictionary where keys are claim names and values are lists of blocked values.
        """
        ...

    def reset_claims(self, claims: Dict[str, str]) -> None:
        """
        Reset the claim validation rules with a new set of claim-value pairs.

        :param claims: A dictionary where keys are claim names and values are their expected values.
        """
        ...

class KeyManager:
    """
    A key manager for handling JWT operations with key storage and validation.
    """

    def __init__(self, key_store: KeyStore) -> None:
        """Initialize a new KeyManager instance."""
        ...

    @staticmethod
    def decode_key(key_base64: str) -> str:
        """Decode a Base64-encoded key."""
        ...

    @staticmethod
    def pem_to_jwk(pem_key: str, key_type: str, algorithm: Optional[str] = None) -> Dict[str, Any]:
        """Convert a PEM key to a JSON Web Key (JWK)."""
        ...

    @staticmethod
    def verify_token(
        token: str,
        public_key: str,
        validation: TokenValidation,
    ) -> Dict[str, Any]:
        """Verify a JWT token using a public key and validation rules."""
        ...

    def verify_token_by_kid(
        self,
        token: str,
        kid: str,
        validation: TokenValidation,
    ) -> Dict[str, Any]:
        """Verify a JWT token using a Key ID and validation rules."""
        ...

    @staticmethod
    def generate_token(
        private_key: str,
        claims: Dict[str, Any],
        header: TokenHeader,
    ) -> str:
        """Generate a JWT token using a private key, claims, and a header."""
        ...

    def generate_token_by_kid(
        self,
        claims: Dict[str, Any],
        header: TokenHeader,
    ) -> str:
        """Generate a JWT token using a Key ID, claims, and a header."""
        ...


class InvalidTokenError(Exception): ...
class DecodeError(Exception): ...
class InvalidSignatureError(Exception): ...
class ExpiredSignatureError(Exception): ...
class InvalidAudienceError(Exception): ...
class InvalidIssuerError(Exception): ...
class InvalidIssuedAtError(Exception): ...
class ImmatureSignatureError(Exception): ...
class InvalidKeyError(Exception): ...
class InvalidAlgorithmError(Exception): ...
class MissingRequiredClaimError(Exception): ...
class InvalidOperation(Exception): ...
class UnsupportedAlgorithm(Exception): ...
class KeyNotFoundError(Exception): ...
class DuplicateKeyError(Exception): ...
class InvalidKeyFormat(Exception): ...
class NotFound(Exception): ...
class BlockedKeyError(Exception): ...
class ExpiredTokenError(Exception): ...
class MissingMatchClaimError(Exception): ...