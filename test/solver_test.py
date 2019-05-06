import unittest
from solver import solver

class PrimeGeneratorTest(unittest.TestCase):

    def setUp(self):
        self.available_primes = solver.primes(0,100)

    def test_solver_diagonal(self):
        solution = solver.main()
        self.assertIn((solution[(0,0)]+solution[(1,1)]+solution[(2,2)])/3, self.available_primes) # Make sure that the average of the numbers on the main diagonal are a prime number


if __name__ == '__main__':
    unittest.main()
