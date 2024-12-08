from .helpers import generate_uid
import pandas as pd
import json
from inspect import isfunction

constants = None
uid = None


def to_jsonld(instance):
    """
    Write an instance in JSON-LD format

    :param instance: an instance of a schema-related class
    :return: JSON string in JSON-LD format
    """
    result_all = {}
    global uid
    uid = generate_uid()
    global constants
    constants = instance.add_df_constants()

    def write_info(instance):
        result = {
            "@id": "_:n" + str(uid()),
            "@type": instance.add_dt_type(instance.dt_id)}
        for field in instance.prop_list:
            instance_field = getattr(instance, field)
            prop_id = next(item for item in instance.prop_info if item["dtp_name"] == field)[
                "dtp_id"]
            prop_type = instance.add_dtp_type(prop_id)
            if instance_field is None or instance_field is []:
                pass
            elif isfunction(instance_field):
                print("Input in " + field + " should not be a function")
            elif isinstance(instance_field, list) and hasattr(instance_field[0], "prop_list"):
                result[prop_type] = list(map(write_info, instance_field))
            elif hasattr(instance_field, "prop_list"):
                result[prop_type] = write_info(instance_field)
            else:
                result[prop_type] = differ_input(instance_field)
        return result
    result_all = write_info(instance)
    result_all["@context"] = instance.add_context(instance.prefix)
    result_json = json.dumps(result_all, indent=2)
    return result_json


def differ_input(input):
    """
    Differentiate input for further use by to_jsonld function

    :param input: an object to be differentiated as a dataframe or another type
    :return: the result of calling the df_structure function, or the input unchanged
    """
    if isinstance(input, pd.DataFrame):
        output = df_structure(input)
    else:
        output = input
    return output


def df_structure(df):
    """
    Prepare a dataframe for to_jsonld function

    :param df: a dataframe
    :return: a dictionary to be used by to_jsonld function
    """
    global uid
    global constants
    result = {}
    result["@type"] = constants["table"]
    result["tab_label"] = df.name if hasattr(df, "name") else "Table"
    column_ids = []
    result["columns"] = []
    for i, col in enumerate(df.columns):
        column = {
            "@type": constants["column"],
            "col_number": i + 1,
            "col_titles": col,
            "@id": "_:n" + str(uid())
        }
        column_ids.append(column["@id"])
        result["columns"].append(column)
    result["rows"] = []
    for i, (title, ro) in enumerate(df.iterrows()):
        row = {
            "@type": constants["row"],
            "row_number": i + 1,
            "row_titles": str(title),
            "@id": "_:n" + str(uid()),
            "cells": []
        }
        for j, cel_val in enumerate(ro):
            row["cells"].append({
                "@type": constants["cell"],
                "@id": "_:n" + str(uid()),
                "value": str(cel_val) if not pd.isna(cel_val) else None,
                "column": column_ids[j]
            })
        result["rows"].append(row)
    result["@id"] = "_:n" + str(uid())
    return result
