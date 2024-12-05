"""
Uils functions for groupings
"""

from enoslib import Host

from e2clab.grouping.grouping import (
    AddressMatch,
    Aggregate,
    Asarray,
    Grouping,
    RoundRobin,
)


def get_grouping_class(grouping: str) -> type[Grouping]:
    d = {
        "asarray": Asarray,
        "aggregate": Aggregate,
        "round_robin": RoundRobin,
        "address_match": AddressMatch,
    }
    # If 'grouping' is not in the keys, we 'want' an error to raise
    # as this should not happen after the schema validation
    return d[grouping]


def get_grouping(
    grouping: str,
    hosts: list[Host],
    prefix: str,
    selected_service_extra_info: list[dict],
) -> Grouping:
    """Get a grouping object

    Args:
        grouping (str): Grouping type
        hosts (list[Host]): List of hosts
        prefix (str): Prefix to access an extra info of a Service in workflow.yaml
        selected_service_extra_info (list[dict]): Extra information

    Returns:
        Grouping: E2Clab 'Grouping' like object
    """

    grouping_class = get_grouping_class(grouping)
    inst_grouping = grouping_class(
        hosts=hosts,
        service_extra_info=selected_service_extra_info,
        prefix=prefix,
    )

    return inst_grouping
