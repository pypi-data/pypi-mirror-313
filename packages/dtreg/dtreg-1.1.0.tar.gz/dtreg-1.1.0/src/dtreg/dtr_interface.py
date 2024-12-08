from typing import Protocol
from .extract_epic import extract_epic
from .extract_orkg import extract_orkg
from .from_static import from_static


def select_dtr(datatype_id):
    """
    Select a dtr-related class based on a schema identifier

    :param datatype_id: a schema identifier
    :return: a class related to the datatype registry
    """
    selected_class = None
    if datatype_id.split("/", 4)[3] == '21.T11969':
        selected_class = Epic
    elif "orkg.org" in datatype_id.split("/", 4)[2]:
        selected_class = Orkg
    else:
        print("Please check whether the schema belongs to the ePIC or the ORKG dtr")
    return selected_class


class DataTypeReg(Protocol):
    """
    Interface for a class representing a datatype registry
    """

    def get_schema_info(self, datatype_id):
        """
        Obtain information from a schema

        :param datatype_id: a schema identifier
        :return: not implemented, this is an interface
        """
        pass

    def add_context(self, prefix):
        """
        Write dtr-specific context for JSON-LD
        The dtr-specific information is provided by the dtr

        :param prefix: A URL prefix
        :return: not implemented, this is an interface
        """
        pass

    def add_dt_type(self, identifier):
        """
        Write schema type for JSON-LD

        :param identifier: a schema identifier
        :return: not implemented, this is an interface
        """
        pass

    def add_dtp_type(self, identifier):
        """
        Write property type for JSON-LD

        :param identifier: a property identifier
        :return: not implemented, this is an interface
        """
        pass

    def add_df_constants(self):
        """
        Write dataframe constants for JSON-LD

        :return: not implemented, this is an interface
        """
        pass


class Epic:
    """
    Class representing the ePIC dtr
    """

    def get_schema_info(self, datatype_id):
        """
        Obtain information from an ePIC datatype

        :param datatype_id: an ePIC datatype identifier
        :return: extracted information from the ePIC datatype
        """
        static = from_static(datatype_id)
        if static is None:
            schema_info = extract_epic(datatype_id)
        else:
            schema_info = static
        return schema_info

    def add_context(self, prefix):
        """
        Write ePIC-specific context for JSON-LD
        The ePIC-specific information is provided by the ePIC dtr

        :param prefix: a URL prefix
        :return: context to include in JSON-LD
        """
        context_info = {
            "doi": prefix,
            "columns": prefix + "0424f6e7026fa4bc2c4a#columns",
            "col_number":  prefix + "65ba00e95e60fb8971e6#number",
            "col_titles":  prefix + "65ba00e95e60fb8971e6#titles",
            "rows":  prefix + "0424f6e7026fa4bc2c4a#rows",
            "row_number":  prefix + "9bf7a8e8909bfd491b38#number",
            "row_titles":  prefix + "9bf7a8e8909bfd491b38#titles",
            "cells":  prefix + "9bf7a8e8909bfd491b38#cells",
            "column":  prefix + "4607bc7c42ac8db29bfc#column",
            "value":  prefix + "4607bc7c42ac8db29bfc#value",
            "tab_label": prefix + "0424f6e7026fa4bc2c4a#label"}
        return context_info

    def add_dt_type(self, identifier):
        """
        Write ePIC-specific datatype type for JSON-LD

        :param identifier: an ePIC datatype identifier
        :return: type to include in JSON-LD
        """
        dt_type = "doi:" + identifier
        return dt_type

    def add_dtp_type(self, identifier):
        """
        Write ePIC-specific property type for JSON-LD

        :param identifier: an ePIC property identifier
        :return: property type to include in JSON-LD
        """
        dtp_type = "doi:" + identifier
        return dtp_type

    def add_df_constants(self):
        """
        Write ePIC-specific dataframe constants for JSON-LD

        :return: dataframe constants to include in JSON-LD
        """
        df_constants = {
            "table": "doi:0424f6e7026fa4bc2c4a",
            "column": "doi:65ba00e95e60fb8971e6",
            "row": "doi:9bf7a8e8909bfd491b38",
            "cell": "doi:4607bc7c42ac8db29bfc"}
        return df_constants


class Orkg:
    """
    Class representing the ORKG dtr
    """

    def get_schema_info(self, datatype_id):
        """
        Obtain information from an ORKG template

        :param datatype_id: an ORKG template identifier
        :return: extracted information from the ORKG template
        """
        schema_info = extract_orkg(datatype_id)
        return schema_info

    def add_context(self, prefix):
        """
        Write ORKG-specific context for JSON-LD
        The ORKG-specific information is provided by the ORKG dtr

        :param prefix: a URL prefix
        :return: context to include in JSON-LD
        """
        context_info = {
            "orkgc": prefix + "class/",
            "orkgr": prefix + "resource/",
            "orkgp": prefix + "property/",
            "columns": prefix + "property/" + "CSVW_Columns",
            "col_number": prefix + "property/" + "CSVW_Number",
            "col_titles": prefix + "property/" + "CSVW_Titles",
            "rows": prefix + "property/" + "CSVW_Rows",
            "row_number": prefix + "property/" + "CSVW_Number",
            "row_titles": prefix + "property/" + "CSVW_Titles",
            "cells": prefix + "property/" + "CSVW_Cells",
            "column": prefix + "property/" + "CSVW_Column",
            "value": prefix + "property/" + "CSVW_Value",
            "label": "http://www.w3.org/2000/01/rdf-schema#label",
            "tab_label": "http://www.w3.org/2000/01/rdf-schema#label"}
        return context_info

    def add_dt_type(self, identifier):
        """
        Write ORKG template type for JSON-LD

        :param identifier: an ORKG template identifier
        :return: type to include in JSON-LD
        """
        dt_type = "orkgr:" + identifier
        return dt_type

    def add_dtp_type(self, identifier):
        """
        Write ORKG-specific property type for JSON-LD

        :param identifier: an ORKG property identifier
        :return: property type to include in JSON-LD
        """
        dtp_type = identifier if identifier == "label" else "orkgp:" + identifier
        return dtp_type

    def add_df_constants(self):
        """
        Write ORKG-specific dataframe constants for JSON-LD

        :return: dataframe constants to include in JSON-LD
        """
        df_constants = {
            "table": "orkgc:Table",
            "column": "orkgc:Column",
            "row": "orkgc:Row",
            "cell": "orkgc:Cell"}
        return df_constants
