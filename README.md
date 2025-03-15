# Quantum Factoring with Shor's Algorithm Simulation

## Overview
This Python program simulates Shor's algorithm to factor large numbers using quantum computing principles. It leverages the Qiskit library to create and simulate quantum circuits, employing Quantum Phase Estimation (QPE) to determine the order of a number modulo \(N\). This order is then used to compute factors classically. The code is set to factor the number 3072 by default, but it can be adapted to factor other numbers by modifying the `original_N` variable.

## Key Features
- **Quantum Simulation:** Simulates quantum circuits for order finding using Qiskit.
- **Classical Processing:** Applies classical algorithms to derive factors and generate all divisors from the quantum results.
- **Flexible Output:** Displays the sequence of factors found and a complete list of divisors in ascending order.

## Requirements
To run this code, install the following Python libraries:
- `numpy`
- `qiskit`
- `qiskit-aer`

The `fractions`, `itertools`, and `math` modules are part of Python's standard library and require no additional installation.

### Install the required libraries with pip:
```bash
pip install numpy qiskit qiskit-aer
```

## Code Structure
The code is organized into several key functions:

### `modular_exponentiation(base, exponent, mod)`
Computes $(\text{base}^{\text{exponent}}) \mod \text{mod}$ efficiently using Python's `pow` function.

### `classical_multiplication_gate(mod_result)`
Creates a 4-qubit quantum gate that applies a precomputed modular multiplication result to the work register.

### `find_order(a, N)`
Implements Quantum Phase Estimation to find the order \(r\) of \(a\) modulo \(N\). It constructs an 8-qubit circuit (4 counting qubits, 4 work qubits), applies controlled modular multiplications, performs an inverse Quantum Fourier Transform (QFT), and measures the phase to estimate \(r\).

### `is_prime(n)`
Checks if a number is prime using a simple trial division method.

### `prime_factorize(n)`
Returns a dictionary of prime factors and their exponents for a given number.

### `generate_divisors(prime_factors)`
Generates all divisors from a prime factorization using combinations of exponents via `itertools.product`.

## Main Loop
Iteratively factors \(N\) using the order from QPE, collecting factors in a list until \(N = 1\).

## Output Processing
Prints the sequence of factors and computes the complete prime factorization to generate and display all divisors.

---

## How It Works
### **Initialization**
- The number to factor is set as `original_N = 3072`, and the base is `a = 2`.

### **Factoring Process**
While \(N > 1\):
1. If \(N\) is prime, it is added to the factor list, and \(N\) is set to 1.
2. Otherwise, QPE finds the order \(r\) of \(a\) modulo \(N\).
3. If \(r\) is even, potential factors are computed using:
$\gcd(a^{r/2} - 1, N)$ and $\gcd(a^{r/2} + 1, N)$
4. A valid factor (between 1 and \(N\)) is appended to the list, and \(N\) is divided by this factor.
5. If no factor is found, \(a\) is incremented.

### **Output Generation**
- The sequence of factors is printed (e.g., `The factors found for 3072 are: 6 8 2 8 2 2`).
- The prime factorization of each factor is computed and combined to form the complete prime factorization of `original_N`.
- All divisors are generated from the prime factorization and printed in ascending order (e.g., `All divisors of 3072: 1, 2, 3, 4, 6, 8, 12, ...`).

---

## Usage
### **Running the Code**
Execute the script in a Python environment with the required libraries installed:
```bash
python script_name.py
```
The simulation will run, and the output will display the factors and divisors.

### **Customizing the Number**
Change `original_N` at the top of the script to factor a different number:
```python
original_N = 1234  # Replace with your number
N = original_N
```
> **Note:** Larger numbers may require more qubits or computational resources, which could exceed this simulation's scope.

### **Expected Output**
Two lines will be printed:
1. **Factors found during the simulation** (order may vary due to quantum randomness).
2. **All divisors of `original_N` in ascending order.**

#### **Example for 3072:**
```bash
The factors found for 3072 are: 6 8 2 8 2 2
All divisors of 3072: 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512, 768, 1024, 1536, 3072
```

---

## Notes
### **Simulation Limits**
- The code uses an 8-qubit circuit (4 counting, 4 work), suitable for small numbers like 3072.
- Larger numbers require more qubits, which may be impractical for classical simulation.

### **Randomness**
- The factor sequence may differ across runs due to the probabilistic nature of quantum simulation, but the product of factors always equals `original_N`.

### **Divisors**
- The divisor list is deterministic, derived from the prime factorization, and always accurate.

