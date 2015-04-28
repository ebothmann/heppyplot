import os

import yaml

def read_configuration_file(path):
    with open(path) as f:
        return yaml.safe_load(f)
    return None

def read_configuration_value(configuration, key=None, default='__no_default__', diff=False):
    try:
        value = configuration['diff'] if diff else configuration[key]
    except KeyError:
        if default == '__no_default__':
            raise
        value = default
    return value

def read_configuration_subplot_values(configuration, key=None, defaults='__no_default__'):
    try:
        main_subplot_value = configuration[key]
    except KeyError:
        if defaults == '__no_default__':
            raise
        main_subplot_value = defaults[0]
    try:
        diff_subplot_value = configuration['diff'][key]
    except KeyError:
        if defaults == '__no_default__':
            raise
        diff_subplot_value = main_subplot_value if defaults[1] == '__use_main__' else defaults[1]
    return [main_subplot_value, diff_subplot_value]
