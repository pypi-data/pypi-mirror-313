import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt  # PyJWT
from key_manager import (
    ExpiredSignatureError,
    InvalidTokenError,
    TokenHeader,
    KeyManager,
    KeyStore,
    TokenValidation,
)

private_key_path = "private_key.pem"
public_key_path = "public_key.pem"

# Load keys from files
with open(private_key_path, "rb") as f:
    PRIVATE_KEY = f.read().decode("utf-8")

with open(public_key_path, "rb") as f:
    PUBLIC_KEY = f.read().decode("utf-8")

exp = datetime.now(timezone.utc) + timedelta(hours=1)
# Convert to Unix timestamp (seconds since epoch)
exp_timestamp = int(exp.timestamp())

# Claims to encode
claims = {
    "sub": "user123",
    "custom_claim": "example_value",
    "exp": exp_timestamp,
    "iat": int(time.time()) - 40
}


# Benchmark PyJWT
def benchmark_pyjwt():
    try:
        # Token generation
        start_gen = time.time()
        token = jwt.encode(claims, PRIVATE_KEY, algorithm="RS256")
        end_gen = time.time()

        # Token validation
        start_val = time.time()
        decoded = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
        end_val = time.time()

        print("PyJWT:")
        print(f"  Generation time: {end_gen - start_gen:.6f} seconds")
        print(f"  Validation time: {end_val - start_val:.6f} seconds")

        return {
            "generation_time": end_gen - start_gen,
            "validation_time": end_val - start_val,
            "token": token,
            "decoded": decoded,
        }
    except jwt.ExpiredSignatureError as e:
        print("PyJWT Exception: Token has expired." , e)
    except jwt.InvalidTokenError as e:
        print("PyJWT Exception: Invalid token.", e)
    except Exception as e:
        print(f"Unexpected PyJWT exception: benchmark_pyjwt {e}")


# Benchmark Rust-based package
def benchmark_key_manager_key_story():
    try:
        # Token generation
        key_store: KeyStore = KeyStore()
        kid = "default"
        algorithm = "RS256"
        key_store.load_keys(kid, str(Path(private_key_path).absolute()), str(Path(public_key_path).absolute()), algorithm, is_default=True)

        # get absulte value of the key

        key_manager = KeyManager(key_store)

        # Token generation
        start_gen = time.time()
        header = TokenHeader(alg="RS256", kid=kid)
        token = key_manager.generate_token_by_kid(header=header, claims=claims)
        end_gen = time.time()

        # Token validation
        validations = TokenValidation(kid=kid)
        start_val = time.time()
        decoded = key_manager.verify_token_by_kid(token=token, validation=validations)
        end_val = time.time()

        print("PyKeyStoreKeyManager:")
        print(f"  Generation time: {end_gen - start_gen:.6f} seconds")
        print(f"  Validation time: {end_val - start_val:.6f} seconds")

        return {
            "generation_time": end_gen - start_gen,
            "validation_time": end_val - start_val,
            "token": token,
            "decoded": decoded,
        }
    except ExpiredSignatureError as e:
        print("PyJWT Exception: Token has expired." , e)
    except InvalidTokenError as e:
        print("PyJWT Exception: Invalid token.", e)
    except Exception as e:
        print(f"Unexpected PyJWT exception: benchmark_key_manager_key_story {e}")


def benchmark_key_manager():
    try:
        # Token generation
        key_manager = KeyManager(key_store= KeyStore())

        # Token generation
        start_gen = time.time()
        header = TokenHeader()
        token = key_manager.generate_token(private_key=PRIVATE_KEY, claims=claims, header=header)
        end_gen = time.time()

        # Token validation
        validations = TokenValidation()
        start_val = time.time()
        decoded = key_manager.verify_token(token=token, public_key=PUBLIC_KEY,validation=validations)
        end_val = time.time()

        print("PyKeyManager:")
        print(f"  Generation time: {end_gen - start_gen:.6f} seconds")
        print(f"  Validation time: {end_val - start_val:.6f} seconds")

        return {
            "generation_time": end_gen - start_gen,
            "validation_time": end_val - start_val,
            "token": token,
            "decoded": decoded,
        }
    except ExpiredSignatureError as e:
        print("PyJWT Exception: Token has expired." , e)
    except InvalidTokenError as e:
        print("PyJWT Exception: Invalid token.", e)
    except Exception as e:
        print(f"Unexpected PyJWT exception: benchmark_key_manager {e}")

if __name__ == "__main__":
    print("Benchmarking PyJWT vs Rust-based RSA JWT\n")

    pyjwt_results = benchmark_pyjwt()
    key_manager_results = benchmark_key_manager()
    key_manager_key_story_results = benchmark_key_manager_key_story()

    # Check if results are available (in case of exceptions)
    if pyjwt_results and key_manager_results:
        # Calculate improvement factors
        gen_improvement = pyjwt_results["generation_time"] / key_manager_results["generation_time"]
        val_improvement = pyjwt_results["validation_time"] / key_manager_results["validation_time"]

        # Display results
        print("\nBenchmarking Results\n")

        print("PyJWT:")
        print(f"  Generation time: {pyjwt_results['generation_time']:.6f} seconds")
        print(f"  Validation time: {pyjwt_results['validation_time']:.6f} seconds")

        print("\nRust-based RSA JWT:")
        print(f"  Generation time: {key_manager_results['generation_time']:.6f} seconds")
        print(f"  Validation time: {key_manager_results['validation_time']:.6f} seconds")

        print("\nPerformance Comparison:")
        print(f"  Token generation: Rust is {gen_improvement:.2f}x faster than PyJWT")
        print(f"  Token validation: Rust is {val_improvement:.2f}x faster than PyJWT")



        store_key_gen_improvement = pyjwt_results["generation_time"] / key_manager_key_story_results["generation_time"]
        stor_key_val_improvement = pyjwt_results["validation_time"] / key_manager_key_story_results["validation_time"]

        # Display results
        print("\nBenchmarking Results for Manager Key Story Results\n")

        print("PyJWT:")
        print(f"  Generation time: {pyjwt_results['generation_time']:.6f} seconds")
        print(f"  Validation time: {pyjwt_results['validation_time']:.6f} seconds")

        print("\nRust-based KeyManager with KeyStore:")
        print(f"  Generation time: {key_manager_key_story_results['generation_time']:.6f} seconds")
        print(f"  Validation time: {key_manager_key_story_results['validation_time']:.6f} seconds")

        print("\nPerformance Comparison:")
        print(f"  Token generation: Rust is {store_key_gen_improvement:.2f}x faster than PyJWT")
        print(f"  Token validation: Rust is {stor_key_val_improvement:.2f}x faster than PyJWT")
