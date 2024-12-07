use pyo3::create_exception;
use pyo3::exceptions::PyValueError;

create_exception!(token_validation, ExpiredTokenError, PyValueError);
create_exception!(token_validation, MissingRequiredClaimError, PyValueError);
create_exception!(token_validation, MissingMatchClaimError, PyValueError);
create_exception!(token_validation, BlockedKeyError, PyValueError);
create_exception!(token_validation, InvalidOperation, PyValueError);