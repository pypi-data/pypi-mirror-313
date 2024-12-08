import unittest
from dtreg.extract_orkg import extract_orkg


class TestExtractOrkg(unittest.TestCase):

    def test_extract_orkg(self):
        result = extract_orkg("https://orkg.org/template/R758316")
        expected = {'dtreg_test_template2': [[{'dt_name': 'dtreg_test_template2',
                                               'dt_id': 'R758316',
                                               'dt_class': 'C102007'}],
                                             [{'dtp_name': 'property3',
                                               'dtp_id': 'P160024',
                                               'dtp_card_min': 0,
                                               'dtp_card_max': None,
                                               'dtp_value_type': 'Integer'},
                                              {'dtp_name': 'label',
                                                 'dtp_id': 'label',
                                                 'dtp_card_min': 0,
                                                 'dtp_card_max': 1,
                                                 'dtp_value_type': 'string'}]]}
        self.assertEqual(result, expected)

    def test_extract_orkg_props(self):
        schema = extract_orkg("https://orkg.org/template/R758316")
        values = schema["dtreg_test_template2"][1][0].values()
        expected = "dict_values(['property3', 'P160024', 0, None, 'Integer'])"
        self.assertEqual(str(values), expected)

    def test_extract_orkg_nested(self):
        schema = extract_orkg("https://orkg.org/template/R758315")
        expected = "dict_keys(['dtreg_test_template2', 'dtreg_test_template1'])"
        self.assertEqual(str(schema.keys()), expected)


if __name__ == '__main__':
    unittest.main()
