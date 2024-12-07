use serde_json::Value;
use std::collections::HashMap;

use pyo3::types::{PyDict, PyList};
use pyo3::prelude::*;

use crate::token_validation::errors::*;

#[pyclass]
pub struct TokenValidation {
    #[pyo3(get, set)]
    pub required_spec_claims: Vec<String>,
    #[pyo3(get, set)]
    pub leeway: u64,
    #[pyo3(get, set)]
    pub reject_tokens_expiring_in_less_than: u64,
    #[pyo3(get, set)]
    pub validate_exp: bool,
    #[pyo3(get, set)]
    pub validate_nbf: bool,
    #[pyo3(get, set)]
    pub validate_aud: bool,
    #[pyo3(get, set)]
    pub aud: Vec<String>,
    #[pyo3(get, set)]
    pub iss: Vec<String>,
    #[pyo3(get, set)]
    pub sub: Option<String>,
    #[pyo3(get, set)]
    pub kid: Option<String>,
    #[pyo3(get, set)]
    pub algorithms: Vec<String>,
    #[pyo3(get, set)]
    pub validate_signature: bool,
    #[pyo3(get, set)]
    pub exclude_headers: Vec<String>,
    #[pyo3(get, set)]
    pub block: HashMap<String, Vec<String>>,
    #[pyo3(get, set)]
    pub claims: HashMap<String, String>,
    #[pyo3(get, set)]
    pub ttl: Option<u64>
}

impl TokenValidation {
    pub fn validate_payload(&self, payload: &serde_json::Map<String, Value>) -> PyResult<()> {
        // Check if block validation is enabled

        if !self.block.is_empty(){
            for (key, blocked_list_values) in &self.block {
                if let Some(actual_value) = payload.get(key) {
                    let actual_value = serde_json::to_string(actual_value)
                        .map_err(|_| PyErr::new::<InvalidOperation, _>(format!(
                            "Failed to convert claim value to string")))?
                        .trim_matches('"') // Remove surrounding quotes if any
                        .to_string();

                    if blocked_list_values.contains(&actual_value) {
                        return Err(PyErr::new::<BlockedKeyError, _>(format!(
                            "Blocked value '{}' found for claim '{}'",
                            actual_value, key
                        )));
                    }

                    // Move to the next iteration if the value is not blocked
                } else {
                    return Err(PyErr::new::<MissingRequiredClaimError, _>(format!(
                        "Missing expected claim '{}'",
                        key
                    )));
                }
            }

        }

        // Check if claims validation is enabled
        if !self.claims.is_empty() {
            for (key, expected_value) in &self.claims {
                if let Some(actual_value) = payload.get(key) {
                    let actual_value = serde_json::to_string(actual_value)
                        .map_err(|_| PyErr::new::<InvalidOperation, _>(format!(
                            "Failed to convert claim value to string")))?
                        .trim_matches('"') // Remove surrounding quotes if any
                        .to_string();

                    if actual_value != *expected_value {
                        return Err(PyErr::new::<MissingMatchClaimError, _>(format!(
                            "Claim '{}' does not match the expected value '{}'",
                                key, expected_value
                        )));
                    }
                } else {
                    return Err(PyErr::new::<MissingRequiredClaimError, _>(format!(
                        "Claim '{}' does not match the expected value '{}'",
                        key, expected_value
                    )));
                }
            }
        }

        // Check TTL validation
        if let Some(ttl) = self.ttl {
            let now = std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .map_err(|_| PyErr::new::<InvalidOperation, _>("System time error"))?
                .as_secs() as i64;

            if let Some(iat_value) = payload.get("iat") {
                let iat = iat_value.as_i64().ok_or_else(|| {
                    PyErr::new::<MissingRequiredClaimError, _>("Missing 'iat' claim for TTL validation")
                })?;

                if (now - iat) > ttl as i64 {
                    return Err(PyErr::new::<ExpiredTokenError, _>(
                        "Token has expired"
                    ));
                }


            } else {
                return Err(PyErr::new::<MissingRequiredClaimError, _>("Missing 'iat' claim for TTL validation"));

            }
        }

        Ok(())
    }
}

#[pymethods]
impl TokenValidation {
    #[new]
    #[pyo3(signature = (
        required_spec_claims = None, 
        leeway = None, 
        reject_tokens_expiring_in_less_than = None, 
        validate_exp = None, 
        validate_nbf = None, 
        validate_aud = None, 
        aud = None, 
        iss = None, 
        sub = None, 
        algorithms = None, 
        validate_signature = None, 
        exclude_headers = None, 
        block = None, 
        claims = None, 
        ttl = None,
        kid = None,
    ))]
    pub fn new(
        required_spec_claims: Option<Vec<String>>,
        leeway: Option<u64>,
        reject_tokens_expiring_in_less_than: Option<u64>,
        validate_exp: Option<bool>,
        validate_nbf: Option<bool>,
        validate_aud: Option<bool>,
        aud: Option<Vec<String>>,
        iss: Option<Vec<String>>,
        sub: Option<String>,
        algorithms: Option<Vec<String>>,
        validate_signature: Option<bool>,
        exclude_headers: Option<Vec<String>>,
        block: Option<HashMap<String, Vec<String>>>,
        claims: Option<HashMap<String, String>>,
        ttl: Option<u64>,
        kid: Option<String>,
    ) -> Self {
        TokenValidation {
            required_spec_claims: required_spec_claims.unwrap_or_else(|| vec!["exp".to_string()]),
            leeway: leeway.unwrap_or(60),
            reject_tokens_expiring_in_less_than: reject_tokens_expiring_in_less_than.unwrap_or(0),
            validate_exp: validate_exp.unwrap_or(false),
            validate_nbf: validate_nbf.unwrap_or(false),
            validate_aud: validate_aud.unwrap_or(true),
            aud: aud.unwrap_or_else(Vec::new),
            iss: iss.unwrap_or_else(Vec::new),
            sub,
            kid,
            algorithms: algorithms.unwrap_or_else(|| vec!["RS256".to_string()]),
            validate_signature: validate_signature.unwrap_or(true),
            exclude_headers: exclude_headers.unwrap_or_else(Vec::new),
            block: block.unwrap_or_else(HashMap::new),
            claims: claims.unwrap_or_else(HashMap::new),
            ttl,
        }
    }


    fn rest_block(&mut self, block: &Bound<'_, PyDict>) -> PyResult<()> {
        self.block.clear();
        for (key, value) in block.iter() {
            let key: String = key.extract()?;
            let value: Vec<String> = value.downcast::<PyList>()?.extract()?;
            self.block.insert(key, value);
        }
        Ok(())
    }

    fn reset_claims(&mut self, claims: &Bound<'_, PyDict>) -> PyResult<()> {
        self.claims.clear();
        for (key, value) in claims.iter() {
            let key: String = key.extract()?;
            let value: String = value.extract()?;
            self.claims.insert(key, value);
        }
        Ok(())
    }

}