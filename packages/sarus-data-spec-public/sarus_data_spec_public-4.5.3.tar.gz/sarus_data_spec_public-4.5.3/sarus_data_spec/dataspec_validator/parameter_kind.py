from __future__ import annotations

from enum import Enum, auto
import itertools as it
import typing as t


class Operator(Enum):
    AND = auto()
    OR = auto()


class AcceptanceCondition:
    """Maintain a Sum Of Product (SOP) form of the condition.

    The Python representation is a list of sets.
    """

    products: t.List[t.Set[t.Union[AcceptanceCondition, ParameterKind]]]

    def __init__(
        self,
        left: t.Union[AcceptanceCondition, ParameterKind],
        right: t.Union[AcceptanceCondition, ParameterKind],
        operator: Operator,
    ):
        if isinstance(left, AcceptanceCondition):
            left_condition = t.cast(AcceptanceCondition, left)
            left_products = left_condition.products
        else:
            left_kind = t.cast(ParameterKind, left)
            left_products = [{left_kind}]

        if isinstance(right, AcceptanceCondition):
            right_condition = t.cast(AcceptanceCondition, right)
            right_products = right_condition.products
        else:
            right_kind = t.cast(ParameterKind, right)
            right_products = [{right_kind}]

        if operator == Operator.OR:
            self.products = left_products + right_products
        else:
            self.products = [
                set(right) | set(left)
                for right, left in it.product(right_products, left_products)
            ]

    def __repr__(self) -> str:
        return " ∨ ".join(
            [
                f"({' ∧ '.join([str(p) for p in product])})"
                for product in self.products
            ]
        )

    def __and__(
        self, other: t.Union[AcceptanceCondition, ParameterKind]
    ) -> AcceptanceCondition:
        return AcceptanceCondition(self, other, Operator.AND)

    def __or__(
        self, other: t.Union[AcceptanceCondition, ParameterKind]
    ) -> AcceptanceCondition:
        return AcceptanceCondition(self, other, Operator.OR)

    def isin(self, other: t.Union[AcceptanceCondition, ParameterKind]) -> bool:
        return is_accepted(self, other)


def is_accepted(
    accepted_kind: t.Union[AcceptanceCondition, ParameterKind],
    incoming_kind: t.Union[AcceptanceCondition, ParameterKind],
) -> bool:
    """Checks if the incoming parameter kind satisfies the
    acceptance condition.
    """
    if not isinstance(accepted_kind, ParameterKind):
        accepted_products = accepted_kind.products
    else:
        accepted_products = [{accepted_kind}]

    if not isinstance(incoming_kind, ParameterKind):
        incoming_products = incoming_kind.products
    else:
        incoming_products = [{incoming_kind}]

    return any(
        [
            accepted_prod.issubset(incoming_prod)
            for incoming_prod, accepted_prod in it.product(
                incoming_products, accepted_products
            )
        ]
    )


class ParameterKind(Enum):
    DATASET = auto()
    SCALAR = auto()
    PUP = auto()
    PUBLIC = auto()
    STATIC = auto()
    TRANSFORM = auto()

    def __and__(
        self, other: t.Union[AcceptanceCondition, ParameterKind]
    ) -> AcceptanceCondition:
        return AcceptanceCondition(self, other, Operator.AND)

    def __or__(
        self, other: t.Union[AcceptanceCondition, ParameterKind]
    ) -> AcceptanceCondition:
        return AcceptanceCondition(self, other, Operator.OR)

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

    def isin(self, other: t.Union[AcceptanceCondition, ParameterKind]) -> bool:
        return is_accepted(self, other)


# Aliases
ParameterCondition = t.Union[AcceptanceCondition, ParameterKind]

DATASET = ParameterKind.DATASET
SCALAR = ParameterKind.SCALAR
STATIC = ParameterKind.STATIC
PUP = ParameterKind.PUP
PUP_DATASET = ParameterKind.DATASET & ParameterKind.PUP
DATASPEC = ParameterKind.SCALAR | ParameterKind.DATASET
TRANSFORM = ParameterKind.TRANSFORM
