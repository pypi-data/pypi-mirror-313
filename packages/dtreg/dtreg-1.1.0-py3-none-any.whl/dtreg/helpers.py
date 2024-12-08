def format_string(string):
    """
    Format a string to lowercase, spaces and dashes as underscores

    :param string: a string
    :return: the string formatted in the required way
    """
    return string.lower().replace(" ", "_").replace("-", "_")


def get_prefix(url_string):
    """
    Get a prefix of a URL string

    :param url_string: a URL string
    :return: the prefix string indicating a datatype
    """
    part = url_string.split("/", 4)
    if "orkg.org" in url_string.split("/", 4)[2]:
        prefix = part[0] + "//" + part[2] + "/"
    elif url_string.split("/", 4)[3] == '21.T11969':
        prefix = part[0] + "//" + part[2] + "/" + part[3] + "/"
    return prefix


def specify_cardinality(cardinality_string):
    """
    Write cardinality of an ePIC property as a dictionary

    :param cardinality_string: an ePIC string for cardinality
    :return: a dictionary with "min" and "max" values as integers or None
    """
    card_parts = cardinality_string.split(" - ")
    if len(card_parts) == 1:
        min_max = {
            "min": int(cardinality_string),
            "max": int(cardinality_string)}
    else:
        min_max = {
            "min": int(card_parts[0]),
            "max": None if card_parts[1] == "n" else int(card_parts[1])}
    return min_max


def generate_uid():
    """
    Generate a counting function for assigning identifiers
    :return: the counting function
    """
    i = 0

    def function():
        nonlocal i
        i += 1
        return i
    return function
