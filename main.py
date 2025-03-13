import numpy as np
import math
from fractions import Fraction
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from numpy import pi
from itertools import product

# Initial number to factor and base
original_N = 3072
N = original_N
a = 2

# Modular exponentiation function
def modular_exponentiation(base, exponent, mod):
    """Computes (base ^ exponent) % mod efficiently."""
    return pow(base, exponent, mod)

# Classical multiplication gate for modular arithmetic
def classical_multiplication_gate(mod_result):
    """Creates a 4-qubit gate that applies a classical modular multiplication result."""
    qc = QuantumCircuit(4)
    for i in range(4):
        if (mod_result >> i) & 1:
            qc.x(i)
    return qc.to_gate(label=f"ModMul({mod_result})")

# Function to find the order of 'a' modulo 'N' using QPE
def find_order(a, N):
    """Uses Quantum Phase Estimation to find the order of 'a' modulo 'N'."""
    circuit = QuantumCircuit(8, 4)
    circuit.h(range(4))  # Superposition on counting qubits
    circuit.x(4)  # Initialize work register to |1>
    for i in range(4):
        exp = 2 ** i
        mod_result = modular_exponentiation(a, exp, N)
        circuit.append(classical_multiplication_gate(mod_result).control(), [i] + [4, 5, 6, 7])
    # Inverse QFT
    circuit.h(3)
    circuit.cp(-pi/2, 2, 3)
    circuit.cp(-pi/4, 1, 3)
    circuit.cp(-pi/8, 0, 3)
    circuit.h(2)
    circuit.cp(-pi/2, 1, 2)
    circuit.cp(-pi/4, 0, 2)
    circuit.h(1)
    circuit.cp(-pi/2, 0, 1)
    circuit.h(0)
    circuit.measure(range(4), range(4))
    simulator = Aer.get_backend('qasm_simulator')
    compiled = transpile(circuit, simulator)
    result = simulator.run(compiled, shots=1024).result()
    counts = result.get_counts()
    measured_value = max(counts, key=counts.get)
    j = int(measured_value[::-1], 2)
    phase = j / 16  # 2^4 counting qubits
    fraction = Fraction(phase).limit_denominator(N)
    return fraction.denominator

# Simple test to see if it's prime
def is_prime(n):
    """Returns True if 'n' is prime, False otherwise."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Function to compute prime factorization
def prime_factorize(n):
    """Returns a dictionary of prime factors and their exponents for a number n."""
    factors = {}
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n //= 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors[i] = factors.get(i, 0) + 1
            n //= i
        i += 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

# Function to generate all divisors from prime factors
def generate_divisors(prime_factors):
    """Generates all divisors from a dictionary of prime factors and exponents."""
    primes = list(prime_factors.keys())
    exponents = [range(exp + 1) for exp in prime_factors.values()]
    divisors = []
    for exp_comb in product(*exponents):
        divisor = 1
        for prime, exp in zip(primes, exp_comb):
            divisor *= prime ** exp
        divisors.append(divisor)
    return sorted(divisors)

# Main factoring loop with factor collection
factor_list = []
while N > 1:
    if is_prime(N):
        factor_list.append(N)
        N = 1
    else:
        r = find_order(a, N)
        if r % 2 == 0:
            factor1 = math.gcd(a**(r//2) - 1, N)
            factor2 = math.gcd(a**(r//2) + 1, N)
            if 1 < factor1 < N:
                factor_list.append(factor1)
                N //= factor1
            elif 1 < factor2 < N:
                factor_list.append(factor2)
                N //= factor2
            else:
                a += 1
        else:
            a += 1

# Output the factors found
print("The factors found for {} are: ".format(original_N), " ".join(map(str, factor_list)))

# Compute the complete prime factorization from the factors
total_factors = {}
for factor in factor_list:
    factor_factors = prime_factorize(factor)
    for prime, exp in factor_factors.items():
        total_factors[prime] = total_factors.get(prime, 0) + exp

# Generate and print all divisors
all_divisors = generate_divisors(total_factors)
print("All divisors of {}: ".format(original_N), ", ".join(map(str, all_divisors)))