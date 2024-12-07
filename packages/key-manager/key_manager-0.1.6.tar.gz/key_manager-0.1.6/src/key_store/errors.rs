use pyo3::create_exception;
use pyo3::exceptions::PyValueError;

create_exception!(key_store, KeyNotFoundError, PyValueError);
create_exception!(key_store, DuplicateKeyError, PyValueError);
create_exception!(key_store, InvalidKeyFormat, PyValueError);
create_exception!(key_store, InvalidOperation, PyValueError);
create_exception!(key_store, NotFound, PyValueError);
