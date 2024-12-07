import unittest
from rtandcaskinetics.casmodel_func import compute_fluorescence, plot_fluorescence

class TestComputeFluorescence(unittest.TestCase):
    def test_valid_inputs(self):
        """Test the compute_fluorescence function with valid inputs."""
        forwardDNA = "TTTTTTTTTTTTTGATGATGTGAAGGTGTTGTCGTTTATTTATTTATTTATTTATTTCTATCTTTCCTCTTAATTCGACG"
        TemplateConc_nM = 5
        PrimerConc_nM = 50
        dNTPConc_nM = 100

        results = compute_fluorescence(forwardDNA, TemplateConc_nM, PrimerConc_nM, dNTPConc_nM)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        for time_mins, fluorescence in results:
            self.assertEqual(len(time_mins), len(fluorescence))
            self.assertTrue(all(f >= 0 for f in fluorescence), "Fluorescence values should be non-negative.")

    def test_zero_primer_concentration(self):
        """Test edge case with zero primer concentration."""
        forwardDNA = "TTTTTTTTTTTTTGATGATGTGAAGGTGTTGTCGTTTATTTATTTATTTATTTATTTCTATCTTTCCTCTTAATTCGACG"
        TemplateConc_nM = 5 
        PrimerConc_nM = 0  # Zero primer concentration
        dNTPConc_nM = 100

        results = compute_fluorescence(forwardDNA, TemplateConc_nM, PrimerConc_nM, dNTPConc_nM)
        for time_mins, fluorescence in results:
            self.assertTrue(all(f == 0 for f in fluorescence), "Fluorescence should be zero when primer concentration is zero.")

    def test_invalid_dna_sequence(self):
        """Test compute_fluorescence with an invalid DNA sequence."""
        forwardDNA = "INVALID_DNA"
        TemplateConc_nM = 5
        PrimerConc_nM = 50
        dNTPConc_nM = 100

        with self.assertRaises(ValueError):
            compute_fluorescence(forwardDNA, TemplateConc_nM, PrimerConc_nM, dNTPConc_nM)

    def test_negative_concentration(self):
        """Test compute_fluorescence with negative concentration."""
        forwardDNA = "TTTTTTTTTTTTTGATGATGTGAAGGTGTTGTCGTTTATTTATTTATTTATTTATTTCTATCTTTCCTCTTAATTCGACG"
        TemplateConc_nM = -5 # Negative concentration
        PrimerConc_nM = 50
        dNTPConc_nM = 100

        with self.assertRaises(ValueError):
            compute_fluorescence(forwardDNA, TemplateConc_nM, PrimerConc_nM, dNTPConc_nM)

    def test_fluorescence_data_length(self):
        """Test that compute_fluorescence returns consistent data lengths."""
        forwardDNA = "TTTTTTTTTTTTTGATGATGTGAAGGTGTTGTCGTTTATTTATTTATTTATTTATTTCTATCTTTCCTCTTAATTCGACG"
        TemplateConc_nM = 5
        PrimerConc_nM = 50
        dNTPConc_nM = 100

        results = compute_fluorescence(forwardDNA, TemplateConc_nM, PrimerConc_nM, dNTPConc_nM)
        for time_mins, fluorescence in results:
            self.assertEqual(len(time_mins), len(fluorescence), "Time and fluorescence data lengths should match.")

class TestPlotFluorescence(unittest.TestCase):
    def test_plot_fluorescence(self):
        """Test that plot_fluorescence runs without error."""
        forwardDNA = "TTTTTTTTTTTTTGATGATGTGAAGGTGTTGTCGTTTATTTATTTATTTATTTATTTCTATCTTTCCTCTTAATTCGACG"
        TemplateConc_nM = 5
        PrimerConc_nM = 50
        dNTPConc_nM = 100

        results = compute_fluorescence(forwardDNA, TemplateConc_nM, PrimerConc_nM, dNTPConc_nM)

        try:
            plot_fluorescence(results)
        except Exception as e:
            self.fail(f"plot_fluorescence raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
