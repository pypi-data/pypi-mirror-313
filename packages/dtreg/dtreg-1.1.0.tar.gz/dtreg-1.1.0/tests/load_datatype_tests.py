import unittest
from dtreg.load_datatype import load_datatype


class TestLoadDatatype(unittest.TestCase):

    def test_load_nonstatic(self):
        dt = load_datatype("https://doi.org/21.T11969/1ea0e148d9bbe08335cd")
        self.assertEqual(next(iter(dt.__dict__)), 'pidinst_schemaobject')

    def test_load_prop_epic(self):
        dt = load_datatype("https://doi.org/21.T11969/31483624b5c80014b6c7")
        props = dt.matrix_size.prop_list
        expected = ['number_of_rows', 'number_of_columns']
        self.assertEqual(props, expected)

    def test_load_prop_orkg(self):
        dt = load_datatype("https://orkg.org/template/R758316")
        props = dt.dtreg_test_template2.prop_list
        expected = ['property3', 'label']
        self.assertEqual(props, expected)


if __name__ == '__main__':
    unittest.main()
