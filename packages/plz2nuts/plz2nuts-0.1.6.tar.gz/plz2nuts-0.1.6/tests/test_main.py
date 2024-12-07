import unittest
import plz_to_nuts

class TestMain(unittest.TestCase):
    def test_replace_german_umlauts(self):
        self.assertEqual(plz_to_nuts.replace_german_umlauts("äöüß"), "aeoeuess")
        self.assertEqual(plz_to_nuts.replace_german_umlauts("ÄÖÜ"), "AeOeUe")

    def test_get_region_by_prefix(self):
        result = plz_to_nuts.get_region_by_prefix("10")
        self.assertIsInstance(result, dict)

if __name__ == "__main__":
    unittest.main()
