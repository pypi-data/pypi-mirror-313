import json
import os
import ssl
import typing
from datetime import datetime
import grpc
from lxml import objectify
from typing import Union


def objectify_xml(path_file) -> objectify.ObjectifiedElement:
    """
    Try to objectify the xml file and return the objectified element. Return None if it fails.
    """
    try:
        return objectify.parse(path_file).getroot()
    except:
        raise Exception(f"Error parsing {path_file}")


def try_get_from_oe(prop: str, object: objectify.ObjectifiedElement) -> Union[str, None]:
    try:
        return object[prop]
    except:
        return None


def try_get_lxml_attrib(node: objectify.ObjectifiedElement, attribute_name: str) -> Union[str, None]:
    """
    If the attribute exists on the objectified node then return it, else return None
    """
    if attribute_name in node.attrib.keys():
        return node.attrib[attribute_name]
    else:
        return None


def append_timestamp_to_basepath(base_path):
    now = datetime.now()
    unique_directory = os.path.join(base_path, "{0}{1}{2}_{3}{4}_{5}".format(now.year, now.month, now.day, now.hour,
                                                                             now.minute,
                                                                             now.second))
    return unique_directory


def try_get_from_str_dict(key: str, dictionary: dict, default_value: Union[int, float, str, None] = "") -> \
        Union[int, float, str, None]:
    """
    returns the value of the lookup element if it is available in the dict.
    if the lookup element is not in the dict, the default value is returned.
    """
    if key in dictionary.keys():
        return dictionary[key]
    return default_value


def to_spatial_reference_xml(sr_id: str):
    if sr_id.lower() == "lv95":
        return load_file_as_string("LV95.txt")
    elif sr_id.lower() == "lv03":
        return load_file_as_string("LV_03.txt")
    else:
        raise Exception


def load_json_file(json_file_path: str):
    with open(json_file_path) as json_file:
        return json.load(json_file)


def load_file_as_string(file_name: str) -> str:
    cwd = os.getcwd()
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, encoding='utf-8') as file:
        lines = file.readlines()
        return "".join(lines)


def to_bool(value: Union[str, bool, int, None] = None, default_value: bool = False) -> bool:
    """"
    treats "true" or "True" or 'yes' or 'Yes' or 1 or '1' as True (bool). Anything else returns False (bool)
    """
    if type(value) == bool:
        return value
    if type(value) == str:
        if str_is_none_or_empty(value):
            return default_value
        if value.upper() == 'TRUE' or value.upper() == 'YES' or value == '1':
            return True
        else:
            return False
    if type(value) == int:
        if value == 1:
            return True
        else:
            return False
    else:
        return default_value


def str_not_empty(string: str) -> bool:
    if string:
        if string == "":
            return False
        else:
            return True
    return False


def str_is_none_or_empty(string: str) -> bool:
    return not str_not_empty(string)


def to_float(value: Union[str, int, float, None], default_value: float = 0) -> Union[float, None]:
    """
    :param value: value that gets converted to float type
    :param default_value: value that is returned in case the float conversion fails
    :return:
    """
    try:
        return float(value)
    except:
        return default_value


def to_int(value: Union[str, int, None], default_value: int = 0) -> Union[int, None]:
    """
    Tries to convert the input value to int. If conversion is not possible, returns the default value.

    :param value: value that gets converted to int type
    :param default_value: value that is returned in case the int conversion fails
    :return: int representation of the input value or 0
   """
    try:
        return int(value)
    except:
        return default_value


def get_value_or_default(value: typing.Any, default: typing.Any) -> typing.Any:
    """
    Returns the value if it is not None. Else returns the default value.
    """
    if value:
        return value
    return default


def get_ssl_channel_credentials() -> grpc.ssl_channel_credentials:
    """
    Creates an ssl channel credentials object for use with an SSL-enabled channel for the 
    authentication with a server that requires TLS/SSL. The appropriate root certificates
    for server authentication are loaded from the windows certificate store.

    :return: A ChannelCredentials object
    """
    ctx = ssl.create_default_context()
    ca_certs = ctx.get_ca_certs(binary_form=True)
    ctx.load_default_certs(purpose=ssl.Purpose.SERVER_AUTH)

    root_certificates_pem = ''

    for cert in ca_certs:
        pem = ssl.DER_cert_to_PEM_cert(cert)
        root_certificates_pem += pem

    return grpc.ssl_channel_credentials(root_certificates=str.encode(root_certificates_pem, 'utf-8'))
