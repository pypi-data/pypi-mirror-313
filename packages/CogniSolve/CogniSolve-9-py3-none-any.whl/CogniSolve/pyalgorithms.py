
def factorial(n : int) -> int:
    """Calculates the factorial of a non-negative integer.

    Args:
        n: A non-negative integer.

    Returns:
        The factorial of n.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is negative.
    """
    if not isinstance(n, int): raise TypeError("Input must be an integer.")
    if n < 0: raise ValueError("Input must be a non-negative integer.")

    s = 1
    for i in range(2, n + 1): s *= i
    return s

def binomial_coefficient(n: int, k: int) -> int:
    """Calculates the binomial coefficient C(n, k), also known as "n choose k".

    Args:
        n: The total number of items.
        k: The number of items to choose.

    Returns:
        The binomial coefficient C(n, k).

    Raises:
        TypeError: If n or k are not integers.
        ValueError: If n or k are negative, or if k > n.
    """
    if not (isinstance(n, int) and isinstance(k, int)): raise TypeError("Inputs n and k must be integers.")
    if n < 0 or k < 0: raise ValueError("Inputs n and k must be non-negative integers.")
    if k > n: raise ValueError("k cannot be greater than n.")
    
    return factorial(n) // (factorial(k) * factorial(n - k))

def Pascal_triangle(n: int) -> list:
    """Generates the n-th row of Pascal's triangle.

    Args:
      n: The row index (0-based) of Pascal's triangle to generate.

    Returns:
      A list representing the n-th row of Pascal's triangle.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is negative.
    """
    if not isinstance(n, int): raise TypeError("Input n must be an integer.")
    if n < 0: raise ValueError("Input n must be a non-negative integer.")

    l = [1]
    for i in range(n): l = [sum(x) for x in zip([0] + l, l + [0])]
    return l

def binary_gcd(n1: int, n2: int) -> int:
    """Calculates the greatest common divisor (GCD) of two non-negative integers
    using the binary GCD algorithm.

    Args:
        n1: A non-negative integer.
        n2: A non-negative integer.

    Returns:
        The greatest common divisor of n1 and n2.

    Raises:
        TypeError: If either n1 or n2 is not an integer.
        ValueError: If either n1 or n2 is negative.
    """
    if not (isinstance(n1, int) and isinstance(n2, int)): raise TypeError("Inputs must be integers.")
    if n1 < 0 or n2 < 0: raise ValueError("Inputs must be non-negative integers.")

    if n1 == 0: return n2
    if n2 == 0:  return n1
    sh = 0
    while (n1 | n2) & 1 == 0:
        sh += 1
        n1 >>= 1
        n2 >>= 1
    while n2 != 0:
        while n2 & 1 == 0:
            n2 >>= 1
        if n1 > n2:
            n1, n2 = n2, n1
        n2 -= n1
    return n1 << sh

def is_prime(n: int) -> bool:
    """Checks if a given non-negative integer is a prime number.

    Args:
        n: A non-negative integer.

    Returns:
        True if n is a prime number, False otherwise.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is negative.
    """
    if not isinstance(n, int): raise TypeError("Input must be an integer.")
    if n < 0: raise ValueError("Input must be a non-negative integer.")

    if n <= 1: return False
    if n == 2: return True
    if n % 2 == 0: return False
    j = 3
    while j * j <= n:
        if n % j == 0: return False
        j += 2
    return True

def EratosfenSieve(n : int) -> list:
    """Generates a list of prime numbers up to (but not including) a given integer
    using the Sieve of Eratosthenes algorithm.

    Args:
        n: An integer greater than 1. The upper limit (exclusive) for prime number generation.

    Returns:
        A list of prime numbers less than n.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is less than or equal to 1.
    """
    if not isinstance(n, int): raise TypeError("Input must be an integer.")
    if n <= 1: raise ValueError("Input must be an integer greater than 1.")
    
    l = list(range(n - 1))
    l[1] = 0
    for i in l:
        if i > 1:
            for j in range(2 * i, len(l), i):
                l[j] = 0
    return [e for e in l if e != 0]

import heapq

def heuristic(a : tuple, b: tuple) -> int:
    """Calculates the Manhattan distance between two points.

    Args:
        a: The first point (x1, y1).
        b: The second point (x2, y2).

    Returns:
        The Manhattan distance between a and b.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(array : list, start : tuple, goal : tuple) -> "list | bool":
    """Finds the shortest path from a start point to a goal point in a 2D grid using the A* search algorithm.

    Args:
        array: A 2D grid representing the environment. 0 represents walkable cells, and 1 represents obstacles.
        start: The starting point (x, y).
        goal: The goal point (x, y).

    Returns:
        A list of tuples representing the shortest path from start to goal if a path is found, otherwise False.
    """
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []
    heapq.heappush(oheap, (fscore[start], start))
    
    while oheap:
        current = heapq.heappop(oheap)[1]
        
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data[::-1]
        
        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + 1
            
            if 0 <= neighbor[0] < len(array):
                if 0 <= neighbor[1] < len(array[0]):
                    if array[neighbor[0]][neighbor[1]] == 1: continue
                else: continue
            else: continue
                
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0): continue
                
            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))
    return False

def prime_factors(n: int) -> list:
    """
    Computes the prime factorization of a given integer.

    This function takes a positive integer 'n' as input and returns a list of its prime factors in ascending order.

    Args:
        n: The input positive integer.

    Returns:
        A list of integers representing the prime factors of 'n'.
    """
    factors = []
    divisor = 2
    while n > 1:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
            if n > 1 and is_prime(n) :
                return factors + [n]
        divisor += 1
        if divisor * divisor > n and n > 1:
            factors.append(n)
            break
    return factors

def smallest_number_from_digits(n : int) -> int:
    """Constructs the smallest possible number using digits obtained from prime factorization of n.

    This function takes a positive integer 'n' as input and attempts to find the smallest number that can be formed by concatenating the digits of its prime factors in ascending order. 
    For instance, if n = 12 (2 * 2 * 3), the function would return 223.

    Args:
        n: The input positive integer.

    Returns:
       The smallest number formed from the digits of the prime factors of n, sorted in ascending order.
       Returns -1 if no such number can be formed (i.e., if n has a prime factor greater than 9).
       Returns 10 if n is 0.
       Returns 1 if n is 1.
    """

    if n == 0: return 10
    if n == 1: return 1
    factors = []
    for digit in range(9, 1, -1):
        while n % digit == 0:
            factors.append(digit)
            n //= digit
    if n > 1: return -1
    factors.sort()
    return int("".join(map(str, factors)))
