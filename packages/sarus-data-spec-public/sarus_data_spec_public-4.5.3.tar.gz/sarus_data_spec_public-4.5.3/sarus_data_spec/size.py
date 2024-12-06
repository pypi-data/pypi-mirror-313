from __future__ import annotations

import typing as t

from sarus_data_spec.base import Referring
from sarus_data_spec.dataset import Dataset
from sarus_data_spec.statistics import Statistics
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st


class Size(Referring[sp.Size]):
    """A python class to describe size"""

    def __init__(self, protobuf: sp.Size, store: bool = True) -> None:
        self._referred = {
            protobuf.dataset
        }  # This has to be defined before it is initialized
        super().__init__(protobuf, store=store)

    def prototype(self) -> t.Type[sp.Size]:
        """Return the type of the underlying protobuf."""
        return sp.Size

    def dataset(self) -> Dataset:
        return t.cast(
            Dataset, self.storage().referrable(self._protobuf.dataset)
        )

    def statistics(self) -> Statistics:
        """returns the python object writing the statistics proto"""
        return Statistics(self.protobuf().statistics)


# Builder
def size(
    dataset: st.Dataset,
    statistics: t.Optional[st.Statistics] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Size:
    name = f"{dataset.name()}_sizes"

    return Size(
        sp.Size(
            dataset=dataset.uuid(),
            name=name,
            statistics=statistics.protobuf()
            if statistics is not None
            else statistics,
            properties=properties,
        )
    )
