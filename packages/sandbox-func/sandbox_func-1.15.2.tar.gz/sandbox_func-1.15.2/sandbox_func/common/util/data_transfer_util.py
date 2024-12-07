import json


def json2obj(json_str, obj_class):
    parse_dict = json.loads(json_str)
    return dict2obj(parse_dict, obj_class)


def dict2obj(parse_dict, obj_class):
    res = obj_class(**parse_dict)
    return res
