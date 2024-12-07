use pyo3::prelude::*;

use serde::{Serialize, Deserialize};

/// Represents the headers for a JWT
#[pyclass]
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct TokenHeader {
    #[pyo3(get, set)]
    pub alg: String, // Algorithm (e.g., RS256, HS256)
    #[pyo3(get, set)]
    pub typ: Option<String>, // Type (e.g., JWT)
    #[pyo3(get, set)]
    pub kid: Option<String>, // Key ID
    #[pyo3(get, set)]
    pub cty: Option<String>, // Content type (e.g., JWT for nested tokens)
    #[pyo3(get, set)]
    pub x5t: Option<String>, // X.509 Certificate Thumbprint
    #[pyo3(get, set)]
    pub x5c: Option<Vec<String>>, // X.509 Certificate Chain
    #[pyo3(get, set)]
    pub jku: Option<String>, // JWK Set URL
}

#[pymethods]
impl TokenHeader {
    /// Create a new `TokenHeader` with the required `alg` and optional parameters.
    #[new]
    #[pyo3(signature = (alg="RS256".to_string(), kid=None, cty=None, x5t=None, x5c=None, jku=None))]
    pub fn new(
        alg: String,
        kid: Option<String>,
        cty: Option<String>,
        x5t: Option<String>,
        x5c: Option<Vec<String>>,
        jku: Option<String>,
    ) -> Self {
        Self {
            alg,
            typ: Some("JWT".to_string()),
            kid,
            cty,
            x5t,
            x5c,
            jku,
        }
    }
}