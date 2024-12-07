use pyo3::prelude::*;
use pyo3::{PyResult, PyErr, create_exception};
use pyo3::exceptions::PyValueError;
use pyo3::types::{PyDict};

use rsa::{RsaPrivateKey, RsaPublicKey};
use rsa::pkcs1::{DecodeRsaPrivateKey};
use rsa::pkcs8::{DecodePublicKey};
use rsa::traits::{PrivateKeyParts, PublicKeyParts};

use base64::engine::general_purpose::{STANDARD, URL_SAFE_NO_PAD};
use base64::Engine;

use sha2::{Digest, Sha256};

use serde_json::{json};

use jsonwebtoken::{ Header, decode, Validation, decode_header, DecodingKey};
use jsonwebtoken::errors::ErrorKind;

use std::collections::{ HashSet};
use std::{ str};

pub mod key_store;
pub mod token_validation;
pub mod utils;
pub mod token_header;

pub use utils::{parse_algorithm, convert_dict_to_map};
pub use key_store::{KeyStore};
pub use token_validation::TokenValidation;
pub use token_header::TokenHeader;

use crate::key_store::{KeyNotFoundError, DuplicateKeyError, InvalidKeyFormat, NotFound};
use crate::token_validation::{ExpiredTokenError, MissingMatchClaimError, BlockedKeyError};
use crate::utils::{UnsupportedAlgorithm};

// Define all custom exceptions
create_exception!(key_manager, InvalidTokenError, PyValueError);
create_exception!(key_manager, DecodeError, PyValueError);
create_exception!(key_manager, InvalidSignatureError, PyValueError);
create_exception!(key_manager, ExpiredSignatureError, PyValueError);
create_exception!(key_manager, InvalidAudienceError, PyValueError);
create_exception!(key_manager, InvalidIssuerError, PyValueError);
create_exception!(key_manager, InvalidIssuedAtError, PyValueError);
create_exception!(key_manager, ImmatureSignatureError, PyValueError);
create_exception!(key_manager, InvalidKeyError, PyValueError);
create_exception!(key_manager, InvalidAlgorithmError, PyValueError);
create_exception!(key_manager, MissingRequiredClaimError, PyValueError);
create_exception!(key_manager, InvalidOperation, PyValueError);


#[pyclass]
pub struct KeyManager {
    key_store: KeyStore
}

impl KeyManager {
    fn extract_header(token: &str) -> Result<Header, PyErr> {
        decode_header(token)
            .map_err(|_| PyErr::new::<InvalidTokenError, _>("Invalid token header"))
    }

    fn configure_jwt_validation(
        validation: &TokenValidation,
    ) -> PyResult<Validation> {
       

        let algorithm = validation.algorithms.get(0).ok_or_else(|| {
            PyErr::new::<InvalidOperation, _>("Algorithm must be specified")
        })?;
        // Create JWT validation object
        let mut jwt_validation = Validation::new(parse_algorithm(&algorithm)?);

        // Disable signature validation if specified
        if !validation.validate_signature {
            println!("Warning: Disabling signature validation");
            jwt_validation.insecure_disable_signature_validation();
        }

        // Configure JWT validation based on the `TokenValidation` object
        jwt_validation.validate_exp = validation.validate_exp;
        jwt_validation.validate_nbf = validation.validate_nbf;
        jwt_validation.validate_aud = validation.validate_aud;
        jwt_validation.leeway = validation.leeway;
        jwt_validation.required_spec_claims = validation
            .required_spec_claims
            .iter()
            .cloned()
            .collect::<HashSet<String>>();

        if !validation.aud.is_empty() {
            jwt_validation.set_audience(validation.aud.as_slice());
        }
        // check if issuers empty or not
        if !validation.iss.is_empty() {
            jwt_validation.set_issuer(validation.iss.as_slice());
        }
     


        Ok(jwt_validation)
    }

    fn build_jwt_header(header: &TokenHeader) -> PyResult<Header> {
        // Parse the algorithm from the TokenHeader
        let parsed_algorithm = parse_algorithm(&header.alg)?;

        // Construct the JWT Header
        let mut jwt_header = Header::new(parsed_algorithm);

        // Populate JWT Header fields from TokenHeader
        jwt_header.kid = header.kid.clone();
        jwt_header.typ = header.typ.clone();
        jwt_header.cty = header.cty.clone();
        jwt_header.x5t = header.x5t.clone();
        jwt_header.x5c = header.x5c.clone();
        jwt_header.jku = header.jku.clone();
        Ok(jwt_header)
    }

    fn process_claims(
        token_data: jsonwebtoken::TokenData<serde_json::Value>,
        validation: &TokenValidation,
    ) -> PyResult<PyObject> {
        Python::with_gil(|py| {
           

            let claims = token_data.claims.as_object().ok_or_else(|| {
                PyErr::new::<InvalidOperation, _>("Invalid token_data decode:")
            })?;

            validation.validate_payload(claims).map_err(|e| {
                PyErr::new::<InvalidOperation, _>(format!("Invalid claims: {}", e))
            })?;

            let py_dict = PyDict::new(py);
            for (key, value) in claims {
                py_dict.set_item(key, value.to_string()).map_err(|e| {
                    PyErr::new::<InvalidOperation, _>(format!("Invalid claims while converting them to dict: {}", e))
                })?;
            }
            Ok(py_dict.into())
        })
    }


    fn map_decode_error(e: &jsonwebtoken::errors::Error) -> PyErr {
        match e.kind() {
            ErrorKind::InvalidToken => PyErr::new::<InvalidTokenError, _>(format!("Invalid token: {}", e)),
            ErrorKind::InvalidSignature => PyErr::new::<InvalidSignatureError, _>(format!("Invalid signature: {}", e)),
            ErrorKind::InvalidEcdsaKey => PyErr::new::<InvalidKeyError, _>(format!("Invalid ECDSA key: {}", e)),
            ErrorKind::InvalidRsaKey(_) => PyErr::new::<InvalidKeyError, _>(format!("Invalid RSA key: {}", e)),
            ErrorKind::RsaFailedSigning => PyErr::new::<InvalidOperation, _>(format!("RSA signing failed: {}", e)),
            ErrorKind::InvalidAlgorithmName => PyErr::new::<InvalidAlgorithmError, _>(format!("Invalid algorithm name: {}", e)),
            ErrorKind::InvalidKeyFormat => PyErr::new::<InvalidKeyError, _>(format!("Invalid key format: {}", e)),
            ErrorKind::MissingRequiredClaim(c) => PyErr::new::<MissingRequiredClaimError, _>(format!("Missing required claim: {}:{}", e, c)),
            ErrorKind::ExpiredSignature => PyErr::new::<ExpiredSignatureError, _>(format!("Token has expired: {}", e)),
            ErrorKind::InvalidIssuer => PyErr::new::<InvalidIssuerError, _>(format!("Invalid issuer: {}", e)),
            ErrorKind::InvalidAudience => PyErr::new::<InvalidAudienceError, _>(format!("Invalid audience: {}", e)),
            ErrorKind::InvalidSubject => PyErr::new::<InvalidIssuerError, _>(format!("Invalid subject: {}", e)), // Reusing InvalidIssuerError for subject-related issues
            ErrorKind::ImmatureSignature => PyErr::new::<ImmatureSignatureError, _>(format!("Token is not valid yet: {}", e)),
            ErrorKind::InvalidAlgorithm => PyErr::new::<InvalidAlgorithmError, _>(format!("Invalid algorithm: {}", e)),
            ErrorKind::MissingAlgorithm => PyErr::new::<InvalidAlgorithmError, _>(format!("Missing algorithm: {}", e)),
            _ => PyErr::new::<InvalidOperation, _>(format!("Invalid Operation: {}", e)), // Default case
        }
    }
}


#[pymethods]
impl KeyManager {
    #[new]
     pub fn new(key_store:&Bound<'_, KeyStore> ) -> PyResult<Self> {
        let key_store_ref: KeyStore = key_store.as_ref().extract()?;
        Ok(KeyManager {
            key_store: key_store_ref
        })
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
            .map_err(|e| PyErr::new::<DecodeError, _>(format!("Failed to decode Base64 key: {}", e )))?;

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
        Err(PyErr::new::<DecodeError, _>("The provided key is neither a valid public nor private key in PEM format" ))
    }


    #[staticmethod]
    #[pyo3(signature = (pem_key, key_type, algorithm=None))]
    pub fn pem_to_jwk(pem_key: String, key_type: String, algorithm: Option<String>) -> PyResult<Py<PyDict>> {
        // Parse the RSA key based on the specified key type
        let alg = algorithm.unwrap_or_else(|| "RS256".to_string());
        let _algorithm = parse_algorithm(&alg)?;
    

        let (n, e, d, p, q) = if key_type == "private" {
            let private_key = RsaPrivateKey::from_pkcs1_pem(&pem_key)
            .map_err(|e| PyErr::new::<InvalidOperation, _>(format!("Invalid private key format: {}", e )))?;
            (
                private_key.n().to_bytes_be(),
                private_key.e().to_bytes_be(),
                Some(private_key.d().to_bytes_be()),
                Some(private_key.primes()[0].to_bytes_be()),
                Some(private_key.primes()[1].to_bytes_be()),
            )
        } else if key_type == "public" {
            let public_key = RsaPublicKey::from_public_key_pem(&pem_key)
                .map_err(|e| PyErr::new::<InvalidOperation, _>(format!("Invalid public RSA key format: {}", e )))?;
            (
                public_key.n().to_bytes_be(),
                public_key.e().to_bytes_be(),
                None,
                None,
                None,
            )
        } else {
            return Err(PyErr::new::<InvalidOperation, _>( "Invalid key type; must be 'public' or 'private'"))
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
                    .map_err(|e| PyErr::new::<DecodeError, _>(format!("Failed to construct JWK {}", e )))?;
            }
            Ok(py_dict.into())
        })
    }

    #[staticmethod]
    #[pyo3(signature = (token, public_key, validation))]
    fn verify_token(
        token: &str,
        public_key: &str,
        validation: &mut TokenValidation,
    ) -> PyResult<PyObject> {
      
        let jwt_validation = Self::configure_jwt_validation(validation)?;
       
        let decoding_key = DecodingKey::from_rsa_pem(public_key.as_bytes())
            .map_err(|e| PyErr::new::<InvalidKeyError, _>(format!("Invalid key format: {}", e)))?;

        match decode::<serde_json::Value>(token, &decoding_key, &jwt_validation) {
            Ok(token_data) => Self::process_claims(token_data, &validation),            
            Err(e) => Err(Self::map_decode_error(&e)),
        }
    }

    fn verify_token_by_kid(
        &self,
        token: &str,
        validation: &mut TokenValidation,
    ) -> PyResult<PyObject> {

        let header = Self::extract_header(token)?;
        let binding = header.kid.clone();
        let kid = binding.as_deref();
      
        let expected_algorithm = self
            .key_store
            .get_algorithm(kid)?
            .to_string();

        validation.algorithms = vec![expected_algorithm];


        let jwt_validation = Self::configure_jwt_validation(validation)?;
        let decoding_key = self.key_store.get_decoded_public_key(kid)?;

        match decode::<serde_json::Value>(token, &decoding_key, &jwt_validation) {
            Ok(token_data) => Self::process_claims(token_data, &validation),            
            Err(e) => Err(Self::map_decode_error(&e)),
        }
    }

    #[staticmethod]
    #[pyo3(signature = (private_key, claims, header))]
    fn generate_token(
        private_key: &str,
        claims: &Bound<'_, PyDict>,
        header: &TokenHeader,
    ) -> PyResult<String> {
        // Build the JWT header using the utility function
        let jwt_header = Self::build_jwt_header(header)?;
        let claims_map = convert_dict_to_map(claims)?;
        let encoding_key =
            jsonwebtoken::EncodingKey::from_rsa_pem(private_key.as_bytes())
            .map_err(|e| PyErr::new::<InvalidOperation, _>(format!("Failed to parse private key: {}", e )))?;
        

        let token = jsonwebtoken::encode(&jwt_header, &claims_map, &encoding_key)
            .map_err(|e| PyErr::new::<InvalidOperation, _>(format!("Failed to encode token: {}", e )))?;

        Ok(token)
    }

    fn generate_token_by_kid(
        &self,
        claims: &Bound<'_, PyDict>,
        header: &mut TokenHeader,
    ) -> PyResult<String> {
      
        if header.kid.is_none() {
            return Err(PyErr::new::<InvalidOperation, _>("Token kid must be specified"));
        }
        let kid = header.kid.as_ref().unwrap();
        let algorithm = self.key_store
            .get_algorithm(Some(kid))
            .map_err(|e| PyErr::new::<InvalidOperation, _>(format!("Failed to retrieve algorithm for kid {}: {}", kid, e )))?;
   
        header.alg = algorithm;
        let jwt_header = Self::build_jwt_header(header)?;
        let claims_map = convert_dict_to_map(claims)?;
       
        let encoding_key = self.key_store
            .get_encoding_private_key(Some(kid))
            .map_err(|e| PyErr::new::<InvalidOperation, _>(format!("Failed to retrieve private key for kid {}: {}", kid, e )))?;

        let token = jsonwebtoken::encode(&jwt_header, &claims_map, &encoding_key)
            .map_err(|e| PyErr::new::<InvalidOperation, _>(format!("Failed to encode token: {}", e )))?;

        Ok(token)

    }

}







// /// A Python module implemented in Rust
#[pymodule]
fn key_manager(py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<KeyStore>()?;
    m.add_class::<KeyManager>()?;
    m.add_class::<TokenHeader>()?;
    m.add_class::<TokenValidation>()?;

    // Add exceptions
    m.add("MissingMatchClaimError", py.get_type::<MissingMatchClaimError>())?;
    m.add("DecodeError", py.get_type::<DecodeError>())?;
    m.add("BlockedKeyError", py.get_type::<BlockedKeyError>())?;
    m.add("ExpiredTokenError", py.get_type::<ExpiredTokenError>())?;
    m.add("InvalidTokenError", py.get_type::<InvalidTokenError>())?;
    m.add("ExpiredSignatureError", py.get_type::<ExpiredSignatureError>())?;
    m.add("ImmatureSignatureError", py.get_type::<ImmatureSignatureError>())?;
    m.add("InvalidAudienceError", py.get_type::<InvalidAudienceError>())?;
    m.add("InvalidIssuerError", py.get_type::<InvalidIssuerError>())?;
    m.add("InvalidOperation", py.get_type::<InvalidOperation>())?;

    m.add("MissingRequiredClaimError", py.get_type::<MissingRequiredClaimError>())?;
    m.add("InvalidKeyError", py.get_type::<InvalidKeyError>())?;
    m.add("InvalidAlgorithmError", py.get_type::<InvalidAlgorithmError>())?;
    m.add("InvalidSignatureError", py.get_type::<InvalidSignatureError>())?;
    m.add("InvalidIssuedAtError", py.get_type::<InvalidIssuedAtError>())?;
    m.add("UnsupportedAlgorithm", py.get_type::<UnsupportedAlgorithm>())?;
    m.add("KeyNotFoundError", py.get_type::<KeyNotFoundError>())?;
    m.add("DuplicateKeyError", py.get_type::<DuplicateKeyError>())?;
    m.add("InvalidKeyFormat", py.get_type::<InvalidKeyFormat>())?;
    m.add("NotFound", py.get_type::<NotFound>())?;

    Ok(())
}
