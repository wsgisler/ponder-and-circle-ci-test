import unittest
from solver import solver

class PrimeGeneratorTest(unittest.TestCase):

    def setUp(self):
        print("Nothing")

    def test_prime_number_generation(self):
        prime_numbers = solver.primes(0,10)
        self.assertEqual(len(prime_numbers), 4) # There should be 4 prime numbers between 0 and 10
        prime_numbers = solver.primes(100,300)
        self.assertEqual(len(prime_numbers), 37) # There should be 37 prime numbers between 100 and 300

if __name__ == '__main__':
    unittest.main()
