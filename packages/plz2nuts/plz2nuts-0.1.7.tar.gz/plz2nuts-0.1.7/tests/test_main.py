import unittest
import plz_to_nuts.main as plz2nuts
import argparse
from unittest.mock import patch

class TestMain(unittest.TestCase):
    def test_replace_german_umlauts(self):
        self.assertEqual(plz2nuts.replace_german_umlauts("äöüß"), "aeoeuess")
        self.assertEqual(plz2nuts.replace_german_umlauts("ÄÖÜ"), "AeOeUe")
        self.assertEqual(plz2nuts.replace_german_umlauts(""), "")
        self.assertEqual(plz2nuts.replace_german_umlauts("hello"), "hello")


    def test_get_region_by_prefix(self):
        result = plz2nuts.get_region_by_prefix("10")
        self.assertIsInstance(result, dict)
        self.assertIn('place_name', result)
        self.assertIn('community_name', result)

        # Test with an invalid prefix
        result = plz2nuts.get_region_by_prefix("99999")
        self.assertEqual(result, {})

        # Test with an empty prefix
        result = plz2nuts.get_region_by_prefix("")
        self.assertEqual(result, {})


    def test_get_nuts(self):
    # Mock nuts_dict to ensure consistent results
        with patch('plz_to_nuts.main.nuts_dict', {'Berlin': 'DE300'}):
            # Test with a valid region dictionary
            region_dict = {'place_name': 'Berlin', 'community_name': 'Berlin, Kreisfreie Stadt'}
            result = plz2nuts.get_nuts(region_dict)
            self.assertEqual(result, 'DE300')

            # Test with an invalid region dictionary
            region_dict = {'place_name': 'Invalid', 'community_name': 'Invalid'}
            result = plz2nuts.get_nuts(region_dict)
            self.assertEqual(result, "Not Found")

            # Test with an empty dictionary
            region_dict = {}
            result = plz2nuts.get_nuts(region_dict)
            self.assertEqual(result, "Not Found")

            # Test with missing keys in the dictionary
            region_dict = {'place_name': 'Berlin'}
            result = plz2nuts.get_nuts(region_dict)
            self.assertEqual(result, "Not Found")


    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')  # Mock print to capture CLI output
    def test_plz2nuts_cli(self, mock_print, mock_parse_args):
        # Mock the command-line arguments
        mock_parse_args.return_value = argparse.Namespace(postal_code='10115')

        # Mock get_region_by_prefix and get_nuts to control their behavior
        with patch('plz_to_nuts.main.get_region_by_prefix') as mock_get_region, \
            patch('plz_to_nuts.main.get_nuts') as mock_get_nuts:
            
            mock_get_region.return_value = {'place_name': 'Berlin', 'community_name': 'Berlin'}
            mock_get_nuts.return_value = 'DE300'

            # Run the CLI function
            plz2nuts.plz2nuts_cli()

            # Check if print was called with the expected output
            mock_print.assert_called_with('DE300')

        # Test with invalid postal code (mocking behavior)
        mock_parse_args.return_value = argparse.Namespace(postal_code='99999')
        mock_get_region.return_value = {}
        
        plz2nuts.plz2nuts_cli()
        
        mock_print.assert_called_with("No region found for the given postal code.")


if __name__ == "__main__":
    unittest.main()
