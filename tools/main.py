def greeting():
    print("Hi there")

def calculate_pi():
    """
    Calculate pi to the 5th digit using the Machin formula.
    Formula: pi/4 = 4*arctan(1/5) - arctan(1/239)
    Returns pi rounded to 5 decimal places (3.14159)
    """
    def arctan(x, num_terms=50):
        """Calculate arctan using Taylor series expansion"""
        result = 0
        for n in range(num_terms):
            term = ((-1) ** n) * (x ** (2 * n + 1)) / (2 * n + 1)
            result += term
        return result
    
    # Machin's formula for calculating pi
    pi = 4 * (4 * arctan(1/5) - arctan(1/239))
    
    # Round to 5 decimal places
    pi_5_digits = round(pi, 5)
    
    return pi_5_digits