from __future__ import annotations

import typing as t

import numpy as np

from sarus_data_spec.base import Base
from sarus_data_spec.constants import ARRAY_VALUES, LIST_VALUES, OPTIONAL_VALUE
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st


class Statistics(Base[sp.Statistics]):
    """A python class to describe statistics"""

    def prototype(self) -> t.Type[sp.Statistics]:
        """Return the type of the underlying protobuf."""
        return sp.Statistics

    def name(self) -> str:
        """Return the statistics name"""
        return self.protobuf().name

    def distribution(self) -> st.Distribution:
        return Distribution(
            getattr(
                self.protobuf(),
                t.cast(str, self.protobuf().WhichOneof("statistics")),
            ).distribution
        )

    def size(self) -> int:
        return t.cast(
            int,
            getattr(
                self.protobuf(),
                t.cast(str, self.protobuf().WhichOneof("statistics")),
            ).size,
        )

    def multiplicity(self) -> float:
        return t.cast(
            float,
            getattr(
                self.protobuf(),
                t.cast(str, self.protobuf().WhichOneof("statistics")),
            ).multiplicity,
        )

    def accept(self, visitor: st.StatisticsVisitor) -> None:
        dispatch: t.Callable[[], None] = {
            "null": lambda: visitor.Null(
                self._protobuf.null.size, self._protobuf.null.multiplicity
            ),
            "unit": lambda: visitor.Unit(
                self._protobuf.unit.size, self._protobuf.unit.multiplicity
            ),
            "boolean": lambda: visitor.Boolean(
                size=self._protobuf.boolean.size,
                multiplicity=self._protobuf.boolean.multiplicity,
                probabilities=[
                    element.probability
                    for element in self._protobuf.boolean.distribution.boolean.points  # noqa: E501
                ],
                names=[
                    element.name
                    for element in self._protobuf.boolean.distribution.boolean.points  # noqa: E501
                ],
                values=[
                    element.value
                    for element in self._protobuf.boolean.distribution.boolean.points  # noqa: E501
                ],
            ),
            "integer": lambda: visitor.Integer(
                size=self._protobuf.integer.size,
                multiplicity=self._protobuf.integer.multiplicity,
                min_value=self._protobuf.integer.distribution.integer.min,
                max_value=self._protobuf.integer.distribution.integer.max,
                probabilities=[
                    element.probability
                    for element in self._protobuf.integer.distribution.integer.points  # noqa: E501
                ],
                values=[
                    element.value
                    for element in self._protobuf.integer.distribution.integer.points  # noqa: E501
                ],
            ),
            "id": lambda: visitor.Id(
                self._protobuf.id.size, self._protobuf.id.multiplicity
            ),
            "enum": lambda: visitor.Enum(
                size=self._protobuf.enum.size,
                multiplicity=self._protobuf.enum.multiplicity,
                probabilities=[
                    element.probability
                    for element in self._protobuf.enum.distribution.enum.points  # noqa: E501
                ],
                names=[
                    element.name
                    for element in self._protobuf.enum.distribution.enum.points  # noqa: E501
                ],
                values=[
                    element.value
                    for element in self._protobuf.enum.distribution.enum.points  # noqa: E501
                ],
            ),
            "float": lambda: visitor.Float(
                size=self._protobuf.float.size,
                multiplicity=self._protobuf.float.multiplicity,
                min_value=self._protobuf.float.distribution.double.min,
                max_value=self._protobuf.float.distribution.double.max,
                probabilities=[
                    element.probability
                    for element in self._protobuf.float.distribution.double.points  # noqa: E501
                ],
                values=[
                    element.value
                    for element in self._protobuf.float.distribution.double.points  # noqa: E501
                ],
            ),
            "text": lambda: visitor.Text(
                size=self._protobuf.text.size,
                multiplicity=self._protobuf.text.multiplicity,
                min_value=self._protobuf.text.distribution.integer.min,
                max_value=self._protobuf.text.distribution.integer.max,
                probabilities=[
                    element.probability
                    for element in self._protobuf.text.distribution.integer.points  # noqa: E501
                ],
                values=[
                    element.value
                    for element in self._protobuf.text.distribution.integer.points  # noqa: E501
                ],
                example=self._protobuf.text.example,
            ),
            "bytes": lambda: visitor.Bytes(
                self._protobuf.bytes.size, self._protobuf.bytes.multiplicity
            ),
            "struct": lambda: visitor.Struct(
                {
                    field.name: Statistics(field.statistics)
                    for field in self._protobuf.struct.fields
                },
                self._protobuf.struct.size,
                name=self._protobuf.name,
                multiplicity=self._protobuf.struct.multiplicity,
                properties=self._protobuf.properties,
            ),
            "union": lambda: visitor.Union(
                {
                    field.name: Statistics(field.statistics)
                    for field in self._protobuf.union.fields
                },
                size=self._protobuf.union.size,
                name=self._protobuf.name,
                multiplicity=self._protobuf.union.multiplicity,
                properties=self._protobuf.properties,
            ),
            "optional": lambda: visitor.Optional(
                Statistics(self._protobuf.optional.statistics),
                size=self._protobuf.optional.size,
                multiplicity=self._protobuf.optional.multiplicity,
            ),
            "list": lambda: visitor.List(
                statistics=Statistics(self._protobuf.list.statistics),
                size=self._protobuf.list.size,
                multiplicity=self._protobuf.list.multiplicity,
                min_value=self._protobuf.list.distribution.integer.min,
                max_value=self._protobuf.list.distribution.integer.max,
                probabilities=[
                    element.probability
                    for element in self._protobuf.list.distribution.integer.points  # noqa: E501
                ],
                values=[
                    element.value
                    for element in self._protobuf.list.distribution.integer.points  # noqa: E501
                ],
            ),
            "array": lambda: visitor.Array(
                statistics=Statistics(self._protobuf.array.statistics),
                size=self._protobuf.array.size,
                multiplicity=self._protobuf.array.multiplicity,
                min_values=[
                    distribution.double.min
                    for distribution in self._protobuf.array.distributions
                ],
                max_values=[
                    distribution.double.max
                    for distribution in self._protobuf.array.distributions
                ],
                probabilities=[
                    [
                        element.probability
                        for element in distribution.double.points
                    ]
                    for distribution in self._protobuf.array.distributions
                ],
                values=[
                    [element.value for element in distribution.double.points]
                    for distribution in self._protobuf.array.distributions
                ],
            ),
            "datetime": lambda: visitor.Datetime(
                size=self._protobuf.datetime.size,
                multiplicity=self._protobuf.datetime.multiplicity,
                min_value=self._protobuf.datetime.distribution.integer.min,
                max_value=self._protobuf.datetime.distribution.integer.max,
                probabilities=[
                    element.probability
                    for element in self._protobuf.datetime.distribution.integer.points  # noqa: E501
                ],
                values=[
                    element.value
                    for element in self._protobuf.datetime.distribution.integer.points  # noqa: E501
                ],
            ),
            "date": lambda: visitor.Date(
                size=self._protobuf.date.size,
                multiplicity=self._protobuf.date.multiplicity,
                min_value=self._protobuf.date.distribution.integer.min,
                max_value=self._protobuf.date.distribution.integer.max,
                probabilities=[
                    element.probability
                    for element in self._protobuf.date.distribution.integer.points  # noqa: E501
                ],
                values=[
                    element.value
                    for element in self._protobuf.date.distribution.integer.points  # noqa: E501
                ],
            ),
            "time": lambda: visitor.Time(
                size=self._protobuf.time.size,
                multiplicity=self._protobuf.time.multiplicity,
                min_value=self._protobuf.time.distribution.integer.min,
                max_value=self._protobuf.time.distribution.integer.max,
                probabilities=[
                    element.probability
                    for element in self._protobuf.time.distribution.integer.points  # noqa: E501
                ],
                values=[
                    element.value
                    for element in self._protobuf.time.distribution.integer.points  # noqa: E501
                ],
            ),
            "duration": lambda: visitor.Duration(
                size=self._protobuf.duration.size,
                multiplicity=self._protobuf.duration.multiplicity,
                min_value=self._protobuf.duration.distribution.integer.min,
                max_value=self._protobuf.duration.distribution.integer.max,
                probabilities=[
                    element.probability
                    for element in self._protobuf.duration.distribution.integer.points  # noqa: E501
                ],
                values=[
                    element.value
                    for element in self._protobuf.duration.distribution.integer.points  # noqa: E501
                ],
            ),
            "constrained": lambda: visitor.Constrained(
                Statistics(self._protobuf.constrained.statistics),
                self._protobuf.constrained.size,
                self._protobuf.constrained.multiplicity,
            ),
            None: lambda: None,
        }[self._protobuf.WhichOneof("statistics")]
        dispatch()

    def nodes_statistics(self, path: st.Path) -> t.List[st.Statistics]:
        """Returns the List of each statistics corresponding at the leaves of
        path"""

        class Select(st.StatisticsVisitor):
            def __init__(self, statistics: st.Statistics):
                self.result = [statistics]

            def Struct(
                self,
                fields: t.Mapping[str, st.Statistics],
                size: int,
                multiplicity: float,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                result = []
                for sub_path in path.sub_paths():
                    result.extend(
                        fields[sub_path.label()].nodes_statistics(sub_path)
                    )
                if len(result) > 0:
                    self.result = result
                    # otherwise struct is empty and it is a terminal node

            def Union(
                self,
                fields: t.Mapping[str, st.Statistics],
                size: int,
                multiplicity: float,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                result = []
                for sub_path in path.sub_paths():
                    result.extend(
                        fields[sub_path.label()].nodes_statistics(sub_path)
                    )
                if len(result) > 0:
                    self.result = result  # otherwise union is empty and it is a terminal node  # noqa: E501

            def Optional(
                self,
                statistics: st.Statistics,
                size: int,
                multiplicity: float,
            ) -> None:
                result = []
                if len(path.sub_paths()) == 1:
                    result.extend(
                        statistics.nodes_statistics(path.sub_paths()[0])
                    )
                    self.result = result

            def List(
                self,
                statistics: st.Statistics,
                size: int,
                multiplicity: float,
                min_value: int,
                max_value: int,
                name: str = "List",
                probabilities: t.Optional[t.List[float]] = None,
                values: t.Optional[t.List[int]] = None,
            ) -> None:
                result = []
                if len(path.sub_paths()) == 1:
                    result.extend(
                        statistics.nodes_statistics(path.sub_paths()[0])
                    )
                    self.result = result

            def Array(
                self,
                statistics: st.Statistics,
                size: int,
                multiplicity: float,
                min_values: t.Optional[t.List[float]] = None,
                max_values: t.Optional[t.List[float]] = None,
                name: str = "Array",
                probabilities: t.Optional[t.List[t.List[float]]] = None,
                values: t.Optional[t.List[t.List[float]]] = None,
            ) -> None:
                result = []
                if len(path.sub_paths()) == 1:
                    result.extend(
                        statistics.nodes_statistics(path.sub_paths()[0])
                    )
                    self.result = result

            def Constrained(
                self,
                statistics: st.Statistics,
                size: int,
                multiplicity: float,
            ) -> None:
                result = []
                if len(path.sub_paths()) == 1:
                    result.extend(
                        statistics.nodes_statistics(path.sub_paths()[0])
                    )
                    self.result = result

            def Bytes(self, size: int, multiplicity: float) -> None:
                pass

            def Date(
                self,
                size: int,
                multiplicity: float,
                min_value: int,
                max_value: int,
                probabilities: t.Optional[t.List[float]] = None,
                values: t.Optional[t.List[int]] = None,
            ) -> None:
                pass

            def Time(
                self,
                size: int,
                multiplicity: float,
                min_value: int,
                max_value: int,
                probabilities: t.Optional[t.List[float]] = None,
                values: t.Optional[t.List[int]] = None,
            ) -> None:
                pass

            def Datetime(
                self,
                size: int,
                multiplicity: float,
                min_value: int,
                max_value: int,
                probabilities: t.Optional[t.List[float]] = None,
                values: t.Optional[t.List[int]] = None,
            ) -> None:
                pass

            def Duration(
                self,
                size: int,
                multiplicity: float,
                min_value: int,
                max_value: int,
                probabilities: t.Optional[t.List[float]] = None,
                values: t.Optional[t.List[int]] = None,
            ) -> None:
                pass

            def Null(self, size: int, multiplicity: float) -> None:
                pass

            def Unit(self, size: int, multiplicity: float) -> None:
                pass

            def Boolean(
                self,
                size: int,
                multiplicity: float,
                probabilities: t.Optional[t.List[float]] = None,
                names: t.Optional[t.List[bool]] = None,
                values: t.Optional[t.List[int]] = None,
            ) -> None:
                pass

            def Id(self, size: int, multiplicity: float) -> None:
                pass

            def Integer(
                self,
                size: int,
                multiplicity: float,
                min_value: int,
                max_value: int,
                probabilities: t.Optional[t.List[float]] = None,
                values: t.Optional[t.List[int]] = None,
            ) -> None:
                pass

            def Enum(
                self,
                size: int,
                multiplicity: float,
                probabilities: t.Optional[t.List[float]] = None,
                names: t.Optional[t.List[str]] = None,
                values: t.Optional[t.List[float]] = None,
                name: str = "Enum",
            ) -> None:
                pass

            def Float(
                self,
                size: int,
                multiplicity: float,
                min_value: float,
                max_value: float,
                probabilities: t.Optional[t.List[float]] = None,
                values: t.Optional[t.List[float]] = None,
            ) -> None:
                pass

            def Text(
                self,
                size: int,
                multiplicity: float,
                min_value: int,
                max_value: int,
                example: str = "",
                probabilities: t.Optional[t.List[float]] = None,
                values: t.Optional[t.List[int]] = None,
            ) -> None:
                pass

        visitor = Select(statistics=self)
        self.accept(visitor)
        return visitor.result

    def children(self: st.Statistics) -> t.Dict[str, st.Statistics]:
        """Returns the children contained in the type tree structure"""

        class GetChildren(st.StatisticsVisitor):
            result: t.Dict[str, st.Statistics] = {}

            def __init__(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ):
                self.properties = properties

            def Struct(
                self,
                fields: t.Mapping[str, st.Statistics],
                size: int,
                multiplicity: float,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = t.cast(t.Dict[str, st.Statistics], fields)

            def Union(
                self,
                fields: t.Mapping[str, st.Statistics],
                size: int,
                multiplicity: float,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = t.cast(t.Dict[str, st.Statistics], fields)

            def Optional(
                self,
                statistics: st.Statistics,
                size: int,
                multiplicity: float,
            ) -> None:
                self.result = {OPTIONAL_VALUE: statistics}

            def List(
                self,
                statistics: st.Statistics,
                size: int,
                multiplicity: float,
                min_value: int,
                max_value: int,
                name: str = "List",
                probabilities: t.Optional[t.List[float]] = None,
                values: t.Optional[t.List[int]] = None,
            ) -> None:
                self.result = {LIST_VALUES: statistics}

            def Array(
                self,
                statistics: st.Statistics,
                size: int,
                multiplicity: float,
                min_values: t.Optional[t.List[float]] = None,
                max_values: t.Optional[t.List[float]] = None,
                name: str = "Array",
                probabilities: t.Optional[t.List[t.List[float]]] = None,
                values: t.Optional[t.List[t.List[float]]] = None,
            ) -> None:
                self.result = {ARRAY_VALUES: statistics}

            def Bytes(self, size: int, multiplicity: float) -> None:
                pass

            def Date(
                self,
                size: int,
                multiplicity: float,
                min_value: int,
                max_value: int,
                probabilities: t.Optional[t.List[float]] = None,
                values: t.Optional[t.List[int]] = None,
            ) -> None:
                pass

            def Time(
                self,
                size: int,
                multiplicity: float,
                min_value: int,
                max_value: int,
                probabilities: t.Optional[t.List[float]] = None,
                values: t.Optional[t.List[int]] = None,
            ) -> None:
                pass

            def Datetime(
                self,
                size: int,
                multiplicity: float,
                min_value: int,
                max_value: int,
                probabilities: t.Optional[t.List[float]] = None,
                values: t.Optional[t.List[int]] = None,
            ) -> None:
                pass

            def Duration(
                self,
                size: int,
                multiplicity: float,
                min_value: int,
                max_value: int,
                probabilities: t.Optional[t.List[float]] = None,
                values: t.Optional[t.List[int]] = None,
            ) -> None:
                pass

            def Null(self, size: int, multiplicity: float) -> None:
                pass

            def Unit(self, size: int, multiplicity: float) -> None:
                pass

            def Boolean(
                self,
                size: int,
                multiplicity: float,
                probabilities: t.Optional[t.List[float]] = None,
                names: t.Optional[t.List[bool]] = None,
                values: t.Optional[t.List[int]] = None,
            ) -> None:
                pass

            def Id(self, size: int, multiplicity: float) -> None:
                pass

            def Integer(
                self,
                size: int,
                multiplicity: float,
                min_value: int,
                max_value: int,
                probabilities: t.Optional[t.List[float]] = None,
                values: t.Optional[t.List[int]] = None,
            ) -> None:
                pass

            def Enum(
                self,
                size: int,
                multiplicity: float,
                probabilities: t.Optional[t.List[float]] = None,
                names: t.Optional[t.List[str]] = None,
                values: t.Optional[t.List[float]] = None,
                name: str = "Enum",
            ) -> None:
                pass

            def Float(
                self,
                size: int,
                multiplicity: float,
                min_value: float,
                max_value: float,
                probabilities: t.Optional[t.List[float]] = None,
                values: t.Optional[t.List[float]] = None,
            ) -> None:
                pass

            def Text(
                self,
                size: int,
                multiplicity: float,
                min_value: int,
                max_value: int,
                example: str = "",
                probabilities: t.Optional[t.List[float]] = None,
                values: t.Optional[t.List[int]] = None,
            ) -> None:
                pass

            def Constrained(
                self, statistics: st.Statistics, size: int, multiplicity: float
            ) -> None:
                raise NotImplementedError

        visitor = GetChildren(properties=self.properties())
        self.accept(visitor)
        return visitor.result


class Distribution(Base[sp.Distribution]):
    """A python class to describe distributions"""

    def prototype(self) -> t.Type[sp.Distribution]:
        """Return the type of the underlying protobuf."""
        return sp.Distribution

    def values(self) -> t.Union[t.List[float], t.List[int]]:
        return [
            element.value
            for element in getattr(
                self.protobuf(),
                t.cast(str, self.protobuf().WhichOneof("distribution")),
            ).points
        ]

    def probabilities(self) -> t.List[float]:
        return [
            element.probability
            for element in getattr(
                self.protobuf(),
                t.cast(str, self.protobuf().WhichOneof("distribution")),
            ).points
        ]

    def names(self) -> t.Union[t.List[bool], t.List[str]]:
        distrib_type = t.cast(str, self.protobuf().WhichOneof("distribution"))
        if distrib_type in ["integer", "double"]:
            raise TypeError(
                f"{distrib_type} distribution has no attribute names"
            )
        return [
            element.name
            for element in getattr(self.protobuf(), distrib_type).points
        ]

    def min_value(self) -> t.Union[int, float]:
        distrib_type = t.cast(str, self.protobuf().WhichOneof("distribution"))
        if distrib_type in ["enum", "boolean"]:
            raise TypeError(f"{distrib_type} distribution has no min")
        # mypy thinks the return should be Any
        if distrib_type == "float":
            return t.cast(float, getattr(self.protobuf(), distrib_type).min)
        return t.cast(int, getattr(self.protobuf(), distrib_type).min)

    def max_value(self) -> t.Union[int, float]:
        distrib_type = t.cast(str, self.protobuf().WhichOneof("distribution"))
        if distrib_type in ["enum", "boolean"]:
            raise TypeError(f"{distrib_type} distribution has no max")
        # mypy thinks the return should be Any
        if distrib_type == "float":
            return t.cast(float, getattr(self.protobuf(), distrib_type).max)
        return t.cast(int, getattr(self.protobuf(), distrib_type).max)


# A few builders


# Distributions
def Integer_Distribution(
    min_value: t.Optional[int] = None,
    max_value: t.Optional[int] = None,
    probabilities: t.Optional[t.List[float]] = None,
    values: t.Optional[t.List[int]] = None,
) -> Distribution:
    if min_value is None:
        min_value = np.iinfo(np.int64).min
    if max_value is None:
        max_value = np.iinfo(np.int64).max
    if probabilities is None:
        probabilities = []
    if values is None:
        values = []
    return Distribution(
        sp.Distribution(
            integer=sp.Distribution.Integer(
                points=[
                    sp.Distribution.Integer.Point(
                        value=value, probability=probability
                    )
                    for value, probability in zip(values, probabilities)
                ],
                min=min_value,
                max=max_value,
            )
        )
    )


def Boolean_Distribution(
    probabilities: t.Optional[t.List[float]] = None,
    names: t.Optional[t.List[bool]] = None,
    values: t.Optional[t.List[int]] = None,
) -> Distribution:
    if probabilities is None:
        probabilities = []
    if names is None:
        names = []
    if values is None:
        values = []
    return Distribution(
        sp.Distribution(
            boolean=sp.Distribution.Boolean(
                points=[
                    sp.Distribution.Boolean.Point(
                        name=name, value=value, probability=probability
                    )
                    for name, value, probability in zip(
                        names, values, probabilities
                    )
                ]
            )
        )
    )


def Double_Distribution(
    min_value: t.Optional[float] = None,
    max_value: t.Optional[float] = None,
    probabilities: t.Optional[t.List[float]] = None,
    values: t.Optional[t.List[float]] = None,
) -> Distribution:
    if min_value is None:
        min_value = np.finfo(np.float64).min  # type:ignore
    if max_value is None:
        max_value = np.finfo(np.float64).max  # type:ignore
    if probabilities is None:
        probabilities = []
    if values is None:
        values = []
    return Distribution(
        sp.Distribution(
            double=sp.Distribution.Double(
                points=[
                    sp.Distribution.Double.Point(
                        value=value, probability=probability
                    )
                    for value, probability in zip(values, probabilities)
                ],
                min=min_value,  # type:ignore
                max=max_value,  # type: ignore
            )
        )
    )


def Enum_Distribution(
    probabilities: t.Optional[t.List[float]] = None,
    names: t.Optional[t.List[str]] = None,
    values: t.Optional[t.List[float]] = None,
) -> Distribution:
    if probabilities is None:
        probabilities = []
    if names is None:
        names = []
    if values is None:
        values = [i for i in range(len(names))]
    return Distribution(
        sp.Distribution(
            enum=sp.Distribution.Enum(
                points=[
                    sp.Distribution.Enum.Point(
                        name=name, value=value, probability=probability
                    )
                    for name, value, probability in zip(
                        names, values, probabilities
                    )
                ]
            )
        )
    )


# Statistics
def Null(size: int, multiplicity: float) -> Statistics:
    return Statistics(
        sp.Statistics(
            name="Null",
            null=sp.Statistics.Null(size=size, multiplicity=multiplicity),
        )
    )


def Unit(
    size: int,
    multiplicity: float,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Statistics:
    return Statistics(
        sp.Statistics(
            name="Unit",
            unit=sp.Statistics.Unit(size=size, multiplicity=multiplicity),
            properties=properties,
        )
    )


def Id(size: int, multiplicity: float) -> Statistics:
    return Statistics(
        sp.Statistics(
            name="Id",
            id=sp.Statistics.Id(size=size, multiplicity=multiplicity),
        )
    )


def Boolean(
    size: int,
    multiplicity: float,
    probabilities: t.Optional[t.List[float]] = None,
    names: t.Optional[t.List[bool]] = None,
    values: t.Optional[t.List[int]] = None,
) -> Statistics:
    return Statistics(
        sp.Statistics(
            name="Boolean",
            boolean=sp.Statistics.Boolean(
                distribution=Boolean_Distribution(
                    probabilities=probabilities, names=names, values=values
                ).protobuf(),
                size=size,
                multiplicity=multiplicity,
            ),
        )
    )


def Integer(
    size: int,
    multiplicity: float,
    min_value: t.Optional[int] = None,
    max_value: t.Optional[int] = None,
    probabilities: t.Optional[t.List[float]] = None,
    values: t.Optional[t.List[int]] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Statistics:
    return Statistics(
        sp.Statistics(
            name="Integer",
            integer=sp.Statistics.Integer(
                distribution=Integer_Distribution(
                    min_value=min_value,
                    max_value=max_value,
                    probabilities=probabilities,
                    values=values,
                ).protobuf(),
                size=size,
                multiplicity=multiplicity,
            ),
            properties=properties,
        )
    )


def Enum(
    size: int,
    multiplicity: float,
    probabilities: t.Optional[t.List[float]] = None,
    names: t.Optional[t.List[str]] = None,
    values: t.Optional[t.List[float]] = None,
    name: str = "Enum",
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Statistics:
    return Statistics(
        sp.Statistics(
            name=name,
            enum=sp.Statistics.Enum(
                distribution=Enum_Distribution(
                    probabilities=probabilities, values=values, names=names
                ).protobuf(),
                size=size,
                multiplicity=multiplicity,
            ),
            properties=properties,
        )
    )


def Float(
    size: int,
    multiplicity: float,
    min_value: t.Optional[float] = None,
    max_value: t.Optional[float] = None,
    probabilities: t.Optional[t.List[float]] = None,
    values: t.Optional[t.List[float]] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Statistics:
    return Statistics(
        sp.Statistics(
            name="Float",
            float=sp.Statistics.Float(
                distribution=Double_Distribution(
                    min_value=min_value,
                    max_value=max_value,
                    probabilities=probabilities,
                    values=values,
                ).protobuf(),
                size=size,
                multiplicity=multiplicity,
            ),
            properties=properties,
        )
    )


def Text(
    size: int,
    multiplicity: float,
    example: str = "",
    min_value: t.Optional[int] = None,
    max_value: t.Optional[int] = None,
    probabilities: t.Optional[t.List[float]] = None,
    values: t.Optional[t.List[int]] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Statistics:
    return Statistics(
        sp.Statistics(
            name="Text",
            text=sp.Statistics.Text(
                distribution=Integer_Distribution(
                    min_value=min_value,
                    max_value=max_value,
                    probabilities=probabilities,
                    values=values,
                ).protobuf(),
                example=example,
                size=size,
                multiplicity=multiplicity,
            ),
            properties=properties,
        )
    )


def Bytes(size: int, multiplicity: float) -> Statistics:
    return Statistics(
        sp.Statistics(
            name="Bytes",
            bytes=sp.Statistics.Bytes(size=size, multiplicity=multiplicity),
        )
    )


def Struct(
    fields: t.Mapping[str, st.Statistics],
    size: int,
    multiplicity: float,
    name: t.Optional[str] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Statistics:
    return Statistics(
        sp.Statistics(
            name="Struct" if name is None else name,
            struct=sp.Statistics.Struct(
                fields=[
                    sp.Statistics.Struct.Field(
                        name=name, statistics=statistics.protobuf()
                    )
                    for name, statistics in fields.items()
                ],
                size=size,
                multiplicity=multiplicity,
            ),
            properties=properties,
        )
    )


def Union(
    fields: t.Mapping[str, st.Statistics],
    size: int,
    multiplicity: float,
    name: str = "Union",
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Statistics:
    return Statistics(
        sp.Statistics(
            name=name,
            union=sp.Statistics.Union(
                fields=[
                    sp.Statistics.Union.Field(
                        name=field_name, statistics=field_stat.protobuf()
                    )
                    for field_name, field_stat in fields.items()
                ],
                size=size,
                multiplicity=multiplicity,
            ),
            properties=properties,
        )
    )


def Optional(
    statistics: st.Statistics,
    size: int,
    multiplicity: float,
    name: str = "Optional",
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Statistics:
    return Statistics(
        sp.Statistics(
            name=name,
            optional=sp.Statistics.Optional(
                statistics=statistics.protobuf(),
                size=size,
                multiplicity=multiplicity,
            ),
            properties=properties,
        )
    )


def List(
    statistics: st.Statistics,
    size: int,
    multiplicity: float,
    name: str = "List",
    min_value: t.Optional[int] = None,
    max_value: t.Optional[int] = None,
    probabilities: t.Optional[t.List[float]] = None,
    values: t.Optional[t.List[int]] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Statistics:
    return Statistics(
        sp.Statistics(
            name=name,
            list=sp.Statistics.List(
                statistics=statistics.protobuf(),
                distribution=Integer_Distribution(
                    min_value=min_value,
                    max_value=max_value,
                    probabilities=probabilities,
                    values=values,
                ).protobuf(),
                size=size,
                multiplicity=multiplicity,
            ),
            properties=properties,
        )
    )


def Array(
    statistics: st.Statistics,
    size: int,
    multiplicity: float,
    name: str = "Array",
    min_values: t.Optional[t.List[float]] = None,
    max_values: t.Optional[t.List[float]] = None,
    probabilities: t.Optional[t.List[t.List[float]]] = None,
    values: t.Optional[t.List[t.List[float]]] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Statistics:
    if min_values is None:
        min_values = []
    if max_values is None:
        max_values = []
    if probabilities is None:
        probabilities = [[]]
    if values is None:
        values = [[]]
    distributions = [
        sp.Distribution(
            double=sp.Distribution.Double(
                points=[
                    sp.Distribution.Double.Point(
                        value=value, probability=probability
                    )
                    for value, probability in zip(
                        value_dimension, probability_dimension
                    )
                ],
                min=min_value,
                max=max_value,
            )
        )
        for value_dimension, probability_dimension, min_value, max_value in zip(  # noqa: E501
            values, probabilities, min_values, max_values
        )
    ]
    return Statistics(
        sp.Statistics(
            name=name,
            array=sp.Statistics.Array(
                statistics=statistics.protobuf(),
                distributions=distributions,
                size=size,
                multiplicity=multiplicity,
            ),
            properties=properties,
        )
    )


def Datetime(
    size: int,
    multiplicity: float,
    min_value: t.Optional[int] = None,
    max_value: t.Optional[int] = None,
    probabilities: t.Optional[t.List[float]] = None,
    values: t.Optional[t.List[int]] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Statistics:
    return Statistics(
        sp.Statistics(
            name="Datetime",
            datetime=sp.Statistics.Datetime(
                distribution=Integer_Distribution(
                    min_value=min_value,
                    max_value=max_value,
                    probabilities=probabilities,
                    values=values,
                ).protobuf(),
                size=size,
                multiplicity=multiplicity,
            ),
            properties=properties,
        )
    )


def Date(
    size: int,
    multiplicity: float,
    min_value: t.Optional[int] = None,
    max_value: t.Optional[int] = None,
    probabilities: t.Optional[t.List[float]] = None,
    values: t.Optional[t.List[int]] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Statistics:
    return Statistics(
        sp.Statistics(
            name="Date",
            date=sp.Statistics.Date(
                distribution=Integer_Distribution(
                    min_value=min_value,
                    max_value=max_value,
                    probabilities=probabilities,
                    values=values,
                ).protobuf(),
                size=size,
                multiplicity=multiplicity,
            ),
            properties=properties,
        )
    )


def Time(
    size: int,
    multiplicity: float,
    min_value: t.Optional[int] = None,
    max_value: t.Optional[int] = None,
    probabilities: t.Optional[t.List[float]] = None,
    values: t.Optional[t.List[int]] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Statistics:
    return Statistics(
        sp.Statistics(
            name="Time",
            time=sp.Statistics.Time(
                distribution=Integer_Distribution(
                    min_value=min_value,
                    max_value=max_value,
                    probabilities=probabilities,
                    values=values,
                ).protobuf(),
                size=size,
                multiplicity=multiplicity,
            ),
            properties=properties,
        )
    )


def Duration(
    size: int,
    multiplicity: float,
    min_value: t.Optional[int] = None,
    max_value: t.Optional[int] = None,
    probabilities: t.Optional[t.List[float]] = None,
    values: t.Optional[t.List[int]] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Statistics:
    return Statistics(
        sp.Statistics(
            name="Duration",
            duration=sp.Statistics.Duration(
                distribution=Integer_Distribution(
                    min_value=min_value,
                    max_value=max_value,
                    probabilities=probabilities,
                    values=values,
                ).protobuf(),
                size=size,
                multiplicity=multiplicity,
            ),
            properties=properties,
        )
    )


def Constrained(
    statistics: st.Statistics,
    size: int,
    multiplicity: float,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Statistics:
    return Statistics(
        sp.Statistics(
            name="Constrained",
            constrained=sp.Statistics.Constrained(
                statistics=statistics.protobuf(),
                size=size,
                multiplicity=multiplicity,
            ),
            properties=properties,
        )
    )


# A New Visitor base implementation
class StatisticsVisitor(st.StatisticsVisitor):
    """A base implementation for visitor class"""

    def default(self) -> None:
        raise NotImplementedError

    def Null(self, size: int, multiplicity: float) -> None:
        self.default()

    def Unit(self, size: int, multiplicity: float) -> None:
        self.default()

    def Boolean(
        self,
        size: int,
        multiplicity: float,
        probabilities: t.Optional[t.List[float]] = None,
        names: t.Optional[t.List[bool]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None:
        self.default()

    def Id(self, size: int, multiplicity: float) -> None:
        self.default()

    def Integer(
        self,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None:
        self.default()

    def Enum(
        self,
        size: int,
        multiplicity: float,
        probabilities: t.Optional[t.List[float]] = None,
        names: t.Optional[t.List[str]] = None,
        values: t.Optional[t.List[float]] = None,
        name: str = "Enum",
    ) -> None:
        self.default()

    def Float(
        self,
        size: int,
        multiplicity: float,
        min_value: float,
        max_value: float,
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[float]] = None,
    ) -> None:
        self.default()

    def Text(
        self,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        example: str = "",
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None:
        self.default()

    def Bytes(self, size: int, multiplicity: float) -> None:
        self.default()

    def Struct(
        self,
        fields: t.Mapping[str, st.Statistics],
        size: int,
        multiplicity: float,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        self.default()

    def Union(
        self,
        fields: t.Mapping[str, st.Statistics],
        size: int,
        multiplicity: float,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        self.default()

    def Optional(
        self, statistics: st.Statistics, size: int, multiplicity: float
    ) -> None:
        self.default()

    def List(
        self,
        statistics: st.Statistics,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        name: str = "List",
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None:
        self.default()

    def Array(
        self,
        statistics: st.Statistics,
        size: int,
        multiplicity: float,
        min_values: t.Optional[t.List[float]] = None,
        max_values: t.Optional[t.List[float]] = None,
        name: str = "Array",
        probabilities: t.Optional[t.List[t.List[float]]] = None,
        values: t.Optional[t.List[t.List[float]]] = None,
    ) -> None:
        self.default()

    def Datetime(
        self,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None:
        self.default()

    def Time(
        self,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None:
        self.default()

    def Date(
        self,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None:
        self.default()

    def Duration(
        self,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None:
        self.default()

    def Constrained(
        self, statistics: st.Statistics, size: int, multiplicity: float
    ) -> None:
        self.default()


if t.TYPE_CHECKING:
    test_stat: st.Statistics = Statistics(sp.Statistics())
    test_dis: st.Distribution = Distribution(sp.Distribution())
