import unittest
from dtreg.request_dtr import request_dtr


class TestRequest(unittest.TestCase):

    def test_obtain_epic(self):
        b2_schema = request_dtr('https://doi.org/21.T11969/6128ce5def6ffac006e0?locatt=view:json')
        self.assertEqual(b2_schema["name"], 'B2INST-Schema')

    def test_obtain_orkg(self):
        b2_schema = request_dtr('https://orkg.org//api/templates/R758316')
        self.assertEqual(b2_schema["label"], 'dtreg_test_template2')


if __name__ == '__main__':
    unittest.main()
