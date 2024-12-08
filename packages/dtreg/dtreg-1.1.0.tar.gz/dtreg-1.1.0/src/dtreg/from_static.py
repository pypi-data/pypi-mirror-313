import json
from importlib_resources import files


def from_static(datatype_id):
    """
    Get schema information from static files

    :param datatype_id: a schema identifier
    :return: the requested schema information, or None if not in static
    """
    id = datatype_id.split("/", 4)[4]
    schema_info = None
    for f in files("dtreg.data").iterdir():
        if id in f.stem:
            file_text = f.read_text()
            schema_info = json.loads(file_text)
    return schema_info
