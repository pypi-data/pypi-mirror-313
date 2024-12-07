import unittest
import numpy as np
from My_Py_Package.module2 import matrix_multiply, invert_matrix, sieve_of_eratosthenes

class TestModule2(unittest.TestCase):
    
    def test_matrix_multiply(self):
        A = np.array([[1, 2], [3, 4]])
        B = np.array([[5, 6], [7, 8]])
        result = matrix_multiply(A, B)
        np.testing.assert_array_equal(result, np.array([[19, 22], [43, 50]]))
    
    def test_invert_matrix(self):
        A = np.array([[1, 2], [3, 4]])
        inv = invert_matrix(A)
        np.testing.assert_array_equal(np.dot(A, inv), np.eye(2))  # Should be close to identity matrix
    
    def test_sieve_of_eratosthenes(self):
        primes = sieve_of_eratosthenes(30)
        self.assertEqual(primes, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])

if __name__ == '__main__':
    unittest.main()
