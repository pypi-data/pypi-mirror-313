from typing import Optional, List, Dict

class InvalidTokenError(Exception):
    pass

class ExpiredSignatureError(Exception):
    pass

class ImmatureSignatureError(Exception):
    pass

class InvalidAudienceError(Exception):
    pass

class InvalidIssuerError(Exception):
    pass

class MissingRequiredClaimError(Exception):
    pass

class DecodeError(Exception):
    pass

class InvalidKeyError(Exception):
    pass

class InvalidAlgorithmError(Exception):
    pass

class PyJWTError(Exception):
    pass


class MissingMatchClaimError(Exception):
    pass

class DecodeError(Exception):
    pass

class BlockedKeyError(Exception):
    pass

class ExpiredToken(Exception):
    pass


class TokenValidation:
    required_spec_claims: List[str]
    leeway: int
    reject_tokens_expiring_in_less_than: int
    validate_exp: bool
    validate_nbf: bool
    validate_aud: bool
    aud: Optional[List[str]]
    iss: Optional[List[str]]
    sub: Optional[str]
    algorithms: List[str]
    validate_signature: bool
    exclude_headers: List[str]
    block: Dict[str, List[str]]
    claims: Dict[str, str]
    ttl: Optional[int]

    def __init__(self) -> None: ...
    def update_block(self, block: Dict[str, List[str]]) -> None: ...
    def update_claims(self, claims: Dict[str, str]) -> None: ...
    def validate_payload(self, payload: Dict[str, str]) -> None: ...
    def as_dict(self) -> Dict[str, str]: ...

class KeyStore:
    def __init__(self) -> None: ...
    def clone_inner(self) -> 'KeyStore': ...
    def register_keys(self, kid: str, private_pem: str, public_pem: str, algorithm: str, is_default: bool) -> None: ...
    def load_keys(self, kid: str, private_key_path: str, public_key_path: str, algorithm: str, is_default: bool) -> None: ...
    def get_kid(self, kid: Optional[str] = None) -> str: ...
    def get_public_key(self, kid: Optional[str] = None) -> str: ...
    def get_private_key(self, kid: Optional[str] = None) -> str: ...
    def get_algorithm(self, kid: Optional[str] = None) -> str: ...

class KeyManager:
    def __init__(self, key_store: KeyStore) -> None: ...
    @staticmethod
    def decode_key(key_base64: str) -> str: ...
    @staticmethod
    def pem_to_jwk(pem_key: str, key_type: str, algorithm: Optional[str] = None) -> Dict[str, str]: ...
    @staticmethod
    def verify_token(token: str, public_key: str, validation: TokenValidation, algorithm: Optional[str] = None) -> Dict[str, str]: ...
    def verify_token_by_kid(self, token: str, kid: str, validation: TokenValidation) -> Dict[str, str]: ...
    @staticmethod
    def generate_token(private_key: str, claims: Dict[str, str], algorithm: Optional[str] = None, kid: Optional[str] = None) -> str: ...
    def generate_token_by_kid(self, kid: str, claims: Dict[str, str]) -> str: ...
