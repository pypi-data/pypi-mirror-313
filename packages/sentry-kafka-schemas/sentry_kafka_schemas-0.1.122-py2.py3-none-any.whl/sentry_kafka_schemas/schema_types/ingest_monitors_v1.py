from typing import Union, TypedDict, Literal, Any, Required, List, Dict


class CheckIn(TypedDict, total=False):
    """
    check_in.

    A message that contains a monitor check-in payload.
    """

    message_type: Required[Literal['check_in']]
    """
    Discriminant marker identifying this as a check-in message.

    Required property
    """

    payload: Required[Union[str, Union[int, float], Dict[str, Any], List[Any], bool, None]]
    """
    bytes. JSON string of the wrapped monitor check-in event.

    Required property
    """

    start_time: Required[Union[int, float]]
    """
    The time relay produced the check-in to kafka. In seconds with floating precision.

    Required property
    """

    project_id: Required[int]
    """
    The project for which this check-in is being sent.

    minimum: 0
    maximum: 18446744073709551615

    Required property
    """

    sdk: Union[str, None]
    """ The originating SDK client identifier string. """

    retention_days: Required[int]
    """
    minimum: 0
    maximum: 65535

    Required property
    """



class ClockPulse(TypedDict, total=False):
    """
    clock_pulse.

    A message that is only used as a marker for minute boundaries.
    """

    message_type: Required[Literal['clock_pulse']]
    """
    Discriminant marker identifying this as a clock-pulse message.

    Required property
    """



IngestMonitorMessage = Union["ClockPulse", "CheckIn"]
"""
ingest_monitor_message.

Aggregation type: oneOf
"""

