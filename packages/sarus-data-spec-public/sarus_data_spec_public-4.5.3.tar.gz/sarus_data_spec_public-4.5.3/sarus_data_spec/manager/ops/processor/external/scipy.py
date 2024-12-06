from typing import Any, List, Literal, Optional, Sequence, Tuple, Union
import typing as t

import numpy as np
import pandas._typing as pdt

from sarus_data_spec.dataspec_validator.parameter_kind import DATASPEC, STATIC
from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from .external_op import ExternalOpImplementation

try:
    from scipy.sparse import (
        bsr_array,
        bsr_matrix,
        coo_array,
        coo_matrix,
        csc_array,
        csc_matrix,
        csr_array,
        csr_matrix,
        dia_array,
        dia_matrix,
        dok_array,
        dok_matrix,
        lil_array,
        lil_matrix,
        spmatrix,
    )
except ModuleNotFoundError:
    bsr_matrix = Any
    coo_matrix = Any
    csc_matrix = Any
    csr_matrix = Any
    dok_matrix = Any
    lil_matrix = Any
    bsr_array = Any
    coo_matrix = Any
    coo_array = Any
    csc_array = Any
    csr_array = Any
    dia_matrix = Any
    dia_array = Any
    dok_array = Any
    lil_array = Any
    spmatrix = Any

Casting = Literal["no", "equiv", "safe", "same_kind", "unsafe"]
Order = Literal["K", "A", "C", "F"]


# ------ CONSTRUCTORS ------
class sp_bsr_matrix(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_BSR_MATRIX"
    _signature = SarusSignature(
        SarusParameter(
            name="arg1",
            annotation=Union[
                np.ndarray,
                bsr_matrix,
                Tuple[np.ndarray, Tuple[np.ndarray, np.ndarray]],
                Tuple[np.ndarray, np.ndarray, np.ndarray],
            ],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="shape",
            annotation=Optional[Tuple[int, int]],
            default=None,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[Union[np.dtype, str]],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="blocksize",
            annotation=Optional[Tuple[int, int]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> bsr_matrix:
        this, kwargs = signature.collect_kwargs_method()
        return bsr_matrix(this, **kwargs)


class sp_coo_matrix(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_COO_MATRIX"
    _signature = SarusSignature(
        SarusParameter(
            name="arg1",
            annotation=Union[
                np.ndarray,
                coo_matrix,
                Tuple[np.ndarray, Tuple[np.ndarray, np.ndarray]],
            ],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="shape",
            annotation=Optional[Tuple[int, int]],
            default=None,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[np.dtype],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=Optional[bool],
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return coo_matrix(this, **kwargs)


class sp_csc_matrix(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_CSC_MATRIX"
    _signature = SarusSignature(
        SarusParameter(
            name="arg1",
            annotation=Union[
                Tuple[pdt.ArrayLike, Tuple[pdt.ArrayLike, pdt.ArrayLike]],
                Tuple[pdt.ArrayLike, pdt.ArrayLike, pdt.ArrayLike],
                pdt.ArrayLike,
                Tuple[int, int],
            ],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="shape",
            annotation=Optional[Tuple[int, int]],
            default=None,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[type],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> csc_matrix:
        kwargs = signature.collect_kwargs()
        return csc_matrix(**kwargs)


class sp_csr_matrix(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_CSR_MATRIX"
    _signature = SarusSignature(
        SarusParameter(
            name="arg1",
            annotation=Union[
                Tuple[pdt.ArrayLike, Tuple[pdt.ArrayLike, pdt.ArrayLike]],
                Tuple[pdt.ArrayLike, pdt.ArrayLike, pdt.ArrayLike],
                pdt.ArrayLike,
                Tuple[int, int],
            ],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="shape",
            annotation=Optional[Tuple[int, int]],
            default=None,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[type],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> csr_matrix:
        kwargs = signature.collect_kwargs()
        return csr_matrix(**kwargs)


class sp_dia_matrix(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_DIA_MATRIX"
    _signature = SarusSignature(
        SarusParameter(
            name="arg1",
            annotation=Union[
                Tuple[np.ndarray, np.ndarray],
                Tuple[int, int],
                dia_matrix,
                np.ndarray,
            ],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="shape",
            annotation=Optional[Tuple[int, int]],
            default=None,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[Union[str, np.dtype]],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return dia_matrix(**kwargs)


class sp_dok_matrix(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_DOK_MATRIX"
    _signature = SarusSignature(
        SarusParameter(
            name="arg1",
            annotation=Union[np.ndarray, spmatrix],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="shape",
            annotation=Optional[Tuple[int, int]],
            default=None,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[np.dtype],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return dok_matrix(**kwargs)


class sp_lil_matrix(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_LIL_MATRIX"
    _signature = SarusSignature(
        SarusParameter(
            name="arg1",
            annotation=Union[np.ndarray, spmatrix],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="shape",
            annotation=Optional[Tuple[int, int]],
            default=None,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[np.dtype],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return lil_matrix(**kwargs)


class sp_bsr_array(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_BSR_ARRAY"
    _signature = SarusSignature(
        SarusParameter(
            name="arg1",
            annotation=Union[
                np.ndarray,
                spmatrix,
                Tuple[np.ndarray, Tuple[np.ndarray, np.ndarray]],
                Tuple[np.ndarray, np.ndarray, np.ndarray],
            ],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="shape",
            annotation=Optional[Tuple[int, int]],
            default=None,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[Union[str, np.dtype]],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="blocksize",
            annotation=Optional[Tuple[int, int]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> bsr_matrix:
        kwargs = signature.collect_kwargs()
        return bsr_array(**kwargs)


class sp_coo_array(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_COO_ARRAY"
    _signature = SarusSignature(
        SarusParameter(
            name="arg1",
            annotation=Union[
                np.ndarray,
                spmatrix,
                Tuple[np.ndarray, Tuple[np.ndarray, np.ndarray]],
            ],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="shape",
            annotation=Optional[Tuple[int, int]],
            default=None,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[Union[str, np.dtype]],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> coo_matrix:
        kwargs = signature.collect_kwargs()
        return coo_array(**kwargs)


class sp_csc_array(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_CSC_ARRAY"
    _signature = SarusSignature(
        SarusParameter(
            name="arg1",
            annotation=Union[
                np.ndarray,
                spmatrix,
                Tuple[Union[np.ndarray, List], Tuple[np.ndarray, np.ndarray]],
                Tuple[np.ndarray, np.ndarray, np.ndarray],
            ],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="shape",
            annotation=Optional[Tuple[int, int]],
            default=None,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[np.dtype],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return csc_array(**kwargs)


class sp_csr_array(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_CSR_ARRAY"
    _signature = SarusSignature(
        SarusParameter(
            name="arg1",
            annotation=Union[
                np.ndarray,
                spmatrix,
                Tuple[Union[np.ndarray, List], Tuple[np.ndarray, np.ndarray]],
                Tuple[np.ndarray, np.ndarray, np.ndarray],
            ],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="shape",
            annotation=Optional[Tuple[int, int]],
            default=None,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[np.dtype],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return csr_array(**kwargs)


class sp_dia_array(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_DIA_ARRAY"
    _signature = SarusSignature(
        SarusParameter(
            name="arg1",
            annotation=Union[
                np.ndarray,
                dia_matrix,
                Tuple[Union[np.ndarray, Sequence[int]], Tuple[int, int]],
            ],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="shape",
            annotation=Optional[Tuple[int, int]],
            default=None,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[np.dtype],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return dia_array(**kwargs)


class sp_dok_array(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_DOK_ARRAY"
    _signature = SarusSignature(
        SarusParameter(
            name="arg1",
            annotation=Union[np.ndarray, dok_matrix, Tuple[int, int]],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="shape",
            annotation=Optional[Tuple[int, int]],
            default=None,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[np.dtype],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return dok_array(**kwargs)


class sp_lil_array(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_LIL_ARRAY"
    _signature = SarusSignature(
        SarusParameter(
            name="arg1",
            annotation=Union[np.ndarray, lil_matrix, Tuple[int, int]],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="shape",
            annotation=Optional[Tuple[int, int]],
            default=None,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[np.dtype],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return lil_array(**kwargs)


# ------ Scipy sparse METHODS ------


class scipy_SCIPY_arcsin(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_ARCSIN"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        this = signature.collect_args()[0]
        return this.arcsin()


class scipy_SCIPY_asfptype(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_ASFPTYPE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        this = signature.collect_args()[0]
        return this.asfptype()


class scipy_SCIPY_ceil(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_CEIL"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        this = signature.collect_args()[0]
        return this.ceil()


class scipy_SCIPY_argmax(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_ARGMAX"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="axis",
            annotation=Any,
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Union[csr_matrix, int]:
        this, axis = signature.collect_args()
        return this.argmax(axis=axis)


class scipy_conj(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_CONJ"
    _signature = SarusSignature(
        SarusParameter(
            name="data",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=True,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        data, copy = signature.collect_args()
        return data.conj(copy=copy)


class scipy_conjugate(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_CONJUGATE"
    _signature = SarusSignature(
        SarusParameter(
            name="data",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=True,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        data, copy = signature.collect_args()
        return data.conjugate(copy=copy)


class scipy_count_nonzero(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_COUNT_NONZERO"
    _signature = SarusSignature(
        SarusParameter(
            name="data",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        )
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (data,) = signature.collect_args()
        return data.count_nonzero()


class scipy_deg2rad(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_DEG2RAD"
    _signature = SarusSignature(
        SarusParameter(
            name="data",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        )
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (data,) = signature.collect_args()
        return data.deg2rad()


class scipy_diagonal(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_DIAGONAL"
    _signature = SarusSignature(
        SarusParameter(
            name="data",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="k",
            annotation=int,
            default=0,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        data, k = signature.collect_args()
        return data.diagonal(k=k)


class scipy_dot(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_DOT"
    _signature = SarusSignature(
        SarusParameter(
            name="data",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="other",
            annotation=spmatrix,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        data, other = signature.collect_args()
        return data.dot(other)


class scipy_eliminate_zeros(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_ELIMINATE_ZEROS"
    _signature = SarusSignature(
        SarusParameter(
            name="data",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        )
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (data,) = signature.collect_args()
        data.eliminate_zeros()
        return data


class scipy_expm1(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_EXPM1"
    _signature = SarusSignature(
        SarusParameter(
            name="data",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        )
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        (data,) = signature.collect_args()
        return data.expm1()


class scipy_floor(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_FLOOR"
    _signature = SarusSignature(
        SarusParameter(
            name="data",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        )
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        (data,) = signature.collect_args()
        return data.floor()


class scipy_log1p(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_LOG1P"
    _signature = SarusSignature(
        SarusParameter(
            name="data",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        )
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        (data,) = signature.collect_args()
        return data.log1p()


class scipy_max(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_MAX"
    _signature = SarusSignature(
        SarusParameter(
            name="data",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="axis",
            annotation=Optional[Union[int, None]],
            default=None,
        ),
        SarusParameter(
            name="out",
            annotation=Optional[None],
            default=None,
        ),
    )

    def call(
        self, signature: SarusSignatureValue
    ) -> Union[spmatrix, int, float]:
        data, axis, out = signature.collect_args()
        return data.max(axis=axis, out=out)


class scipy_maximum(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_MAXIMUM"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="other",
            annotation=spmatrix,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, other) = signature.collect_args()
        return this.maximum(other)


class scipy_mean(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_MEAN"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="axis",
            annotation=Optional[Union[int, None]],
            default=None,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[Any],
            default=None,
        ),
        SarusParameter(
            name="out",
            annotation=Optional[np.matrix],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.mean(**kwargs)


class scipy_minimum(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_MINIMUM"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="other",
            annotation=spmatrix,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, other) = signature.collect_args()
        return this.minimum(other)


class scipy_reshape(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_RESHAPE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="shape",
            annotation=Tuple[int, int],
        ),
        SarusParameter(
            name="order",
            annotation=str,
            default="C",
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.reshape(**kwargs)


class scipy_multiply(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_MULTIPLY"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="other",
            annotation=spmatrix,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        (this, other) = signature.collect_args()
        return this.multiply(other)


class scipy_nanmax(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_NANMAX"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.nanmax()


class scipy_nanmin(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_NANMIN"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.nanmin()


class scipy_nonzero(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_NONZERO"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.nonzero()


class scipy_power(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_POWER"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(name="n", annotation=float),
        SarusParameter(
            name="dtype", annotation=t.Optional[type], default=None
        ),
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        this, n, dtype = signature.collect_args()
        return this.power(n, dtype=dtype)


class scipy_prune(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_PRUNE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.prune()


class scipy_rad2deg(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_RAD2DEG"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        (this,) = signature.collect_args()
        return this.rad2deg()


class scipy_resize(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_RESIZE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="shape",
            annotation=t.Tuple[int, int],
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        (this, shape) = signature.collect_args()
        return this.resize(*shape)


class scipy_rint(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_RINT"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        (this,) = signature.collect_args()
        return this.rint()


class scipy_setdiag(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_SETDIAG"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="values",
            annotation=t.Union[t.Sequence, float, int],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="k",
            annotation=int,
            default=0,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        (this, values, k) = signature.collect_args()
        return this.setdiag(values, k)


class scipy_sign(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_SIGN"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        (this,) = signature.collect_args()
        return this.sign()


class scipy_sin(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_SIN"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        (this,) = signature.collect_args()
        return this.sin()


class scipy_sinh(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_SINH"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        (this,) = signature.collect_args()
        return this.sinh()


class scipy_sort_indices(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_SORT_INDICES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        this.sort_indices()
        return this


class scipy_sorted_indices(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_SORTED_INDICES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        (this,) = signature.collect_args()
        return this.sorted_indices()


class scipy_sqrt(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_SQRT"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        (this,) = signature.collect_args()
        return this.sqrt()


class scipy_sum(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_SUM"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="axis",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[t.Any],
            default=None,
        ),
        SarusParameter(
            name="out",
            annotation=Optional[np.matrix],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.sum(**kwargs)


class scipy_sum_duplicates(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_SUM_DUPLICATES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        this.sum_duplicates()
        return this


class scipy_tan(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_TAN"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        (this,) = signature.collect_args()
        return this.tan()


class scipy_tanh(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_TANH"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> spmatrix:
        (this,) = signature.collect_args()
        return this.tanh()


class scipy_trace(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_TRACE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="offset",
            annotation=int,
            default=0,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, offset) = signature.collect_args()
        return this.trace(offset)


class scipy_transpose(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_TRANSPOSE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="axes",
            annotation=Optional[None],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.transpose(**kwargs)


class scipy_trunc(ExternalOpImplementation):
    _transform_id = "scipy.SCIPY_TRUNC"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=spmatrix,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.trunc()
