import unittest
from rtandcaskinetics.probability_func import calculate_dNTP_probability

class TestCalculateDNTPProbability(unittest.TestCase):
    
    def test_non_T_base(self):
        """Test calculation when base is not 'T'."""
        result = calculate_dNTP_probability('A', 10, 5, 2)
        self.assertEqual(result, 1.0, "Probability should be 1.0 for non-T bases regardless of inputs.")

    def test_T_base_with_non_zero_values(self):
        """Test calculation for base 'T' with valid NRTI_Conc and Kaff."""
        result = calculate_dNTP_probability('T', 10, 5, 2)
        expected_fraction = 10 / (10 + 2 * 5)
        self.assertAlmostEqual(result, expected_fraction, places=6, msg="Incorrect probability for base 'T'.")

    def test_edge_case_zero_dNTP_Conc(self):
        """Test calculation when dNTP_Conc=0 for base 'T'."""
        result = calculate_dNTP_probability('T', 0, 5, 2)
        self.assertEqual(result, 0.0, "Probability should be 0.0 when dNTP_Conc is 0.")

    def test_invalid_base(self):
        """Test invalid base input raises ValueError."""
        with self.assertRaises(ValueError):
            calculate_dNTP_probability('X', 10, 5, 2)

    def test_zero_NRTI_concentration(self):
        """Test calculation when NRTI_Conc is zero."""
        result = calculate_dNTP_probability('T', 10, 0, 2)
        self.assertAlmostEqual(result, 1.0, places=6, msg="Probability should be 1.0 when NRTI_Conc is 0.")

if __name__ == "__main__":
    unittest.main()
