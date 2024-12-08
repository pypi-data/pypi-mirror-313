import unittest
from unittest.mock import patch
import pandas as pd
from dtreg.load_datatype import load_datatype
from dtreg.dtr_interface import Epic
from dtreg.helpers import generate_uid
from dtreg.to_jsonld import differ_input, to_jsonld


class TestJsonLd(unittest.TestCase):

    maxDiff = None

    def test_input_numeric(self):
        self.assertEqual(differ_input(3), 3)

    def test_input_df(self):
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        new_uid = generate_uid()
        new_constants = Epic().add_df_constants()
        with patch('dtreg.to_jsonld.constants', new_constants):
            with patch('dtreg.to_jsonld.uid', new_uid):
                result = differ_input(df)
                self.assertEqual(result["tab_label"], "Table")

    def test_input_named_df(self):
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        df.name = "my_results"
        new_uid = generate_uid()
        new_constants = Epic().add_df_constants()
        with patch('dtreg.to_jsonld.constants', new_constants):
            with patch('dtreg.to_jsonld.uid', new_uid):
                result = differ_input(df)
                self.assertEqual(result["tab_label"], "my_results")

    def test_missing_df(self):
        df = pd.DataFrame({'A': [None, 2], 'B': [3, 4]})
        new_uid = generate_uid()
        new_constants = Epic().add_df_constants()
        with patch('dtreg.to_jsonld.constants', new_constants):
            with patch('dtreg.to_jsonld.uid', new_uid):
                result = differ_input(df)
                self.assertEqual(result["rows"][0]["cells"][0]["value"], None)

    def test_no_function(self):
        def abc(x):
            return x+1
        dt = load_datatype("https://doi.org/21.T11969/74bc7748b8cd520908bc")
        instance = dt.inferential_test_output(has_format=abc)
        to_jsonld(instance)
        self.assertRaisesRegex(
            ValueError, "SystemExit: Input in  has_format  should not be a function")

    def test_jsonld_epic_nested(self):
        dt = load_datatype("https://doi.org/21.T11969/aff130c76e68ead3862e")
        url = dt.url()
        instance = dt.data_item(has_expression=url)
        result = to_jsonld(instance)
        expected = ('{\n'
                    '  "@id": "_:n1",\n'
                    '  "@type": "doi:aff130c76e68ead3862e",\n'
                    '  "doi:aff130c76e68ead3862e#has_expression": {\n'
                    '    "@id": "_:n2",\n'
                    '    "@type": "doi:e0efc41346cda4ba84ca"\n'
                    '  },\n'
                    '  "@context": {\n'
                    '    "doi": "https://doi.org/21.T11969/",\n'
                    '    "columns": "https://doi.org/21.T11969/0424f6e7026fa4bc2c4a#columns",\n'
                    '    "col_number": "https://doi.org/21.T11969/65ba00e95e60fb8971e6#number",\n'
                    '    "col_titles": "https://doi.org/21.T11969/65ba00e95e60fb8971e6#titles",\n'
                    '    "rows": "https://doi.org/21.T11969/0424f6e7026fa4bc2c4a#rows",\n'
                    '    "row_number": "https://doi.org/21.T11969/9bf7a8e8909bfd491b38#number",\n'
                    '    "row_titles": "https://doi.org/21.T11969/9bf7a8e8909bfd491b38#titles",\n'
                    '    "cells": "https://doi.org/21.T11969/9bf7a8e8909bfd491b38#cells",\n'
                    '    "column": "https://doi.org/21.T11969/4607bc7c42ac8db29bfc#column",\n'
                    '    "value": "https://doi.org/21.T11969/4607bc7c42ac8db29bfc#value",\n'
                    '    "tab_label": "https://doi.org/21.T11969/0424f6e7026fa4bc2c4a#label"\n'
                    '  }\n'
                    '}')
        self.assertEqual(result, expected)

    def test_jsonld_epic_list(self):
        dt = load_datatype("https://doi.org/21.T11969/aff130c76e68ead3862e")
        url_1 = dt.url()
        url_2 = dt.url()
        instance = dt.data_item(has_expression=[url_1, url_2])
        result = to_jsonld(instance)
        expected = ('{\n'
                    '  "@id": "_:n1",\n'
                    '  "@type": "doi:aff130c76e68ead3862e",\n'
                    '  "doi:aff130c76e68ead3862e#has_expression": [\n'
                    '    {\n'
                    '      "@id": "_:n2",\n'
                    '      "@type": "doi:e0efc41346cda4ba84ca"\n'
                    '    },\n'
                    '    {\n'
                    '      "@id": "_:n3",\n'
                    '      "@type": "doi:e0efc41346cda4ba84ca"\n'
                    '    }\n'
                    '  ],\n'
                    '  "@context": {\n'
                    '    "doi": "https://doi.org/21.T11969/",\n'
                    '    "columns": "https://doi.org/21.T11969/0424f6e7026fa4bc2c4a#columns",\n'
                    '    "col_number": "https://doi.org/21.T11969/65ba00e95e60fb8971e6#number",\n'
                    '    "col_titles": "https://doi.org/21.T11969/65ba00e95e60fb8971e6#titles",\n'
                    '    "rows": "https://doi.org/21.T11969/0424f6e7026fa4bc2c4a#rows",\n'
                    '    "row_number": "https://doi.org/21.T11969/9bf7a8e8909bfd491b38#number",\n'
                    '    "row_titles": "https://doi.org/21.T11969/9bf7a8e8909bfd491b38#titles",\n'
                    '    "cells": "https://doi.org/21.T11969/9bf7a8e8909bfd491b38#cells",\n'
                    '    "column": "https://doi.org/21.T11969/4607bc7c42ac8db29bfc#column",\n'
                    '    "value": "https://doi.org/21.T11969/4607bc7c42ac8db29bfc#value",\n'
                    '    "tab_label": "https://doi.org/21.T11969/0424f6e7026fa4bc2c4a#label"\n'
                    '  }\n'
                    '}')
        self.assertEqual(result, expected)

    def test_jsonld_orkg(self):
        dt = load_datatype("https://orkg.org/template/R758316")
        instance = dt.dtreg_test_template2(label="test")
        result = to_jsonld(instance)
        expected = ('{\n'
                    '  "@id": "_:n1",\n'
                    '  "@type": "orkgr:R758316",\n'
                    '  "label": "test",\n'
                    '  "@context": {\n'
                    '    "orkgc": "https://orkg.org/class/",\n'
                    '    "orkgr": "https://orkg.org/resource/",\n'
                    '    "orkgp": "https://orkg.org/property/",\n'
                    '    "columns": "https://orkg.org/property/CSVW_Columns",\n'
                    '    "col_number": "https://orkg.org/property/CSVW_Number",\n'
                    '    "col_titles": "https://orkg.org/property/CSVW_Titles",\n'
                    '    "rows": "https://orkg.org/property/CSVW_Rows",\n'
                    '    "row_number": "https://orkg.org/property/CSVW_Number",\n'
                    '    "row_titles": "https://orkg.org/property/CSVW_Titles",\n'
                    '    "cells": "https://orkg.org/property/CSVW_Cells",\n'
                    '    "column": "https://orkg.org/property/CSVW_Column",\n'
                    '    "value": "https://orkg.org/property/CSVW_Value",\n'
                    '    "label": "http://www.w3.org/2000/01/rdf-schema#label",\n'
                    '    "tab_label": "http://www.w3.org/2000/01/rdf-schema#label"\n'
                    '  }\n'
                    '}')
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
