use crate::key_store::errors::*;
use crate::utils::{parse_algorithm};

use jsonwebtoken::{DecodingKey, EncodingKey};

use pyo3::prelude::*;

use std::{fs, str};
use std::collections::HashMap;




#[pyclass]
#[derive(Clone)]
pub struct KeyStore {
    private_keys: HashMap<String, EncodingKey>,
    public_keys: HashMap<String, DecodingKey>,
    algorithms: HashMap<String, String>,
    private_key_pems: HashMap<String, String>,
    public_key_pems: HashMap<String, String>,
    default_kid: Option<String>,
}


impl KeyStore {
    

    pub fn get_encoding_private_key(&self, kid: Option<&str>) -> PyResult<EncodingKey> {
      
        let key_id = self.get_kid(kid)?;
        self
            .private_keys
            .get(&key_id)
            .cloned()
            .ok_or_else(|| PyErr::new::<NotFound, _>(format!(
                "No private key found for key ID: {}", key_id)))
    }

    pub fn get_decoded_public_key(&self, kid: Option<&str>) -> PyResult<DecodingKey> {
        let key_id = self.get_kid(kid)?;
        self
            .public_keys
            .get(&key_id)
            .cloned()
            .ok_or_else(|| PyErr::new::<NotFound, _>(format!(
                "No public key found for key ID: {}", key_id)))
    }
}

#[pymethods]
impl KeyStore {
   

    #[new]
    pub fn new() -> Self {
        Self {
            private_keys: HashMap::new(),
            public_keys: HashMap::new(),
            algorithms: HashMap::new(),
            private_key_pems: HashMap::new(),
            public_key_pems: HashMap::new(),
            default_kid: None,
        }
    }
    

    /// Register a private key
    pub fn register_private_key(
        &mut self,
        kid: String,
        private_pem: String,
        algorithm: String,
    ) -> PyResult<()> {
        // Check for duplicate key ID
        if self.private_keys.contains_key(&kid) {
            return Err(PyErr::new::<DuplicateKeyError, _>(format!(
                "Key ID '{}' already exists",
                kid
            )));
        }

        // Try to create EncodingKey from the private key PEM
        let encoding_key = EncodingKey::from_rsa_pem(private_pem.as_bytes())
            .map_err(|e| PyErr::new::<InvalidKeyFormat, _>(format!(
                "Invalid private key format: {}", e
            )))?;

        // Insert the key into the store
        self.private_keys.insert(kid.clone(), encoding_key);
        self.private_key_pems.insert(kid.clone(), private_pem);
        self.register_algorithm(kid, algorithm)?;

        Ok(())
    }

    // Register a public key
    pub fn register_public_key(
        &mut self,
        kid: String,
        public_pem: String,
        algorithm: String,
    ) -> PyResult<()> {
        if self.public_keys.contains_key(&kid) {
            return Err(PyErr::new::<DuplicateKeyError, _>(format!(
                "Key ID '{}' already exists",
                kid
            )));
        }

        let decoding_key = DecodingKey::from_rsa_pem(public_pem.as_bytes())
            .map_err(|e| PyErr::new::<InvalidKeyFormat, _>(format!(
                "Invalid private key format: {}", e
            )))?;

        self.public_keys.insert(kid.clone(), decoding_key);
        self.public_key_pems.insert(kid.clone(), public_pem);
        self.register_algorithm(kid, algorithm)?;

        Ok(())
    }

    pub fn register_algorithm(&mut self, kid: String, algorithm: String) -> PyResult<()> {
        if self.algorithms.contains_key(&kid) {
            return Ok(()); // Algorithm already registered
        }

        let parsed_algorithm = parse_algorithm(&algorithm)?;
        self.algorithms.insert(kid, format!("{:?}", parsed_algorithm));
        Ok(())
    }
  
    pub fn register_keys(
        &mut self, // Use &mut self for mutability
        kid: String,
        private_pem: String,
        public_pem: String,
        algorithm: String,
        is_default: bool,
    ) -> PyResult<()> {

        self.register_private_key(kid.clone(), private_pem, algorithm.clone())?;
        self.register_public_key(kid.clone(), public_pem, algorithm.clone())?;
        self.register_algorithm(kid.clone(), algorithm.clone())?;
        if is_default {
            if self.default_kid.is_some() {
                return Err(PyErr::new::<InvalidOperation, _>(format!(
                "Default key already set: {}", kid)))?;
            }
            self.default_kid = Some(kid);
        }


        Ok(())
    }

    pub fn load_keys(
        &mut self,
        kid: String,
        private_key_path: String,
        public_key_path: String,
        algorithm: String,
        is_default: bool,
    ) -> PyResult<()> {
        // Read the private key PEM from the file
        let private_key_pem = fs::read_to_string(&private_key_path).map_err(|e| {
            PyErr::new::<InvalidOperation, _>(format!(
                "Failed to read private key file '{}': {}",
                private_key_path, e
            ))
        })?;

        // Read the public key PEM from the file
        let public_key_pem = fs::read_to_string(&public_key_path).map_err(|e| {
            PyErr::new::<InvalidOperation, _>(format!(
                "Failed to read public key file '{}': {}",
                public_key_path, e
            ))
        })?;

        // Register the keys
        self.register_keys(kid, private_key_pem, public_key_pem, algorithm, is_default)
    }


    #[pyo3(signature = (kid=None))]
    pub fn get_private_key(&self, kid: Option<&str>) -> PyResult<String> {
        let key_id = self.get_kid(kid)?;
        self
            .private_key_pems
            .get(&key_id)
            .cloned()
            .ok_or_else(|| PyErr::new::<NotFound, _>(format!(
                "No private key found for key ID: {}",
                key_id
            )))
    }

    #[pyo3(signature = (kid=None))]
    pub fn get_public_key(&self, kid: Option<&str>) -> PyResult<String> {
        let key_id = self.get_kid(kid)?;
        self
            .public_key_pems
            .get(&key_id)
            .cloned()
            .ok_or_else(|| PyErr::new::<NotFound, _>(format!(
                "No public key found for key ID: {}", key_id)))
            
    }

    #[pyo3(signature = (kid=None))]
    pub fn get_algorithm(&self, kid: Option<&str>) -> PyResult<String> {
        let key_id = self.get_kid(kid)?; // Get the key ID, or the default one if `kid` is None

        // Retrieve the algorithm for the key ID and clone the value as a `String`
        self
            .algorithms
            .get(&key_id)
            .cloned() // Clone the `String` from the HashMap
            .ok_or_else(|| PyErr::new::<NotFound, _>(format!(
                "No algorithm found for key ID: {}", key_id
            )))
    }

    #[pyo3(signature = (kid=None))]
    pub fn get_kid(&self, kid: Option<&str>) -> PyResult<String> {
        match kid.or_else(|| self.default_kid.as_deref()) {
            Some(k) if self.private_keys.contains_key(k) => Ok(k.to_string()),
            Some(_) => Err(PyErr::new::<NotFound, _>(format!(
                "Specified key ID does not exist"
            ))),
            None => Err(PyErr::new::<NotFound, _>(format!(
                "No default key is set"
            ))),
        }
    }

}