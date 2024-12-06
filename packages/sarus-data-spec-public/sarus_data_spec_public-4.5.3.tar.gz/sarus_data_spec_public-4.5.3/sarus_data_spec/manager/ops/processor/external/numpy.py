from typing import Any, List, Literal, Optional, Tuple, Union

from numpy.typing import ArrayLike, DTypeLike
import numpy as np

from sarus_data_spec.dataspec_validator.parameter_kind import DATASPEC, STATIC
from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusParameterArray,
    SarusSignature,
    SarusSignatureValue,
)

from .external_op import ExternalOpImplementation

Casting = Literal["no", "equiv", "safe", "same_kind", "unsafe"]
Order = Literal["K", "A", "C", "F"]


# ------ CONSTRUCTORS ------
class np_array(ExternalOpImplementation):
    _transform_id = "numpy.NP_ARRAY"
    _signature = SarusSignature(
        SarusParameter(
            name="object",
            annotation=ArrayLike,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[DTypeLike],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="order",
            annotation=Order,
            default="K",
        ),
        SarusParameter(
            name="subok",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="ndmin",
            annotation=int,
            default=0,
        ),
        SarusParameter(
            name="like",
            annotation=Optional[ArrayLike],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        if kwargs["like"] is None:
            del kwargs["like"]
        return np.array(**kwargs)


# ------ FUNCTIONS ------
class np_ceil(ExternalOpImplementation):
    _transform_id = "numpy.NP_CEIL"
    _signature = SarusSignature(
        SarusParameter(
            name="x",
            annotation=ArrayLike,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="out",
            annotation=Optional[ArrayLike],
            default=None,
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="where",
            annotation=Optional[Union[bool, ArrayLike]],
            default=True,
        ),
        SarusParameter(
            name="casting",
            annotation=Casting,
            default="same_kind",
        ),
        SarusParameter(
            name="order",
            annotation=Order,
            default="K",
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[DTypeLike],
            default=None,
        ),
        SarusParameter(
            name="subok",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        x, kwargs = signature.collect_kwargs_method()
        return np.ceil(x, **kwargs)


class np_floor(ExternalOpImplementation):
    _transform_id = "numpy.NP_FLOOR"
    _signature = SarusSignature(
        SarusParameter(
            name="x",
            annotation=ArrayLike,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="out",
            annotation=Optional[ArrayLike],
            default=None,
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="where",
            annotation=Optional[Union[bool, ArrayLike]],
            default=True,
        ),
        SarusParameter(
            name="casting",
            annotation=Casting,
            default="same_kind",
        ),
        SarusParameter(
            name="order",
            annotation=Order,
            default="K",
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[DTypeLike],
            default=None,
        ),
        SarusParameter(
            name="subok",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        x, kwargs = signature.collect_kwargs_method()
        return np.floor(x, **kwargs)


class np_mean(ExternalOpImplementation):
    _transform_id = "numpy.NP_MEAN"
    _signature = SarusSignature(
        SarusParameter(
            name="a",
            annotation=ArrayLike,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="axis",
            annotation=Optional[Union[int, Tuple[int]]],
            default=None,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[DTypeLike],
            default=None,
        ),
        SarusParameter(
            name="out",
            annotation=Optional[ArrayLike],
            default=None,
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="keepdims",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="where",
            annotation=Optional[Union[bool, ArrayLike]],
            default=np._NoValue,  # type: ignore
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return np.mean(**kwargs)


class np_std(ExternalOpImplementation):
    _transform_id = "numpy.NP_STD"
    _signature = SarusSignature(
        SarusParameter(
            name="a",
            annotation=ArrayLike,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="axis",
            annotation=Optional[Union[int, Tuple[int]]],
            default=None,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[DTypeLike],
            default=None,
        ),
        SarusParameter(
            name="out",
            annotation=Optional[ArrayLike],
            default=None,
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="ddof",
            annotation=int,
            default=0,
        ),
        SarusParameter(
            name="keepdims",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="where",
            annotation=Optional[Union[bool, ArrayLike]],
            default=True,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return np.std(**kwargs)


class np_rand(ExternalOpImplementation):
    _transform_id = "numpy.NP_RAND"
    _signature = SarusSignature(
        SarusParameterArray(
            name="size",
            annotation=Optional[Union[int, List[int]]],
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        sizes = signature.collect_args()
        return np.random.random_sample(sizes)


class np_ravel_constructor(ExternalOpImplementation):
    _transform_id = "numpy.NP_RAVEL"
    _signature = SarusSignature(
        SarusParameter(
            name="a",
            annotation=ArrayLike,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="order",
            annotation=Order,
            default="C",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return np.ravel(**kwargs)


class np_reshape(ExternalOpImplementation):
    _transform_id = "numpy.NP_RESHAPE"
    _signature = SarusSignature(
        SarusParameter(
            name="a",
            annotation=ArrayLike,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="newshape",
            annotation=Optional[Union[int, Tuple[int]]],
        ),
        SarusParameter(
            name="order",
            annotation=Order,
            default="C",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return np.reshape(**kwargs)


# ------ METHODS ------
class np_astype(ExternalOpImplementation):
    _transform_id = "numpy.NP_ASTYPE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=np.ndarray,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="dtype",
            annotation=DTypeLike,
        ),
        SarusParameter(
            name="order",
            annotation=Order,
            default="K",
        ),
        SarusParameter(
            name="casting",
            annotation=Casting,
            default="unsafe",
        ),
        SarusParameter(
            name="subok",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=True,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.astype(**kwargs)


class np_ravel_method(ExternalOpImplementation):
    _transform_id = "numpy.NP_RAVEL_METHOD"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=np.ndarray,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="order",
            annotation=Order,
            default="C",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.ravel(**kwargs)


class np_reshape_method(ExternalOpImplementation):
    _transform_id = "numpy.NP_RESHAPE_METHOD"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=np.ndarray,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="newshape",
            annotation=Optional[Union[int, Tuple[int]]],
        ),
        SarusParameter(
            name="order",
            annotation=Order,
            default="C",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        newshape = kwargs["newshape"]
        order = kwargs["order"]
        return this.reshape(newshape, order=order)
