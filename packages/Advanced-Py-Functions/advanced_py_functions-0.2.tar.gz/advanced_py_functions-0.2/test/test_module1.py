import unittest
from My_Py_Package.module1 import custom_sort_dicts, fibonacci, is_palindrome

class TestModule1(unittest.TestCase):
    
    def test_custom_sort_dicts(self):
        data = [{'value': 5, 'name': 'apple'}, {'value': 3, 'name': 'banana'}, {'value': 8, 'name': 'orange'}]
        sorted_data = custom_sort_dicts(data)
        self.assertEqual(sorted_data, [{'value': 3, 'name': 'banana'}, {'value': 5, 'name': 'apple'}, {'value': 8, 'name': 'orange'}])
    
    def test_fibonacci(self):
        self.assertEqual(fibonacci(10), 55)
        self.assertEqual(fibonacci(20), 6765)
    
    def test_is_palindrome(self):
        self.assertTrue(is_palindrome("madam"))
        self.assertFalse(is_palindrome("hello"))

if __name__ == '__main__':
    unittest.main()
