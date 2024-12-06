from collections import defaultdict
from itertools import chain, combinations
from typing import (
    Callable,
    Collection,
    DefaultDict,
    Dict,
    Final,
    FrozenSet,
    List,
    MutableMapping,
    Optional,
    Set,
    Tuple,
    Union,
    cast,
)

from sarus_data_spec.protobuf.typing import (
    ProtobufWithUUID,
    ProtobufWithUUIDAndDatetime,
)
from sarus_data_spec.storage.utils import sort_dataspecs
from sarus_data_spec.typing import DataSpec, Referrable, Referring

SEP: Final[str] = ","


def referrable_collection_string(
    values: Collection[Referrable[ProtobufWithUUID]],
) -> str:
    return SEP.join(sorted(value.uuid() for value in values))


def uuid_collection_string(uuids: Collection[str]) -> str:
    return SEP.join(sorted(uuid for uuid in uuids))


def referrable_collection_set(
    values: Collection[Referrable[ProtobufWithUUID]],
) -> FrozenSet[str]:
    return frozenset(value.uuid() for value in values)


class Storage:
    """Simple local Storage."""

    def __init__(self) -> None:
        # A Store to save (timestamp, type_name, data, relating data)
        self._referrables: MutableMapping[
            str, Referrable[ProtobufWithUUID]
        ] = dict()
        self._referring: DefaultDict[str, Set[str]] = defaultdict(set)
        self._sources: DefaultDict[str, Set[str]] = defaultdict(set)

    def store(self, value: Referrable[ProtobufWithUUID]) -> None:
        # Checks the value for consistency
        assert value._frozen()
        self._referrables[value.uuid()] = value

        if isinstance(value, Referring):
            value = cast(Referring[ProtobufWithUUID], value)
            referred_values = value.referred()

            # add referring
            referred_combinations = chain.from_iterable(
                combinations(referred_values, r) for r in range(1, 3)
            )
            for combination in referred_combinations:
                self._referring[referrable_collection_string(combination)].add(
                    value.uuid()
                )
            # add sources
            self._store_sources(value)

    def _store_sources(self, value: Referring[ProtobufWithUUID]) -> None:
        """A helper function to only store the sources of a referrable"""
        referred_values = value.referred()
        referred_dataspecs = [
            referred_value
            for referred_value in referred_values
            if isinstance(referred_value, DataSpec)
        ]
        if not referred_dataspecs:
            self._sources[value.uuid()].add(value.uuid())
            return None

        # update _sources if missing sources
        for referred_dataspec in referred_dataspecs:
            if isinstance(referred_dataspec, DataSpec):
                if len(self.sources(referred_dataspec)) == 0:
                    self._store_sources(referred_dataspec)

        sources = set()
        for referred_dataspec in referred_dataspecs:
            sources.update(self._sources[referred_dataspec.uuid()])
        if len(sources) == 0:
            raise ValueError(
                """Unable to retrieve sources. The computation graph
                        in storage is incomplete."""
            )
        self._sources[value.uuid()].update(sources)

    def batch_store(
        self, values: Collection[Referrable[ProtobufWithUUID]]
    ) -> None:
        """Store a collection of referrables in the storage.

        This method does not requires the objects to be provided in the graph
        order.
        """
        for value in values:
            # Add all objects to the referrables first
            assert value._frozen()
            self._referrables[value.uuid()] = value

        for value in values:
            # Add referring link in a second time
            if isinstance(value, Referring):
                value = cast(Referring[ProtobufWithUUID], value)
                referred_combinations = chain.from_iterable(
                    combinations(value.referred(), r) for r in range(1, 3)
                )
                for combination in referred_combinations:
                    self._referring[
                        referrable_collection_string(combination)
                    ].add(value.uuid())

        # add sources
        sorted_values = self.sort_dataspecs(values)
        for value in sorted_values:
            self._store_sources(value)

    def referrable(self, uuid: str) -> Optional[Referrable[ProtobufWithUUID]]:
        """Read a stored value."""
        return self._referrables.get(uuid, None)

    def referring_uuid(
        self,
        referred_uuid: Collection[str],
        type_name: Optional[str] = None,
    ) -> Collection[Referring[ProtobufWithUUID]]:
        """List all values referring to one referred referrable."""
        referring_uuids = self._referring[
            uuid_collection_string(referred_uuid)
        ]
        referrings = [self.referrable(uuid) for uuid in referring_uuids]
        if not all(referring is not None for referring in referrings):
            raise ValueError("A referring is not stored.")

        if type_name is not None:
            referrings = [
                referring
                for referring in referrings
                if (
                    referring is not None
                    and referring.type_name() == type_name
                )
            ]
        return referrings  # type:ignore

    def referring(
        self,
        referred: Union[
            Referrable[ProtobufWithUUID],
            Collection[Referrable[ProtobufWithUUID]],
        ],
        type_name: Optional[str] = None,
    ) -> Collection[Referring[ProtobufWithUUID]]:
        """List all values referring to one referred referrable."""
        if isinstance(referred, Referrable):
            referred_uuid = {referred.uuid()}
        else:
            referred_uuid = {value.uuid() for value in referred}
        return self.referring_uuid(
            referred_uuid=referred_uuid, type_name=type_name
        )

    def batch_referring(
        self,
        collection_referred: Collection[
            Union[
                Referrable[ProtobufWithUUID],
                Collection[Referrable[ProtobufWithUUID]],
            ]
        ],
        type_names: Optional[Collection[str]] = None,
    ) -> Optional[Dict[str, Set[Referring[ProtobufWithUUID]]]]:
        referred_strings = []
        for referred in collection_referred:
            if isinstance(referred, Referrable):
                referred_strings.append(
                    referrable_collection_string([referred])
                )
            else:
                referred_strings.append(referrable_collection_string(referred))

        referring_uuids: List[str] = []
        for referred_string in referred_strings:
            referring_uuids.extend(self._referring[referred_string])

        referrings: List[Referring[ProtobufWithUUID]] = []
        for uuid in referring_uuids:
            ref = self.referrable(uuid)
            assert ref is not None
            referring = cast(Referring[ProtobufWithUUID], ref)
            referrings.append(referring)

        # init result dict with types
        result_dict: Dict[str, Set[Referring[ProtobufWithUUID]]] = {}
        if type_names is not None:
            for type_name in type_names:
                result_dict[type_name] = set()

        for referring in referrings:
            typename = referring.type_name()
            if typename in result_dict:
                result_dict[typename].add(referring)
            else:
                result_dict[typename] = {referring}

        return result_dict

    def sources(
        self,
        value: Referrable[ProtobufWithUUID],
        type_name: Optional[str] = None,
    ) -> Set[DataSpec]:
        """Returns a set of all sources of a referrable."""
        if not isinstance(value, Referring):
            return set()

        value = cast(Referring[ProtobufWithUUID], value)
        source_uuids = self._sources[value.uuid()]
        sources = {self.referrable(uuid) for uuid in source_uuids}
        if not all(source is not None for source in sources):
            raise ValueError("A source is not stored.")

        if len(sources) > 0:
            if type_name is not None:
                sources = {
                    source
                    for source in sources
                    if (source is not None and source.type_name() == type_name)
                }
            return {
                cast(
                    DataSpec,
                    source,
                )
                for source in sources
            }
        else:
            self._store_sources(value)
            return self.sources(value=value, type_name=type_name)

    def all_sources(self, type_name: Optional[str] = None) -> Set[DataSpec]:
        """Returns a set of all sources (with type_name) in the Storage."""
        source_uuids = set.union(*self._sources.values())
        sources = {self.referrable(uuid) for uuid in source_uuids}
        if len(sources) > 0:
            if type_name is not None:
                sources = {
                    source
                    for source in sources
                    if (source is not None and source.type_name() == type_name)
                }
            return {
                cast(
                    DataSpec,
                    source,
                )
                for source in sources
            }
        else:
            return set()

    def last_referring(
        self,
        referred_uuid: Collection[str],
        type_name: str,
    ) -> Optional[Referring[ProtobufWithUUIDAndDatetime]]:
        """Last value referring to one referred.
        This implementation is not very efficient"""
        referrings = cast(
            Collection[Referring[ProtobufWithUUIDAndDatetime]],
            self.referring_uuid(referred_uuid, type_name),
        )
        if len(referrings) > 0:
            return max(referrings, key=lambda r: r.protobuf().datetime)
        else:
            return None

    def update_referring_with_datetime(
        self,
        referred_uuid: Collection[str],
        type_name: str,
        update: Callable[
            [Referring[ProtobufWithUUIDAndDatetime]],
            Tuple[Referring[ProtobufWithUUIDAndDatetime], bool],
        ],
    ) -> Tuple[Referring[ProtobufWithUUIDAndDatetime], bool]:
        """
        The local storage has no concurrency problem,
        simply call last referring and store
        """
        value = self.last_referring(referred_uuid, type_name)
        assert value is not None
        updated, should_update = update(value)
        if should_update:
            self.store(updated)
        return value, True

    def create_referring_with_datetime(
        self,
        value: Referring[ProtobufWithUUIDAndDatetime],
        update: Callable[
            [Referring[ProtobufWithUUIDAndDatetime]],
            Tuple[Referring[ProtobufWithUUIDAndDatetime], bool],
        ],
    ) -> Tuple[Referring[ProtobufWithUUIDAndDatetime], bool]:
        """Local storage is process dependent, no concurrency"""

        self.store(value)
        return value, True

    def type_name(
        self, type_name: str
    ) -> Collection[Referrable[ProtobufWithUUID]]:
        """List all values from a given type_name."""
        return {
            ref
            for ref in self._referrables.values()
            if ref.type_name() == type_name
        }

    def all_referrings(self, uuid: str) -> List[str]:
        """Returns a list all items referring to a Referrable recursively."""
        target = self.referrable(uuid)
        if target is None:
            raise ValueError("The referrable object is not stored.")

        to_delete, to_check = set(), {target}
        while len(to_check) > 0:
            node = to_check.pop()
            if not node:
                continue
            to_delete.add(node)
            deps = node.referring()
            if not deps:
                continue
            for dep in deps:
                if dep not in to_delete:
                    to_check.add(dep)

        return [msg.uuid() for msg in to_delete]

    def delete(self, uuid: str) -> None:
        """Delete a Referrable and all elements referring to it to let the
        storage in a consistent state."""
        uuids_to_delete = set(self.all_referrings(uuid))

        self._referrables = {
            uuid: referring
            for uuid, referring in self._referrables.items()
            if uuid not in uuids_to_delete
        }

        self._referring = defaultdict(
            set,
            {
                uuid: referring_uuids - uuids_to_delete
                for uuid, referring_uuids in self._referring.items()
                if uuid not in uuids_to_delete
            },
        )

        self._sources = defaultdict(
            set,
            {
                uuid: sources_uuids - uuids_to_delete
                for uuid, sources_uuids in self._sources.items()
                if uuid not in uuids_to_delete
            },
        )

    def delete_type(self, type_name: str) -> None:
        """Deletes all referrable corresponding to a given type_name and all
        the referrings corresponfing to it"""

        uuids = [obj.uuid() for obj in self.type_name(type_name)]
        uuids_to_delete = set(
            chain(*(self.all_referrings(uuid) for uuid in uuids))
        )

        self._referrables = {
            uuid: referring
            for uuid, referring in self._referrables.items()
            if uuid not in uuids_to_delete
        }

        self._referring = defaultdict(
            set,
            {
                uuid: referring_uuids - uuids_to_delete
                for uuid, referring_uuids in self._referring.items()
                if uuid not in uuids_to_delete
            },
        )

        self._sources = defaultdict(
            set,
            {
                uuid: sources_uuids - uuids_to_delete
                for uuid, sources_uuids in self._sources.items()
                if uuid not in uuids_to_delete
            },
        )

    def sort_dataspecs(
        self, values: Collection[Referrable[ProtobufWithUUID]]
    ) -> Collection[Referring[ProtobufWithUUID]]:
        """Return a sorted list of dataspecs, in the order of the DAG, from the
        root to the nodes (the elements of the input list)."""
        return sort_dataspecs(self, values)
