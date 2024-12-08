import unittest
from dtreg.from_static import from_static


class TestFromStatic(unittest.TestCase):

    def test_no_static(self):
        no_static = from_static("https://doi.org/21.T11969/111")
        self.assertEqual(no_static, None)

    def test_static(self):
        templ = from_static("https://doi.org/21.T11969/3df63b7acb0522da685d")
        expected = {'string': [[{'dt_name': 'string',
                                 'dt_id': '3df63b7acb0522da685d',
                                 'dt_class': 'String'}],
                               []]}
        self.assertEqual(templ, expected)


if __name__ == '__main__':
    unittest.main()
