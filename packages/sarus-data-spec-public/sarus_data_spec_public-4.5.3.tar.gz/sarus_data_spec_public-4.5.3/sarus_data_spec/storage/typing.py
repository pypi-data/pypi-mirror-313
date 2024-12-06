from typing import (
    Callable,
    Collection,
    Dict,
    Optional,
    Protocol,
    Set,
    Tuple,
    Union,
    runtime_checkable,
)

from sarus_data_spec.protobuf.typing import (
    ProtobufWithUUID,
    ProtobufWithUUIDAndDatetime,
)
from sarus_data_spec.typing import DataSpec, Referrable, Referring

# We want to store objects, be able to filter on their types and keep the last
# added in some type and relating to some object


@runtime_checkable
class Storage(Protocol):
    """Storage protocol
    A Storage can store Referrable and Referring values.
    """

    def store(self, value: Referrable[ProtobufWithUUID]) -> None:
        """Write a value to store."""
        ...

    def batch_store(
        self, values: Collection[Referrable[ProtobufWithUUID]]
    ) -> None:
        """Store a collection of referrables in the storage.

        This method does not requires the objects to be provided in the graph
        order.
        """

    def referrable(self, uuid: str) -> Optional[Referrable[ProtobufWithUUID]]:
        """Read a stored value."""
        ...

    def referring(
        self,
        referred: Union[
            Referrable[ProtobufWithUUID],
            Collection[Referrable[ProtobufWithUUID]],
        ],
        type_name: Optional[str] = None,
    ) -> Collection[Referring[ProtobufWithUUID]]:
        """List all values referring to one referred."""
        ...

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
        """Returns the list of all the referring
        (for multiples type_name) of several Referrables."""
        ...

    def all_sources(self, type_name: Optional[str] = None) -> Set[DataSpec]:
        """Returns a set of all sources (with type_name) in the Storage."""
        ...

    def sources(
        self,
        referring: Referrable[ProtobufWithUUID],
        type_name: Optional[str] = None,
    ) -> Set[DataSpec]:
        """List all sources."""
        ...

    def last_referring(
        self,
        referred_uuid: Collection[str],
        type_name: str,
    ) -> Optional[Referring[ProtobufWithUUIDAndDatetime]]:
        """Last value referring to one referred.

        ``last_referring`` returns the last
        ``Referring[ProtobufWithUUIDAndDatetime]``
        object the ``type_name`` of which correspond
        to the argument ``type_name``.

        A typical use is to gather the last ``Status``
        of a ``Dataset`` and a ``Manager``.

        Note that, only time aware ``Referring``
        objects can be accessed this way as
        *last* would not make sense otherwise in the context of Data Spec where
        objects are immutable and eternal.

        Keyword arguments:

        referred:
            Either a ``Referrable`` or a collection of ``Referrable``
            referred by the object we are trying to retrieve

        type_name:
            The ``type_name`` of the Data Spec object we are trying to retrieve
        """
        ...

    def update_referring_with_datetime(
        self,
        referred_uuid: Collection[str],
        type_name: str,
        update: Callable[
            [Referring[ProtobufWithUUIDAndDatetime]],
            Tuple[Referring[ProtobufWithUUIDAndDatetime], bool],
        ],
    ) -> Tuple[Referring[ProtobufWithUUIDAndDatetime], bool]:
        """Update the last referring value of a type atomically

        Update the object ``self.last_referring(referred, type_name)``
        would be returning using the ``update`` function passed as argument.

        Note that in Sarus Data Spec, *update* means: creating an object
        with a more recent timestamp as objects are all immutable and eternal
        to simplify sync, caching and parallelism.

        Therefore everything happens as if::

            update(self.last_referring(referred, type_name))

        was inserted atomically
        (no object can be inserted with a timestamp in-between).

        Keyword arguments:

        referred:
            Either a ``Referrable`` or a collection of ``Referrable``
            referred by the object we are trying to update

        type_name:
            The ``type_name`` of the dataspec object we are trying to update

        update:
            A callable computing the new object to store
            based on the last such object.
        """
        ...

    def create_referring_with_datetime(
        self,
        value: Referring[ProtobufWithUUIDAndDatetime],
        update: Callable[
            [Referring[ProtobufWithUUIDAndDatetime]],
            Tuple[Referring[ProtobufWithUUIDAndDatetime], bool],
        ],
    ) -> Tuple[Referring[ProtobufWithUUIDAndDatetime], bool]: ...

    def type_name(
        self, type_name: str
    ) -> Collection[Referrable[ProtobufWithUUID]]:
        """List all values from a given type_name."""
        ...

    def delete(self, uuid: str) -> None:
        """Delete a stored value from the database."""
        ...

    def delete_type(self, type_name: str) -> None:
        """Delete all elements of a given type_name
        from the database and all the referrings"""
        ...


@runtime_checkable
class HasStorage(Protocol):
    """Has a storage for persistent objects."""

    def storage(self) -> Storage:
        """Return a storage (usually a singleton)."""
        ...
