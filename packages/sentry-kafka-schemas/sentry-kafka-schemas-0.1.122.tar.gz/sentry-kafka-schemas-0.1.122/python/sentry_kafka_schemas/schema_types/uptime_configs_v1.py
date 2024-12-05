from typing import Required, Literal, List, Any, TypedDict, Union


class CheckConfig(TypedDict, total=False):
    """
    check_config.

    A message containing the configuration for a check to scheduled and executed by the uptime-checker.
    """

    subscription_id: Required[str]
    """
    UUID of the subscription that this check config represents.

    Required property
    """

    interval_seconds: Required["CheckInterval"]
    """
    check_interval.

    The interval between each check run in seconds.

    Required property
    """

    timeout_ms: Required[Union[int, float]]
    """
    The total time we will allow to make the request in milliseconds.

    Required property
    """

    url: Required[str]
    """
    The actual HTTP URL to check.

    Required property
    """

    request_method: "_CheckConfigRequestMethod"
    """ The HTTP method to use for the request. """

    request_headers: List["RequestHeader"]
    """ Additional HTTP headers to send with the request """

    request_body: str
    """ Additional HTTP headers to send with the request """

    trace_sampling: bool
    """ Whether to allow for sampled trace spans for the request. """



CheckInterval = Union[Literal[60], Literal[300], Literal[600], Literal[1200], Literal[1800], Literal[3600]]
"""
check_interval.

The interval between each check run in seconds.
"""
CHECKINTERVAL_60: Literal[60] = 60
"""The values for the 'check_interval' enum"""
CHECKINTERVAL_300: Literal[300] = 300
"""The values for the 'check_interval' enum"""
CHECKINTERVAL_600: Literal[600] = 600
"""The values for the 'check_interval' enum"""
CHECKINTERVAL_1200: Literal[1200] = 1200
"""The values for the 'check_interval' enum"""
CHECKINTERVAL_1800: Literal[1800] = 1800
"""The values for the 'check_interval' enum"""
CHECKINTERVAL_3600: Literal[3600] = 3600
"""The values for the 'check_interval' enum"""



RequestHeader = List[Any]
"""
request_header.

An individual header, consisting of a name and value as a tuple.

prefixItems:
  - title: header_name
    type: string
  - title: header_value
    type: string
"""



_CheckConfigRequestMethod = Union[Literal['GET'], Literal['POST'], Literal['HEAD'], Literal['PUT'], Literal['DELETE'], Literal['PATCH'], Literal['OPTIONS']]
""" The HTTP method to use for the request. """
_CHECKCONFIGREQUESTMETHOD_GET: Literal['GET'] = "GET"
"""The values for the 'The HTTP method to use for the request' enum"""
_CHECKCONFIGREQUESTMETHOD_POST: Literal['POST'] = "POST"
"""The values for the 'The HTTP method to use for the request' enum"""
_CHECKCONFIGREQUESTMETHOD_HEAD: Literal['HEAD'] = "HEAD"
"""The values for the 'The HTTP method to use for the request' enum"""
_CHECKCONFIGREQUESTMETHOD_PUT: Literal['PUT'] = "PUT"
"""The values for the 'The HTTP method to use for the request' enum"""
_CHECKCONFIGREQUESTMETHOD_DELETE: Literal['DELETE'] = "DELETE"
"""The values for the 'The HTTP method to use for the request' enum"""
_CHECKCONFIGREQUESTMETHOD_PATCH: Literal['PATCH'] = "PATCH"
"""The values for the 'The HTTP method to use for the request' enum"""
_CHECKCONFIGREQUESTMETHOD_OPTIONS: Literal['OPTIONS'] = "OPTIONS"
"""The values for the 'The HTTP method to use for the request' enum"""

