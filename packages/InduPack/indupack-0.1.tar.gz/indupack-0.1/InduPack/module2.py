import numpy as np

def validate_matrices(A, B):
    """Check if matrix multiplication is possible (i.e., A.columns == B.rows)."""
    return len(A[0]) == len(B)

def matrix_multiply(A, B):
    """Multiply two matrices A and B."""
    if not validate_matrices(A, B):
        raise ValueError("Matrices cannot be multiplied due to incompatible dimensions.")
    
    return np.dot(A, B)

def invert_matrix(A):
    """Invert a matrix (if possible)."""
    try:
        return np.linalg.inv(A)
    except np.linalg.LinAlgError:
        raise ValueError("Matrix is not invertible.")

def sieve_of_eratosthenes(limit):
    """Generate all prime numbers up to 'limit' using the Sieve of Eratosthenes."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False  # 0 and 1 are not prime
    for num in range(2, int(limit ** 0.5) + 1):
        if sieve[num]:
            for multiple in range(num * num, limit + 1, num):
                sieve[multiple] = False
    return [num for num, is_prime in enumerate(sieve) if is_prime]
