import unittest
from main import calculate_pi


class TestCalculatePi(unittest.TestCase):
    """Test cases for the calculate_pi function"""
    
    def test_pi_value(self):
        """Test that calculate_pi returns the correct value of pi to 5 decimal places"""
        result = calculate_pi()
        expected = 3.14159
        self.assertEqual(result, expected)
    
    def test_pi_type(self):
        """Test that calculate_pi returns a float"""
        result = calculate_pi()
        self.assertIsInstance(result, float)
    
    def test_pi_precision(self):
        """Test that the result has at most 5 decimal places"""
        result = calculate_pi()
        # Convert to string and check decimal places
        result_str = str(result)
        if '.' in result_str:
            decimal_part = result_str.split('.')[1]
            self.assertLessEqual(len(decimal_part), 5)
    
    def test_pi_range(self):
        """Test that pi is within a reasonable range"""
        result = calculate_pi()
        self.assertGreater(result, 3.14)
        self.assertLess(result, 3.15)
    
    def test_pi_accuracy(self):
        """Test that the calculated value is close to the known value of pi"""
        import math
        result = calculate_pi()
        actual_pi = math.pi
        # Should be accurate to at least 5 decimal places
        self.assertAlmostEqual(result, actual_pi, places=5)


if __name__ == '__main__':
    unittest.main()
