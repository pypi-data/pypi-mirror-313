import re

import numpy as np


def safe_isnan(value, extend_to_None=True):
    """
    Make np.isnan working on any type:

    >>> test = {False: False, "": False, None: True, 1: False, np.nan:True}
    >>> for test, exp in test.items():
    ...     assert safe_isnan(test) == exp

    None can be checked as `np.NaN` depending on `extend_to_None`:

    >>> safe_isnan(None, extend_to_None=False)
    False
    >>> safe_isnan(None, extend_to_None=True)  # default
    True
    """
    try:
        return np.isnan(value)
    except TypeError:
        if value is None and extend_to_None:
            return True
        return False


FMTS = {
    "default": {
        "bold": True,
        "font_color": "#3A81CC",
        "align": "center",
        "valign": "vcenter",
        "border": 1,
        "bg_color": "#eeeeec",
    },
    "mandatory": {"bg_color": "#fcaf3e", "color": "black"},
    "padded": {"bg_color": "#8ae234", "color": "black"},
    "units": {"bg_color": "#729fcf", "color": "black"},
}


def fmt_dict(attributes=()):
    """
    >>> fmt_dict(attributes=["mandatory"])
    {'bold': True, 'font_color': '#3A81CC', 'align': 'center', 'valign': 'vcenter', 'border': 1, 'bg_color': '#fcaf3e', 'color': 'black'}
    """
    fmt = FMTS["default"].copy()
    for attr in attributes:
        _d = FMTS[attr].copy()
        fmt.update(_d)
    return fmt


def field_status(colname, schema):
    """return one of {'mandatory', 'padded', 'default'"""
    is_mandatory = colname in schema.required
    pattern = schema.columns_specs[colname]["items"].get("pattern")
    if pattern and not re.match(pattern, "") and is_mandatory:
        is_mandatory = True
    default = schema.columns_specs[colname]["items"].get("default")
    is_padded = False
    if default == "_pad_":
        is_mandatory = False
        is_padded = True
    # xcalling = schema.xcalling.get(colname)
    if is_mandatory:  # or xcalling:
        status = "mandatory"
    elif is_padded:
        status = "padded"
    else:
        status = "default"
    return status


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
