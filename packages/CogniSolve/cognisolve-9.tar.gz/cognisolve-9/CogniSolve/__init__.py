"""
Provides various algorithms and utility functions.

Available functions:

- astar: A* search algorithm.
- binary_gcd: Calculates the greatest common divisor using the binary GCD algorithm.
- binomial_coefficient: Calculates the binomial coefficient.
- EratosfenSieve: Generates prime numbers using the Sieve of Eratosthenes.
- factorial: Calculates the factorial of a number.
- heuristic: Heuristic function (purpose needs clarification).
- is_prime: Checks if a number is prime.
- Pascal_triangle: Generates Pascal's triangle.
- prime_factors: Finds the prime factors of a number.
- smallest_number_from_digits: Forms the smallest possible number from a given set of digits.

"""

__all__ = [
    "factorial",
    "binary_gcd",
    "is_prime",
    "EratosfenSieve",
    "heuristic",
    "astar",
    "binomial_coefficient",
    "Pascal_triangle",
    "smallest_number_from_digits",
    "prime_factors",
]

from .pyalgorithms import *
