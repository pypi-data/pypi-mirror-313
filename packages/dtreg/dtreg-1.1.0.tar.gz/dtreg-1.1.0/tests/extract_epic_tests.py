import unittest
from dtreg.extract_epic import extract_epic


class TestExtractEpic(unittest.TestCase):

    def test_extract_epic(self):
        result = extract_epic("https://doi.org/21.T11969/1ea0e148d9bbe08335cd")
        expected = {'pidinst_schemaobject': [[{'dt_name': 'pidinst_schemaobject',
                                               'dt_id': '1ea0e148d9bbe08335cd',
                                               'dt_class': 'Object'}],
                                             []]}
        self.assertEqual(result, expected)

    def test_extract_epic_props(self):
        schema = extract_epic("https://doi.org/21.T11969/31483624b5c80014b6c7")
        values = schema["matrix_size"][1][0].values()
        expected = "dict_values(['number_of_rows', "\
            "'21.T11969/31483624b5c80014b6c7#number_of_rows', 1, 1, "\
            "'21.T11969/fb2e379f820c6f8f9e82'])"
        self.assertEqual(str(values), expected)


if __name__ == '__main__':
    unittest.main()
