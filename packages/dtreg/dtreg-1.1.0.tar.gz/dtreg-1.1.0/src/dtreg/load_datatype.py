from .dtr_interface import select_dtr
from .helpers import get_prefix
from types import SimpleNamespace


def load_datatype(datatype_id):
    """
    Load classes for a schema with the known identifier

    :param datatype_id: a schema identifier
    :return: a list of schemata as SimpleNamespace objects
    """
    schemata_dict = write_classes(datatype_id)
    schemata = SimpleNamespace(**schemata_dict)
    return schemata


def write_classes(datatype_id):
    """
    Write classes for a specified schema

    :param datatype_id: a schema identifier
    :return: a list of classes
    """
    datypreg = select_dtr(datatype_id)
    schema_info = datypreg().get_schema_info(datatype_id)
    prefix = get_prefix(datatype_id)
    objects = {}
    for key in schema_info.keys():
        dt_name = schema_info[key][0][0]["dt_name"]
        prop_list = []
        if len(schema_info[key][1]) != 0:
            for props in schema_info[key][1]:
                prop_list.append(props["dtp_name"])

        def __init__(self, *args, **kwargs):
            for dtp_name in self.prop_list:
                setattr(self, dtp_name, kwargs.get(dtp_name))
        class_object = type(dt_name,
                            (datypreg,),
                            {"prefix": prefix,
                                "dt_name": dt_name,
                                "dt_id": schema_info[key][0][0]["dt_id"],
                                "dt_class": schema_info[key][0][0]["dt_class"],
                                "prop_list": prop_list,
                                "prop_info": schema_info[key][1],
                                "__init__": __init__})
        objects.update({dt_name: class_object})
    return objects
