import unittest

from dtreg.dtr_interface import select_dtr


class TestDataTypeReg(unittest.TestCase):

    def test_dtr_epic(self):
        dtr_epic = select_dtr("https://doi.org/21.T11969/1ea0e148d9bbe08335cd")
        self.assertEqual(str(dtr_epic), "<class 'dtreg.dtr_interface.Epic'>")

    def test_dtr_orkg(self):
        dtr_orkg = select_dtr("https://incubating.orkg.org/template/R937648")
        self.assertEqual(str(dtr_orkg), "<class 'dtreg.dtr_interface.Orkg'>")

    def test_no_dtr(self):
        select_dtr("https://doi.org/22.B34567/1ea0e148d9bbe08335cd")
        self.assertRaisesRegex(
            ValueError,
            "SystemExit: Please check whether the schema belongs to the ePIC or the ORKG dtr")


if __name__ == '__main__':
    unittest.main()
