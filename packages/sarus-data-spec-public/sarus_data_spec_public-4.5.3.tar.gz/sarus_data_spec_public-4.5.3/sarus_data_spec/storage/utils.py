from typing import Collection, cast

from sarus_data_spec.protobuf.typing import ProtobufWithUUID
from sarus_data_spec.storage.typing import Storage
from sarus_data_spec.typing import Referrable, Referring


def sort_dataspecs(
    storage: Storage, values: Collection[Referrable[ProtobufWithUUID]]
) -> Collection[Referring[ProtobufWithUUID]]:
    """Sort a list of dataspecs, in the order of the DAG, from the root to the
        nodes (the elements of the input list).

        This algorithm is a variation of the depth first search.
        It uses a queue, called values_queue, to store all data elements.
        A separate set, called visited_values, is used to keep track
        of elements that have been processed. The algorithm adds
        elements to the values_queue in such a way that when an element
        is encountered again (we know it from visited_values),
        all of its parent elements have already been added to the
        sorted list. This ensures that the final list is sorted
        in a way that preserves the hierarchical relationships
        between elements.

    The worst case time complexity of this algorithm is O(n^2)
    where n is the number of elements in the input list.


    Args:
        values (Collection[Referrable[ProtobufWithUUID]]):
        A list of dataspecs that need to be sorted.

    Raises:
        ValueError: In case the user attempts to add a dataspec
        with a reference to another dataspec that is not already stored.

    Returns:
        Collection[DataSpec]: The sorted list
        of dataspecs, in the order of the DAG, from the root to the nodes.
    """
    values_queue = []
    for value in values:
        if isinstance(value, Referring):
            value = cast(Referring[ProtobufWithUUID], value)
            values_queue.append(value)
    sorted_values = []
    visited_values = set()
    while values_queue:
        value = values_queue.pop()
        if value not in visited_values:
            referred_uuids = value.referred_uuid()
            referred_values_to_add = []
            for referred_uuid in referred_uuids:
                if (referred_uuid not in [v.uuid() for v in values]) and (
                    not storage.referrable(referred_uuid)
                ):
                    raise ValueError(
                        """Referenced object not found in
                        storage or in dataspecs to be stored."""
                    )
                for queued_value in values_queue:
                    if queued_value.uuid() == referred_uuid:
                        referred_values_to_add.append(queued_value)
            if not referred_values_to_add:
                sorted_values.append(value)
                visited_values.add(value)
            else:
                for referred_value in referred_values_to_add:
                    values_queue.remove(referred_value)
                values_queue.extend([value, *referred_values_to_add])
                visited_values.add(value)
        else:
            sorted_values.append(value)
    return sorted_values
