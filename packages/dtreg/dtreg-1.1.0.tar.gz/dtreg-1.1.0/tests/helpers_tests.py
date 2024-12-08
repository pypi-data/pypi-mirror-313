import unittest
from dtreg.helpers import format_string, get_prefix, generate_uid, specify_cardinality


class TestHelpers(unittest.TestCase):

    def test_format_string(self):
        self.assertEqual(format_string("a-B c"), "a_b_c")

    def test_prefix_epic(self):
        self.assertEqual(get_prefix("https://doi.org/21.T11969/74bc7748b8cd520908bc"),
                         "https://doi.org/21.T11969/")

    def test_prefix_orkg(self):
        self.assertEqual(get_prefix("https://incubating.orkg.org/template/R855534"),
                         "https://incubating.orkg.org/")

    def test_specify_cardinality_one(self):
        self.assertEqual(specify_cardinality("1"), {'min': 1, 'max': 1})

    def test_specify_cardinality_two(self):
        self.assertEqual(specify_cardinality("0 - 1"), {'min': 0, 'max': 1})

    def test_uid(self):
        self.assertEqual(str(type(generate_uid())), "<class 'function'>")

    def test_specify_cardinality_n(self):
        self.assertEqual(specify_cardinality("1 - n"), {'min': 1, 'max': None})


if __name__ == '__main__':
    unittest.main()
