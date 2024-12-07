use pyo3::prelude::*;
use pyo3::{PyResult, PyErr};
use pyo3::exceptions::PyValueError;
use pyo3::types::{PyDict, PyList};
use pyo3::create_exception;

use rsa::{RsaPrivateKey, RsaPublicKey};
use rsa::pkcs1::{DecodeRsaPrivateKey};
use rsa::pkcs8::{DecodePublicKey, EncodePrivateKey, DecodePrivateKey, EncodePublicKey, LineEnding};
use rsa::traits::{PrivateKeyParts, PublicKeyParts};

use base64::engine::general_purpose::{STANDARD, URL_SAFE_NO_PAD};
use base64::Engine;

use sha2::{Digest, Sha256};

use serde_json::{json, Value};

use jsonwebtoken::{Algorithm, Header, decode, Validation, decode_header, DecodingKey};
use jsonwebtoken::errors::ErrorKind;

use std::collections::{HashMap, HashSet};
use std::{fs, str};

// Define all custom exceptions
create_exception!(key_manager, InvalidTokenError, PyValueError);
create_exception!(key_manager, ExpiredSignatureError, PyValueError);
create_exception!(key_manager, ExpiredToken, PyValueError);
create_exception!(key_manager, ImmatureSignatureError, PyValueError);
create_exception!(key_manager, InvalidAudienceError, PyValueError);
create_exception!(key_manager, InvalidIssuerError, PyValueError);
create_exception!(key_manager, MissingRequiredClaimError, PyValueError);
create_exception!(key_manager, MissingMatchClaimError, PyValueError);
create_exception!(key_manager, DecodeError, PyValueError);
create_exception!(key_manager, BlockedKeyError, PyValueError);
create_exception!(key_manager, InvalidKeyError, PyValueError);
create_exception!(key_manager, InvalidAlgorithmError, PyValueError);
create_exception!(key_manager, PyJWTError, PyValueError);


#[pyclass]
struct TokenValidation {
    #[pyo3(get, set)]
    required_spec_claims: Vec<String>,
    #[pyo3(get, set)]
    leeway: u64,
    #[pyo3(get, set)]
    reject_tokens_expiring_in_less_than: u64,
    #[pyo3(get, set)]
    validate_exp: bool,
    #[pyo3(get, set)]
    validate_nbf: bool,
    #[pyo3(get, set)]
    validate_aud: bool,
    #[pyo3(get, set)]
    aud: Option<Vec<String>>,
    #[pyo3(get, set)]
    iss: Option<Vec<String>>,
    #[pyo3(get, set)]
    sub: Option<String>,
    #[pyo3(get, set)]
    algorithms: Vec<String>,
    #[pyo3(get, set)]
    validate_signature: bool,
    #[pyo3(get, set)]
    exclude_headers: Vec<String>,
    #[pyo3(get, set)]
    block: HashMap<String, Vec<String>>,
    #[pyo3(get, set)]
    claims: HashMap<String, String>,
    #[pyo3(get, set)]
    ttl: Option<u64>, // Added the ttl field
}

impl TokenValidation {
    fn validate_payload(&self, payload: &serde_json::Map<String, Value>) -> PyResult<()> {
        // Check if block validation is enabled

        if !self.block.is_empty(){
            for (key, blocked_list_values) in &self.block {
                if let Some(actual_value) = payload.get(key) {
                    let actual_value = serde_json::to_string(actual_value)
                        .map_err(|_| PyValueError::new_err("Failed to convert claim value to string"))?
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
                        .map_err(|_| PyValueError::new_err("Failed to convert claim value to string"))?
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
                .map_err(|_| PyValueError::new_err("System time error"))?
                .as_secs() as i64;

            if let Some(iat_value) = payload.get("iat") {
                let iat = iat_value.as_i64().ok_or_else(|| {
                    PyErr::new::<MissingRequiredClaimError, _>("Missing 'iat' claim for TTL validation")
                })?;

                if (now - iat) > ttl as i64 {
                    return Err(PyErr::new::<ExpiredToken, _>(
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
    fn new() -> Self {
        // Default validation object
        TokenValidation {
            required_spec_claims: vec!["exp".to_string()],
            leeway: 60,
            reject_tokens_expiring_in_less_than: 0,
            validate_exp: false,
            validate_nbf: false,
            validate_aud: true,
            aud: None,
            iss: None,
            sub: None,
            algorithms: vec!["RS256".to_string()],
            validate_signature: true,
            exclude_headers: vec![],
            block: HashMap::new(),
            claims: HashMap::new(),
            ttl: None,
        }
    }

    fn update_block(&mut self, block: &Bound<'_, PyDict>) -> PyResult<()> {
        self.block.clear();
        for (key, value) in block.iter() {
            let key: String = key.extract()?;
            let value: Vec<String> = value.downcast::<PyList>()?.extract()?;
            self.block.insert(key, value);
        }
        Ok(())
    }

    fn update_claims(&mut self, claims: &Bound<'_, PyDict>) -> PyResult<()> {
        self.claims.clear();
        for (key, value) in claims.iter() {
            let key: String = key.extract()?;
            let value: String = value.extract()?;
            self.claims.insert(key, value);
        }
        Ok(())
    }



    fn as_dict(&self, py: Python) -> PyObject {
        let dict = PyDict::new(py);

        dict.set_item("required_spec_claims", &self.required_spec_claims).unwrap();
        dict.set_item("leeway", self.leeway).unwrap();
        dict.set_item("reject_tokens_expiring_in_less_than", self.reject_tokens_expiring_in_less_than).unwrap();
        dict.set_item("validate_exp", self.validate_exp).unwrap();
        dict.set_item("validate_nbf", self.validate_nbf).unwrap();
        dict.set_item("validate_aud", self.validate_aud).unwrap();
        dict.set_item("aud", &self.aud).unwrap();
        dict.set_item("iss", &self.iss).unwrap();
        dict.set_item("sub", &self.sub).unwrap();
        dict.set_item("algorithms", &self.algorithms).unwrap();
        dict.set_item("validate_signature", self.validate_signature).unwrap();
        dict.set_item("exclude_headers", &self.exclude_headers).unwrap();
        dict.set_item("block", &self.block).unwrap();
        dict.set_item("claims", &self.claims).unwrap();

        dict.into()
    }
}


#[pyclass]
#[derive(Clone)] // Add Clone here
pub struct KeyStore {
    inner: InnerKeyStore,
}

#[derive(Default, Clone)]
pub struct InnerKeyStore {
    private_keys: HashMap<String, RsaPrivateKey>,
    public_keys: HashMap<String, RsaPublicKey>,
    algorithms: HashMap<String, String>,
    default_kid: Option<String>,
}

#[pymethods]
impl KeyStore {
    #[new]
    pub fn new() -> Self {
        KeyStore {
            inner: InnerKeyStore::default(),
        }
    }

    pub fn clone_inner(&self) -> KeyStore {
        KeyStore {
            inner: self.inner.clone(),
        }
    }

    pub fn register_keys(
        &mut self, // Use &mut self for mutability
        kid: String,
        private_pem: String,
        public_pem: String,
        algorithm: String,
        is_default: bool,
    ) -> PyResult<()> {
        let private_key = match RsaPrivateKey::from_pkcs1_pem(&private_pem) {
            Ok(key) => key,
            Err(_) => {
                // Fallback to PKCS#8 if PKCS#1 fails
                RsaPrivateKey::from_pkcs8_pem(&private_pem).map_err(|_| {
                    PyValueError::new_err("Invalid private key format. Tried both PKCS#1 and PKCS#8.")
                })?
            }
        };
        let public_key = RsaPublicKey::from_public_key_pem(&public_pem)
            .map_err(|_| PyValueError::new_err("Invalid public key format"))?;
        let parsed_algorithm = parse_algorithm(&algorithm)?;

        if self.inner.private_keys.contains_key(&kid) {
            return Err(PyValueError::new_err(format!("Key ID '{}' already exists", kid)));
        }

        self.inner.private_keys.insert(kid.clone(), private_key);
        self.inner.public_keys.insert(kid.clone(), public_key);
        self.inner
            .algorithms
            .insert(kid.clone(), format!("{:?}", parsed_algorithm));

        if is_default {
            if self.inner.default_kid.is_some() {
                return Err(PyValueError::new_err("Default key already set"));
            }
            self.inner.default_kid = Some(kid.clone());
        }

        Ok(())
    }

    pub fn load_keys(
        &mut self, // Use &mut self for mutability
        kid: String,
        private_key_path: String,
        public_key_path: String,
        algorithm: String,
        is_default: bool,
    ) -> PyResult<()> {
        let private_key_pem = fs::read_to_string(&private_key_path).map_err(|_| {
            PyValueError::new_err(format!("Failed to read private key file: {}", private_key_path))
        })?;
        let public_key_pem = fs::read_to_string(&public_key_path).map_err(|_| {
            PyValueError::new_err(format!("Failed to read public key file: {}", public_key_path))
        })?;

        self.register_keys(kid, private_key_pem, public_key_pem, algorithm, is_default)
    }

    #[pyo3(signature = (kid=None))]
    pub fn get_kid(&self, kid: Option<&str>) -> PyResult<String> {
        match kid {
            Some(kid) if self.inner.private_keys.contains_key(kid) => Ok(kid.to_string()),
            _ => self
                .inner
                .default_kid
                .clone()
                .ok_or_else(|| PyValueError::new_err("No default key available")),
        }
    }

    #[pyo3(signature = (kid=None))]
    pub fn get_public_key(&self, kid: Option<&str>) -> PyResult<String> {
        let key_id = self.get_kid(kid)?;
        let public_key = self.inner.public_keys.get(&key_id).ok_or_else(|| {
            PyValueError::new_err(format!("No public key found for key ID: {}", key_id))
        })?;

        public_key
            .to_public_key_pem(LineEnding::default())
            .map_err(|e| PyValueError::new_err(format!("Failed to encode public key to PEM: {}", e)))
    }

    #[pyo3(signature = (kid=None))]
    pub fn get_private_key(&self, kid: Option<&str>) -> PyResult<String> {
        let key_id = self.get_kid(kid)?;
        let private_key = self.inner.private_keys.get(&key_id).ok_or_else(|| {
            PyValueError::new_err(format!("No private key found for key ID: {}", key_id))
        })?;

        private_key
            .to_pkcs8_pem(LineEnding::default())
            .map(|pem| pem.to_string())
            .map_err(|e| PyValueError::new_err(format!("Failed to encode private key to PEM: {}", e)))
    }

    #[pyo3(signature = (kid=None))]
    pub fn get_algorithm(&self, kid: Option<&str>) -> PyResult<String> {
        let key_id = self.get_kid(kid)?;
        let algorithm = self.inner.algorithms.get(&key_id).ok_or_else(|| {
            PyValueError::new_err(format!("No algorithm found for key ID: {}", key_id))
        })?;
        Ok(algorithm.clone())
    }

}

// PyO3-exposed KeyManager class
#[pyclass]
pub struct KeyManager {
    key_store: KeyStore
}

impl KeyManager {
    fn extract_header(token: &str) -> Result<Header, PyErr> {
        decode_header(token)
            .map_err(|_| PyErr::new::<InvalidTokenError, _>("Invalid token header"))
    }



     /// Validates the token header, ensuring the algorithm and `kid` match expectations
    fn validate_header(&self, token: &str) -> Result<String, PyErr> {
        // Extract the header from the token
        let header = KeyManager::extract_header(token)?;
        let binding = header.kid.clone();
        let kid = binding.as_deref().unwrap_or("");
        let store = self.get_key_store();

        // Retrieve expected algorithm from the key store
        let expected_algorithm = store.get_algorithm(Some(kid))?;

        let algorithm = format!("{:?}", header.alg);
        // Compare the expected algorithm with the header algorithm
        if algorithm != expected_algorithm {
            return Err(PyErr::new::<InvalidTokenError, _>(format!(
                "Algorithm mismatch for kid {}. Expected: {}, Found: {}",
                kid, expected_algorithm, algorithm
            )));
        }

        Ok(algorithm.to_string())
    }

}

#[pymethods]
impl KeyManager {
    #[new]
    pub fn new(py: Python, key_store: Py<KeyStore>) -> PyResult<Self> {
        let key_store_inner = key_store.borrow(py).clone_inner();
        Ok(KeyManager {
            key_store: key_store_inner,
        })
    }

    pub fn get_key_store(&self) -> KeyStore {
        self.key_store.clone()
    }

    #[staticmethod]
    pub fn decode_key(key_base64: String) -> PyResult<String> {

        let cleaned_key = key_base64
            .lines() // Remove all newlines
            .collect::<String>() // Join lines into a single string
            .replace('\r', ""); // Remove carriage returns

        // Base64 padding if necessary
        let safe_base64 = {
            let mut key = cleaned_key.clone();
            let padding = key.len() % 4;
            if padding > 0 {
                key.push_str(&"=".repeat(4 - padding));
            }
            key
        };

        // Base64 decode the key
        let decoded_key = STANDARD
            .decode(&safe_base64)
            .map_err(|e| PyValueError::new_err(format!("Failed to decode Base64 key: {}", e)))?;


        // Check if the decoded key is a valid public key PEM
        if let Ok(pem) = str::from_utf8(&decoded_key) {
            if RsaPublicKey::from_public_key_pem(pem).is_ok() {
                return Ok(pem.to_string());
            }
        }

        // Check if the decoded key is a valid private key PEM
        if let Ok(pem) = str::from_utf8(&decoded_key) {
            if RsaPrivateKey::from_pkcs1_pem(pem).is_ok() {
                return Ok(pem.to_string());
            }
        }

        // If neither decoding succeeded, return an error
        Err(PyValueError::new_err(
            "The provided key is neither a valid public nor private key in PEM format.",
        ))
    }

    #[staticmethod]
    #[pyo3(signature = (pem_key, key_type, algorithm=None))]
    pub fn pem_to_jwk(pem_key: String, key_type: String, algorithm: Option<String>) -> PyResult<Py<PyDict>> {
        // Parse the RSA key based on the specified key type
        let alg = algorithm.unwrap_or_else(|| "RS256".to_string());

        let supported_algorithms = ["RS256", "RS384", "RS512"];
        if !supported_algorithms.contains(&alg.as_str()) {
            return Err(PyValueError::new_err(format!(
                "Unsupported algorithm: {}. Supported algorithms are: {:?}",
                alg, supported_algorithms
            )));
        }

        let (n, e, d, p, q) = if key_type == "private" {
            let private_key = RsaPrivateKey::from_pkcs1_pem(&pem_key)
                .map_err(|_| PyValueError::new_err("Invalid private key format"))?;
            (
                private_key.n().to_bytes_be(),
                private_key.e().to_bytes_be(),
                Some(private_key.d().to_bytes_be()),
                Some(private_key.primes()[0].to_bytes_be()),
                Some(private_key.primes()[1].to_bytes_be()),
            )
        } else if key_type == "public" {
            let public_key = RsaPublicKey::from_public_key_pem(&pem_key)
                .map_err(|_| PyValueError::new_err("Invalid public RSA key format"))?;
            (
                public_key.n().to_bytes_be(),
                public_key.e().to_bytes_be(),
                None,
                None,
                None,
            )
        } else {
            return Err(PyValueError::new_err(
                "Invalid key type; must be 'public' or 'private'",
            ));
        };

        // Encode modulus and exponent
        let n = URL_SAFE_NO_PAD.encode(n);
        let e = URL_SAFE_NO_PAD.encode(e);

        // Generate a unique Key ID (kid)
        let kid = {
            let mut hasher = Sha256::new();
            hasher.update(n.as_bytes());
            format!("{:x}", hasher.finalize())[0..8].to_string()
        };

        // Construct the JWK
        let mut jwk = json!({
            "kty": "RSA",
            "n": n,
            "e": e,
            "alg": "RS256",
            "use": "sig",
            "kid": kid
        });

        // Add private key components if available
        if let (Some(d), Some(p), Some(q)) = (d, p, q) {
            let d = URL_SAFE_NO_PAD.encode(d);
            let p = URL_SAFE_NO_PAD.encode(p);
            let q = URL_SAFE_NO_PAD.encode(q);
            jwk["d"] = json!(d);
            jwk["p"] = json!(p);
            jwk["q"] = json!(q);
        }

        // Convert JWK to PyDict
        Python::with_gil(|py| {
            let py_dict = PyDict::new(py);
            for (key, value) in jwk.as_object().unwrap() {
                py_dict
                    .set_item(key, value.as_str().unwrap_or("").to_string())
                    .map_err(|_| PyValueError::new_err("Failed to construct JWK"))?;
            }
            Ok(py_dict.into())
        })
    }

    #[staticmethod]
    #[pyo3(signature = (token, public_key, validation, algorithm=None))]
    fn verify_token(
        token: &str,
        public_key: &str,
        validation: &TokenValidation,
        algorithm: Option<String>,
    ) -> PyResult<PyObject> {
        let header = KeyManager::extract_header(token)
        .map_err(|e| map_error_to_pyjwt_exception("Invalid token", Some(&e)))?;

        let algo = algorithm.unwrap_or_else(|| "RS256".to_string());
        if format!("{:?}", header.alg) != algo {
            return Err(map_error_to_pyjwt_exception("Invalid algorithm",   None::<&String>
        ));
        }

        let mut jwt_validation = Validation::new(parse_algorithm(&algo)?);

        // if !validation.validate_signature {
        //     println!("Warning Disabling signature validation");
        //     jwt_validation.insecure_disable_signature_validation();
        // }

        // Map fields from TokenValidation to Validation
        jwt_validation.validate_exp = validation.validate_exp;
        jwt_validation.validate_nbf = validation.validate_nbf;
        jwt_validation.validate_aud = validation.validate_aud;
        jwt_validation.required_spec_claims = validation
            .required_spec_claims
            .iter()
            .cloned()
            .collect::<HashSet<String>>();
        jwt_validation.leeway = validation.leeway;

        if let Some(audiences) = &validation.aud {
            jwt_validation.set_audience(audiences);
        }

        if let Some(issuers) = &validation.iss {
            jwt_validation.set_issuer(issuers);
        }

        let decoding_key = DecodingKey::from_rsa_pem(public_key.as_bytes())
            .map_err(|e| map_error_to_pyjwt_exception("Invalid key", Some(&e)))?;

        match decode::<serde_json::Value>(token, &decoding_key, &jwt_validation) {
            Ok(token_data) => {

                Python::with_gil(|py| {
                    let claims = token_data.claims.as_object().ok_or_else(|| {
                        map_error_to_pyjwt_exception("Decoding error",   None::<&String>
                    )
                    })?;

                    validation.validate_payload(claims).map_err(|e| {
                        map_error_to_pyjwt_exception( "Decoding error", Some(&e))
                    })?;

                    let py_dict = PyDict::new(py);
                    for (key, value) in claims {
                        py_dict.set_item(key, value.to_string()).map_err(|e| {
                            map_error_to_pyjwt_exception("Decoding error", Some(&e))
                        })?;
                    }
                    Ok(py_dict.into())
                })

            }
            Err(e) => match e.kind() {
                ErrorKind::ExpiredSignature => Err(map_error_to_pyjwt_exception("Token has expired", Some(&e))),
                ErrorKind::InvalidToken => Err(map_error_to_pyjwt_exception("Invalid token", Some(&e))),
                _ => Err(map_error_to_pyjwt_exception("General decoding error", Some(&e))),
            },
        }
    }

    fn verify_token_by_kid(
        &self,
        token: &str,
        kid: &str,
        validation: &TokenValidation,
    ) -> PyResult<PyObject> {
        let store = self.get_key_store();
        let algorithm = self
            .validate_header(token)
            .map_err(|e| PyValueError::new_err(format!("Header validation failed: {}", e)))?;
        let public_key = store
            .get_public_key(Some(kid))
            .map_err(|e| PyValueError::new_err(format!("Failed to retrieve public key for kid {}: {}", kid, e)))?;
        Self::verify_token(token, &public_key, &validation, Some(algorithm))
    }

    #[staticmethod]
    #[pyo3(signature = (private_key, claims, algorithm=None , kid=None))]
    fn generate_token(
        private_key: &str,
        claims: &Bound<'_, PyDict>,
        algorithm: Option<String>,
        kid: Option<String>,
    ) -> PyResult<String> {

        // Parse algorithm or use default
        let alg = algorithm.unwrap_or_else(|| "RS256".to_string());
        let parsed_algorithm = parse_algorithm(&alg)?;

        // Construct JWT header
        let mut header = Header::default();
        header.alg = parsed_algorithm;
        if let Some(kid) = kid {
            header.kid = Some(kid);
        }

        let mut claims_map = serde_json::Map::new();
        for (key, value) in claims {
            let key = key
                .extract::<String>()
                .map_err(|_| PyValueError::new_err("Claim key must be a string"))?;

            if key == "exp" || key == "iat" {
                let exp_value: i64 = value
                    .extract()
                    .map_err(|_| PyValueError::new_err("Expiration ('exp') must be an integer"))?;
                claims_map.insert(key, Value::Number(exp_value.into()));
            } else {
                // For other claims, convert to string as before
                let value = serde_json::to_value(value.to_string())
                    .map_err(|_| PyValueError::new_err("Failed to serialize claim value"))?;
                claims_map.insert(key, value);
            }

        }

        // Encode the token
        let encoding_key =
            jsonwebtoken::EncodingKey::from_rsa_pem(private_key.as_bytes()).map_err(|e| {
                PyValueError::new_err(format!("Failed to parse private key: {}", e))
            })?;

        let token = jsonwebtoken::encode(&header, &claims_map, &encoding_key)
            .map_err(|e| PyValueError::new_err(format!("Failed to encode token: {}", e)))?;

        Ok(token)
    }

    fn generate_token_by_kid(
        &self,
        kid: &str,
        claims: &Bound<'_, PyDict>,
    ) -> PyResult<String> {
        let store = self.get_key_store();

        // Get algorithm for the given kid
        let algorithm = store
            .get_algorithm(Some(kid))
            .map_err(|e| PyValueError::new_err(format!("Failed to retrieve algorithm for kid {}: {}", kid, e)))?;

        // Get private key for the given kid
        let private_key = store
            .get_private_key(Some(kid))
            .map_err(|e| PyValueError::new_err(format!("Failed to retrieve private key for kid {}: {}", kid, e)))?;

        // Generate the token
        let token = Self::generate_token(
            &private_key,
            claims,
            Some(algorithm),
            Some(kid.to_string()),
        );

        Ok(token?)
    }

}

fn parse_algorithm(alg: &str) -> PyResult<Algorithm> {
    match alg {
        "RS256" => Ok(Algorithm::RS256),
        "RS384" => Ok(Algorithm::RS384),
        "RS512" => Ok(Algorithm::RS512),
        "HS256" => Ok(Algorithm::HS256),
        "HS384" => Ok(Algorithm::HS384),
        "HS512" => Ok(Algorithm::HS512),
        "ES256" => Ok(Algorithm::ES256),
        "ES384" => Ok(Algorithm::ES384),
        "PS256" => Ok(Algorithm::PS256),
        "PS384" => Ok(Algorithm::PS384),
        "PS512" => Ok(Algorithm::PS512),
        "EdDSA" => Ok(Algorithm::EdDSA),
        _ => Err(PyValueError::new_err(format!("Unsupported algorithm: {}", alg))),
    }
}


fn map_error_to_pyjwt_exception(msg: &str, original_error: Option<&impl std::fmt::Display>) -> PyErr {
    // Format the error message based on whether original_error is present
    let formatted_error = match original_error {
        Some(err) => format!("{}: {}", msg, err),
        None => msg.to_string(),
    };

    // TODO: fix the Error Mapping
    if formatted_error.contains("BlockedKeyError") {
        PyErr::new::<BlockedKeyError, _>(formatted_error)
    } else if formatted_error.contains("MissingMatchClaimError") {
        PyErr::new::<MissingMatchClaimError, _>(formatted_error)
    } else if formatted_error.contains("ExpiredToken") {
        PyErr::new::<ExpiredToken, _>(formatted_error)
    } else {
        // Match the primary error message and return the corresponding exception
        match msg {
            "Invalid token" => PyErr::new::<InvalidTokenError, _>(formatted_error),
            "Token has expired" => PyErr::new::<ExpiredSignatureError, _>(formatted_error),
            "Token is not valid yet" => PyErr::new::<ImmatureSignatureError, _>(formatted_error),
            "Invalid audience" => PyErr::new::<InvalidAudienceError, _>(formatted_error),
            "Invalid issuer" => PyErr::new::<InvalidIssuerError, _>(formatted_error),
            "Missing required claim" => PyErr::new::<MissingRequiredClaimError, _>(formatted_error),
            "Decoding error" => PyErr::new::<DecodeError, _>(formatted_error),
            "Invalid key" => PyErr::new::<InvalidKeyError, _>(formatted_error),
            "Invalid algorithm" => PyErr::new::<InvalidAlgorithmError, _>(formatted_error),
            _ => PyErr::new::<PyJWTError, _>(formatted_error), // Default case
        }
    }
}

// /// A Python module implemented in Rust
#[pymodule]
fn key_manager(py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<KeyStore>()?;
    m.add_class::<KeyManager>()?;
    m.add_class::<TokenValidation>()?;

    // Add exceptions
    m.add("MissingMatchClaimError", py.get_type::<MissingMatchClaimError>())?;
    m.add("DecodeError", py.get_type::<DecodeError>())?;
    m.add("BlockedKeyError", py.get_type::<BlockedKeyError>())?;
    m.add("ExpiredToken", py.get_type::<ExpiredToken>())?;
    m.add("InvalidTokenError", py.get_type::<InvalidTokenError>())?;
    m.add("ExpiredSignatureError", py.get_type::<ExpiredSignatureError>())?;
    m.add("ImmatureSignatureError", py.get_type::<ImmatureSignatureError>())?;
    m.add("InvalidAudienceError", py.get_type::<InvalidAudienceError>())?;
    m.add("InvalidIssuerError", py.get_type::<InvalidIssuerError>())?;
    m.add("MissingRequiredClaimError", py.get_type::<MissingRequiredClaimError>())?;
    m.add("DecodeError", py.get_type::<DecodeError>())?;
    m.add("InvalidKeyError", py.get_type::<InvalidKeyError>())?;
    m.add("InvalidAlgorithmError", py.get_type::<InvalidAlgorithmError>())?;
    m.add("PyJWTError", py.get_type::<PyJWTError>())?;
    Ok(())
}
