from typing import Dict, Union, TypedDict


class EapMutation(TypedDict, total=False):
    """ eap_mutation. """

    filter: "_EapMutationFilter"
    update: "_EapMutationUpdate"


class _EapMutationFilter(TypedDict, total=False):
    organization_id: "_Uint"
    """ minimum: 0 """

    _sort_timestamp: "_Uint"
    """ minimum: 0 """

    trace_id: "_Uuid"
    """
    minLength: 32
    maxLength: 36
    """

    span_id: str
    """ The span ID is a unique identifier for a span within a trace. It is an 8 byte hexadecimal string. """



class _EapMutationUpdate(TypedDict, total=False):
    attr_str: Dict[str, str]
    attr_num: Dict[str, Union[int, float]]


_Uint = int
""" minimum: 0 """



_Uuid = str
"""
minLength: 32
maxLength: 36
"""

