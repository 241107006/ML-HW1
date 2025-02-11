from functools import reduce
import random
import unittest

# Function implementing the Chinese Remainder Theorem (CRT)
def chinese_remainder_theorem(remainders, moduli):
    total = 0
    prod = reduce(lambda a, b: a * b, moduli)  # Calculate the product of all moduli
    
    for remainder, modulus in zip(remainders, moduli):
        p = prod // modulus  # Compute partial product
        total += remainder * mul_inv(p, modulus) * p  # Apply the CRT formula
    
    return total % prod  # Return the smallest positive solution

# Function to compute the modular multiplicative inverse using Extended Euclidean Algorithm
def mul_inv(a, b):
    b0, x0, x1 = b, 0, 1  # Initialize values
    if b == 1:
        return 1  # If modulus is 1, the inverse is trivially 1
    while a > 1 and b > 0:
        q = a // b  # Compute quotient
        a, b = b, a % b  # Update values
        x0, x1 = x1 - q * x0, x0  # Update coefficients
    if x1 < 0:
        x1 += b0  # Ensure positive result
    return x1

# Function implementing the Miller-Rabin primality test
def miller_rabin(n, s):
    if n < 2:
        return False  # Numbers less than 2 are not prime
    if n in (2, 3):
        return True  # 2 and 3 are prime numbers
    if n % 2 == 0:
        return False  # Even numbers (except 2) are not prime

    # Express n-1 as 2^r * d where d is odd
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Perform s rounds of testing
    for _ in range(s):
        a = random.randint(2, n - 2)  # Pick a random base in range [2, n-2]
        x = pow(a, d, n)  # Compute a^d % n
        if x == 1 or x == n - 1:
            continue  # If x is 1 or -1, move to next iteration

        for _ in range(r - 1):  # Repeat squaring step
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # Composite number detected
    return True  # Probably prime

# Unit tests for the implemented functions
class TestAlgorithms(unittest.TestCase):
    # Test cases for Chinese Remainder Theorem
    def test_crt(self):
        self.assertEqual(chinese_remainder_theorem([2, 3, 2], [3, 5, 7]), 23)
        self.assertEqual(chinese_remainder_theorem([1, 2, 3], [2, 3, 5]), 23)
        self.assertEqual(chinese_remainder_theorem([0, 3, 4], [3, 4, 5]), 39)
        self.assertEqual(chinese_remainder_theorem([2, 3, 1], [3, 4, 5]), 11)
        self.assertEqual(chinese_remainder_theorem([0, 0, 0], [3, 5, 7]), 0)
        self.assertEqual(chinese_remainder_theorem([1, 1, 1], [2, 3, 5]), 1)
        self.assertEqual(chinese_remainder_theorem([3, 4, 5], [7, 11, 13]), 213)
        self.assertEqual(chinese_remainder_theorem([1, 2, 3, 4], [5, 7, 9, 11]), 1731)
        self.assertEqual(chinese_remainder_theorem([3, 2, 1], [4, 5, 6]), 62)
        self.assertEqual(chinese_remainder_theorem([5, 6, 7], [8, 9, 11]), 645)

    # Test cases for Miller-Rabin primality test
    def test_miller_rabin(self):
        self.assertTrue(miller_rabin(7, 5))
        self.assertTrue(miller_rabin(13, 5))
        self.assertTrue(miller_rabin(17, 5))
        self.assertTrue(miller_rabin(31, 5))
        self.assertTrue(miller_rabin(97, 5))
        self.assertFalse(miller_rabin(9, 5))
        self.assertFalse(miller_rabin(15, 5))
        self.assertFalse(miller_rabin(21, 5))
        self.assertFalse(miller_rabin(25, 5))
        self.assertFalse(miller_rabin(49, 5))

# Run the unit tests
if __name__ == "__main__":
    unittest.main()
