from __future__ import annotations

from enum import Enum, auto
import logging
import time
import typing as t

import pyarrow as pa

from sarus_data_spec.arrow.admin_utils import (
    async_admin_data,
    validate_privacy_unit,
)
from sarus_data_spec.dataspec_validator.parameter_kind import (
    DATASET,
    DATASPEC,
    PUP_DATASET,
    SCALAR,
    STATIC,
    TRANSFORM,
    ParameterCondition,
    is_accepted,
)
from sarus_data_spec.manager.ops.processor.external.utils import (
    static_arguments,
)
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st

logger = logging.getLogger(__name__)


class DefautValue(Enum):
    NO_DEFAULT = auto()


class SarusParameter:
    def __init__(
        self,
        name: str,
        annotation: t.Any,
        default: t.Any = DefautValue.NO_DEFAULT,
        condition: ParameterCondition = STATIC | DATASPEC,
        predicate: t.Callable[[t.Any], bool] = lambda _: True,
    ):
        self.name = name
        self.condition = condition
        self.annotation = annotation
        self.default = default
        self.predicate = predicate


class SarusParameterArray(SarusParameter):
    """Class representing a variable number of positional arguments.

    This is used to represent `*args` in signatures.

    If used, it must be the first argument to a signature. All positional
    arguments are captured by it.
    """

    def __init__(
        self,
        name: str,
        annotation: t.Any,
        condition: ParameterCondition = STATIC | DATASPEC,
        predicate: t.Callable[[t.Any], bool] = lambda _: True,
    ):
        super().__init__(
            name=name,
            annotation=annotation,
            default=DefautValue.NO_DEFAULT,
            condition=condition,
            predicate=predicate,
        )


class SarusParameterMapping(SarusParameter):
    """Class representing a variable number of named arguments.

    This is used to represent `**kwargs` in signatures.

    If used it must be the last argument to a signature. All remaining keyword
    arguments are captured by it.
    """

    def __init__(
        self,
        name: str,
        annotation: t.Any,
        condition: ParameterCondition = STATIC | DATASPEC,
        predicate: t.Callable[[t.Any], bool] = lambda _: True,
    ):
        super().__init__(
            name=name,
            annotation=annotation,
            default=DefautValue.NO_DEFAULT,
            condition=condition,
            predicate=predicate,
        )


class SarusSignature:
    """A Signature is a list of Parameters."""

    def __init__(self, *parameters: SarusParameter, name: str = ""):
        self._parameters = list(parameters)
        self._parameter_map = {param.name: param for param in parameters}
        self._name = name

    def parameters(self) -> t.List[SarusParameter]:
        return self._parameters

    def __getitem__(self, name: str) -> SarusParameter:
        return self._parameter_map[name]

    def __contains__(self, name: str) -> bool:
        return name in self._parameter_map

    def name(self) -> str:
        return self._name

    def _bind_external(
        self,
        transform: st.Transform,
        *ds_args: t.Union[st.DataSpec, st.Transform],
        **ds_kwargs: t.Union[st.DataSpec, st.Transform],
    ) -> SarusBoundSignature:
        # Deserialize arguments
        py_args, py_kwargs, ds_args_pos, ds_types = static_arguments(transform)
        if len(ds_types) != len(ds_args) + len(ds_kwargs):
            raise ValueError(
                "Incorrect number of types specified in the external protobuf."
            )
        pos_values = {pos: val for pos, val in zip(ds_args_pos, ds_args)}
        pos_args = {**pos_values, **py_args}

        kwargs = {**py_kwargs, **ds_kwargs}
        args = [pos_args[i] for i in range(len(pos_args))]
        args_types = [ds_types.get(pos) for pos in range(len(args))]
        kwargs_types = {name: ds_types.get(name) for name in kwargs.keys()}

        # Pair arguments serialized in protobuf with the signature's
        # parameters
        if len(self.parameters()) > 0:
            has_param_array = isinstance(
                self.parameters()[0], SarusParameterArray
            )
            has_param_mapping = isinstance(
                self.parameters()[-1], SarusParameterMapping
            )
        else:
            has_param_array = False
            has_param_mapping = False

        if has_param_array:
            # All positional arguments are captured by the array
            param_array = self.parameters()[0]
            bound_args = [
                SarusBoundArgument(
                    SarusParameter(
                        name=f"{param_array.name}_{i}",
                        annotation=param_array.annotation,
                        default=param_array.default,
                        condition=param_array.condition,
                        predicate=param_array.predicate,
                    ),
                    arg,
                    args_types[i],
                    positional_only=True,
                )
                for i, arg in enumerate(args)
            ]
        else:
            bound_args = [
                SarusBoundArgument(self.parameters()[i], arg, args_types[i])
                for i, arg in enumerate(args)
            ]

        if not has_param_mapping:
            bound_kwargs = [
                SarusBoundArgument(
                    param, kwargs[param.name], kwargs_types[param.name]
                )
                for param in self.parameters()
                if param.name in kwargs
            ]
        else:
            # Capture all kwargs described in the signature
            bound_kwargs = [
                SarusBoundArgument(
                    param, kwargs[param.name], kwargs_types[param.name]
                )
                for param in self.parameters()[:-1]
                if param.name in kwargs
            ]
            # Remaining kwargs are bound to the parameter mapping
            param_mapping = self.parameters()[-1]
            already_bound_kwargs = [arg.name() for arg in bound_kwargs]
            bound_kwargs += [
                SarusBoundArgument(
                    SarusParameter(
                        name=name,
                        annotation=param_mapping.annotation,
                        condition=param_mapping.condition,
                        predicate=param_mapping.predicate,
                    ),
                    value,
                    kwargs_types[name],
                )
                for name, value in kwargs.items()
                if name not in already_bound_kwargs
            ]

        # Check that all arguments have a unique name
        bound_arguments = bound_args + bound_kwargs
        bound_args_names = [bound_arg.name() for bound_arg in bound_arguments]
        if len(set(bound_args_names)) != len(bound_args_names):
            raise ValueError(
                "An argument was specified more than "
                "once in an external transform."
            )

        # Fill in default arguments
        default_bound_args = [
            SarusBoundArgument(param, param.default)
            for param in self.parameters()
            if param.name not in bound_args_names
            and param.default != DefautValue.NO_DEFAULT
        ]
        bound_arguments += default_bound_args

        # Check number of arguments
        if (
            not has_param_array
            and not has_param_mapping
            and len(bound_arguments) != len(self.parameters())
        ):
            raise ValueError(
                "Invalid number of parameters serialized in external"
                f" transform. Expected {len(self.parameters())}, "
                f"got {len(bound_arguments)}."
            )

        # reorder arguments
        if not has_param_array and not has_param_mapping:
            arg_map = {arg.name(): arg for arg in bound_arguments}
            bound_arguments = [
                arg_map[param.name] for param in self.parameters()
            ]

        return SarusBoundSignature(bound_arguments, name=self.name())

    def bind_dataspec(self, dataspec: st.DataSpec) -> SarusBoundSignature:
        if not dataspec.is_transformed():
            raise ValueError("Cannot bind a non transformed dataspec.")

        transform = dataspec.transform()
        ds_args, ds_kwargs = dataspec.parents()
        return self.bind(transform, *ds_args, **ds_kwargs)

    def bind_composed(self, transform: st.Transform) -> SarusBoundSignature:
        if not transform.is_composed():
            raise ValueError("Cannot bind a non composed transform.")

        transform_to_apply = transform.transform_to_apply()
        tr_args, tr_kwargs = transform.composed_parents()
        return self.bind(transform_to_apply, *tr_args, **tr_kwargs)

    def bind(
        self,
        transform: st.Transform,
        *ds_args: t.Union[st.DataSpec, st.Transform],
        **ds_kwargs: t.Union[st.DataSpec, st.Transform],
    ) -> SarusBoundSignature:
        """Deserialize protobuf, get parent dataspecs
        Create bound arguments from the static or dynamic arguments and from
        the parameters Raise an error if there is a mismatch.
        """
        if not transform.is_external():
            raise NotImplementedError(
                "Binding standard signature not implemented yet."
            )
        else:
            return self._bind_external(transform, *ds_args, **ds_kwargs)

    def make_dp(self) -> SarusSignature:
        """Creates a DP Signature from the current one by adding extra
        parameters."""
        return SarusSignature(
            *self._parameters,
            SarusParameter(
                name="budget",
                annotation=sp.Scalar.PrivacyParameters,
                condition=SCALAR,
            ),
            SarusParameter(
                name="seed",
                annotation=int,
                condition=SCALAR,
            ),
        )


class SarusBoundArgument:
    """A BoundArgument is a triplet (parameter, value, kind).

    Args:
        parameter (SarusParameter):
            The Sarus parameter describing what is accepted.
        value (t.Union[st.DataSpec, st.Transform, t.Any]):
            The value as defined by the computation graph.
        kind (t.Optional[str]):
            The Python type a Dataset should be casted to.
        positional_only (bool):
            The argument is positional only and the name should be ignored.
    """

    dataset_types = {
        str(_type): t.cast(t.Type, _type)
        for _type in t.get_args(st.DatasetCastable)
    }

    def __init__(
        self,
        parameter: SarusParameter,
        value: t.Union[st.DataSpec, st.Transform, t.Any],
        kind: t.Optional[str] = None,
        positional_only: bool = False,
    ):
        self.parameter = parameter
        self._value = value
        self.kind = kind
        self.positional_only = positional_only

    def name(self) -> str:
        return self.parameter.name

    def __repr__(self) -> str:
        return f"<BoundArgument {self.name()} {repr(self.static_value())}>"

    def static_value(self) -> t.Any:
        return self._value

    def python_type(self) -> t.Optional[str]:
        return self.kind

    def parameter_kind(self) -> ParameterCondition:
        """Return the value type associated with the Parameter."""
        if isinstance(self.static_value(), st.DataSpec):
            dataspec = t.cast(st.DataSpec, self.static_value())
            if dataspec.prototype() == sp.Dataset:
                dataset = t.cast(st.Dataset, dataspec)
                if dataset.is_pup():
                    return PUP_DATASET
                else:
                    return DATASET
            else:
                return SCALAR
        elif isinstance(self.static_value(), st.Transform):
            return TRANSFORM
        else:
            return STATIC

    def pup_token(self) -> t.Optional[str]:
        if isinstance(self.static_value(), st.DataSpec):
            dataspec = t.cast(st.DataSpec, self.static_value())
            return dataspec.pup_token()
        else:
            return None

    def rewritten_pup_token(self) -> t.Optional[str]:
        if isinstance(self.static_value(), st.DataSpec):
            dataspec = t.cast(st.DataSpec, self.static_value())
            return dataspec.rewritten_pup_token()
        else:
            return None

    def is_pup(self) -> bool:
        return self.pup_token() is not None

    def is_pup_for_rewriting(self) -> bool:
        return self.rewritten_pup_token() is not None

    def is_public(self) -> bool:
        if isinstance(self.static_value(), st.DataSpec):
            dataspec = t.cast(st.DataSpec, self.static_value())
            return dataspec.is_public()
        else:
            return True

    def is_published(self) -> bool:
        if isinstance(self.static_value(), st.DataSpec):
            dataspec = t.cast(st.DataSpec, self.static_value())
            return dataspec.is_published()
        else:
            return True

    def is_publishable(self) -> bool:
        if isinstance(self.static_value(), st.DataSpec):
            dataspec = t.cast(st.DataSpec, self.static_value())
            return dataspec.is_publishable()
        else:
            return True

    def static_validation(self) -> None:
        """Check that the argument is compatible with the parameter"""
        parameter_kind = self.parameter_kind()
        if not is_accepted(self.parameter.condition, parameter_kind):
            raise TypeError(
                f"Expected parameter {self.name()} to be "
                f"{str(self.parameter.condition)}, got {str(parameter_kind)}"
            )

        if DATASET.isin(parameter_kind):
            if self.kind is None:
                raise ValueError(
                    f"Parameter {self.name()} is a Dataset, but no type "
                    "to cast to is defined."
                )

            if self.kind not in self.dataset_types:
                raise ValueError(
                    f"Parameter {self.name()} is a Dataset "
                    f"and cannot be casted to type {self.kind}. "
                    f"Expected one of {list(self.dataset_types.keys())}"
                )

        if STATIC.isin(parameter_kind):
            value = self.static_value()
            if not self.parameter.predicate(value):
                raise ValueError(
                    f"Got invalid value `{value}` for "
                    f"parameter `{self.name()}`"
                )

    async def dynamic_validation(self) -> None: ...

    async def collect(self) -> t.Any:
        """Evaluate the argument before calling the data function."""
        if isinstance(self.static_value(), st.DataSpec):
            ds = t.cast(st.DataSpec, self.static_value())
            if ds.prototype() == sp.Dataset:
                dataset = t.cast(st.Dataset, self.static_value())
                if self.kind is None:
                    raise ValueError(
                        f"Parameter {self.name()} is a Dataset, but no type "
                        "to cast to is defined."
                    )
                return await dataset.async_to(self.dataset_types[self.kind])
            else:
                scalar = t.cast(st.Scalar, ds)
                return await scalar.async_value()
        elif isinstance(self.static_value(), st.Transform):
            transform = t.cast(st.Transform, self.static_value())
            return transform.composed_callable()
        else:
            return self.static_value()

    def callable(self) -> t.Callable[..., SarusArgumentValue]:
        """Returns a callable that will compute the argument's value given
        variables' values."""
        if isinstance(self.static_value(), st.Transform):
            transform = t.cast(st.Transform, self.static_value())
            if transform.is_variable():
                var_name = transform.protobuf().spec.variable.name
                var_pos = transform.protobuf().spec.variable.position

                def arg_callable(
                    *vars: t.Any, **kwvars: t.Any
                ) -> SarusArgumentValue:
                    if var_name in kwvars:
                        value = kwvars[var_name]
                    else:
                        value = vars[var_pos]
                    return SarusArgumentValue(
                        name=self.name(),
                        value=value,
                        positional_only=self.positional_only,
                    )

            else:
                assert transform.is_composed()
                previous_callable = transform.composed_callable()

                def arg_callable(
                    *vars: t.Any, **kwvars: t.Any
                ) -> SarusArgumentValue:
                    value = previous_callable(*vars, **kwvars)
                    return SarusArgumentValue(
                        name=self.name(),
                        value=value,
                        positional_only=self.positional_only,
                    )

        elif isinstance(self.static_value(), st.DataSpec):
            raise ValueError("Cannot collect a DataSpec in a lambda function.")
        else:

            def arg_callable(
                *vars: t.Any, **kwvars: t.Any
            ) -> SarusArgumentValue:
                value = self.static_value()
                return SarusArgumentValue(
                    name=self.name(),
                    value=value,
                    positional_only=self.positional_only,
                )

        return arg_callable

    async def admin_data(self) -> t.Optional[pa.Table]:
        if not self.is_pup():
            return None

        dataset = t.cast(st.Dataset, self.static_value())
        admin_data = await async_admin_data(dataset)
        if admin_data is None:
            raise ValueError(
                f"The dataset {dataset.uuid()} was"
                " inferred PUP but has no admin data."
            )
        return admin_data


class SarusBoundSignature:
    """A BoundSignature is a list of BoundArguments."""

    def __init__(self, arguments: t.List[SarusBoundArgument], name: str):
        self.arguments = arguments
        self._argument_map = {arg.name(): arg for arg in self.arguments}
        self._name = name

    def name(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return (
            f"{self.name()}"
            f"({', '.join([arg.name() for arg in self.arguments])})"
        )

    def is_dp(self) -> bool:
        return "budget" in self._argument_map and "seed" in self._argument_map

    def __getitem__(self, name: str) -> SarusBoundArgument:
        return self._argument_map[name]

    def __contains__(self, name: str) -> bool:
        return name in self._argument_map

    def static_validation(self) -> None:
        """Check that the arguments have the correct dataspec type."""
        start = time.perf_counter()
        for arg in self.arguments:
            arg.static_validation()
        end = time.perf_counter()
        logger.info(f"STATIC VALIDATION {self} ({end-start:.2f}s)")

    async def dynamic_validation(self) -> None:
        """Compare the values with the annotations.

        TODO: Not used yet. Annotations needs to be curated to
        remove ForwardRefs.
        """
        for arg in self.arguments:
            await arg.dynamic_validation()

    def static_kwargs(self) -> t.Dict[str, t.Any]:
        """Return non evaluated arguments."""
        assert not any([arg.positional_only for arg in self.arguments])
        return {
            arg.parameter.name: arg.static_value() for arg in self.arguments
        }

    def static_args(self) -> t.List[t.Any]:
        """Return non evaluated arguments."""
        return [arg.static_value() for arg in self.arguments]

    async def collect_kwargs(self) -> t.Dict[str, t.Any]:
        """Evaluate arguments for calling the data function."""
        assert not any([arg.positional_only for arg in self.arguments])
        return {
            arg.parameter.name: await arg.collect() for arg in self.arguments
        }

    async def collect_args(self) -> t.List[t.Any]:
        """Evaluate arguments for calling the data function."""
        return [await arg.collect() for arg in self.arguments]

    async def collect_kwargs_method(
        self,
    ) -> t.Tuple[t.Any, t.Dict[str, t.Any]]:
        """Evaluate the arguments.

        Return a tuple (self, kwargs)
        """
        assert not any([arg.positional_only for arg in self.arguments])
        first_value = await self.arguments[0].collect()
        other_values = {
            arg.parameter.name: await arg.collect()
            for arg in self.arguments[1:]
        }
        return first_value, other_values

    async def collect_method(
        self,
    ) -> t.Tuple[t.Any, t.List[t.Any], t.Dict[str, t.Any]]:
        """Evaluate the arguments.

        Return a tuple (self, args, kwargs).
        """
        first_value = await self.arguments[0].collect()
        positional_values = [
            await arg.collect()
            for arg in self.arguments[1:]
            if arg.positional_only
        ]
        keyword_values = {
            arg.name(): await arg.collect()
            for arg in self.arguments[1:]
            if not arg.positional_only
        }

        return first_value, positional_values, keyword_values

    async def collect(
        self,
    ) -> t.Tuple[t.List[t.Any], t.Dict[str, t.Any]]:
        """Evaluate the arguments.

        Return a tuple (args, kwargs).
        """
        positional_values = [
            await arg.collect()
            for arg in self.arguments
            if arg.positional_only
        ]
        keyword_values = {
            arg.name(): await arg.collect()
            for arg in self.arguments
            if not arg.positional_only
        }

        return positional_values, keyword_values

    def pup_token(self) -> t.Optional[str]:
        """Compute the PUP token of the inputs.

        A PUP token exists if:
          - all input dataspecs are PUP or PUBLIC
          - there must be at least one input PUP dataspec
          - if there are more that one input PUP dataspecs, all PUP inputs must
            have the same token
        """

        if not all(
            [
                arg.is_public() or arg.is_pup() or arg.is_published()
                for arg in self.arguments
            ]
        ):
            return None

        pup_args = [arg for arg in self.arguments if arg.is_pup()]
        if len(pup_args) == 0:
            return None

        tokens = [arg.pup_token() for arg in pup_args]
        unique_tokens = set(tokens)
        if len(unique_tokens) != 1:
            return None
        else:
            return unique_tokens.pop()

    def rewritten_pup_token(self) -> t.Optional[str]:
        if not all(
            [
                arg.is_public()
                or arg.is_pup_for_rewriting()
                or arg.is_publishable()
                for arg in self.arguments
            ]
        ):
            return None

        pup_args = [
            arg for arg in self.arguments if arg.is_pup_for_rewriting()
        ]
        if len(pup_args) == 0:
            return None

        tokens = [arg.rewritten_pup_token() for arg in pup_args]
        unique_tokens = set(tokens)
        if len(unique_tokens) != 1:
            return None
        else:
            return unique_tokens.pop()

    async def admin_data(self) -> pa.Table:
        """Return the admin data of the inputs."""
        admin_data = [
            await arg.admin_data() for arg in self.arguments if arg.is_pup()
        ]
        if len(admin_data) == 0:
            raise ValueError(
                "The list of input admin data is empty "
                f"among arguments {self.arguments}"
            )

        return validate_privacy_unit(admin_data)

    def callable(
        self,
    ) -> t.Callable[..., SarusSignatureValue]:
        """Returns a callable that will compute the signature's value given
        variables' values."""
        # Build callables here
        arg_callables = [arg.callable() for arg in self.arguments]

        def signature_callable(
            *vars: t.Any, **kwvars: t.Any
        ) -> SarusSignatureValue:
            # Call already built callables here
            return SarusSignatureValue(
                arguments=[
                    arg_callable(*vars, **kwvars)
                    for arg_callable in arg_callables
                ],
                name=self.name(),
                bound_signature=self,
            )

        return signature_callable

    async def collect_signature_value(self) -> SarusSignatureValue:
        """Collect the arguments' values and return them in a
        signature form."""
        return SarusSignatureValue(
            arguments=[
                SarusArgumentValue(
                    name=arg.name(),
                    value=await arg.collect(),
                    positional_only=arg.positional_only,
                )
                for arg in self.arguments
            ],
            name=self.name(),
            bound_signature=self,
        )


class SarusArgumentValue:
    """Represents an evaluated argument."""

    def __init__(
        self,
        name: str,
        value: t.Any,
        positional_only: bool = False,
    ):
        self.name = name
        self.value = value
        self.positional_only = positional_only

    def python_type(self) -> t.Optional[str]:
        return str(type(self.value))


class SarusSignatureValue:
    """Similar to a bound signature but only holds arguments' values.
    As a result it only has sync methods since async computations are not
    called."""

    def __init__(
        self,
        arguments: t.List[SarusArgumentValue],
        name: str,
        bound_signature: SarusBoundSignature,
    ):
        self.arguments = arguments
        self._argument_map = {arg.name: arg for arg in self.arguments}
        self._name = name
        self.bound_signature = bound_signature

    def __getitem__(self, name: str) -> SarusArgumentValue:
        return self._argument_map[name]

    def __contains__(self, name: str) -> bool:
        return name in self._argument_map

    def collect_kwargs(self) -> t.Dict[str, t.Any]:
        """Evaluate arguments for calling the data function."""
        assert not any([arg.positional_only for arg in self.arguments])
        return {arg.name: arg.value for arg in self.arguments}

    def collect_args(self) -> t.List[t.Any]:
        """Evaluate arguments for calling the data function."""
        return [arg.value for arg in self.arguments]

    def collect_kwargs_method(
        self,
    ) -> t.Tuple[t.Any, t.Dict[str, t.Any]]:
        assert not any([arg.positional_only for arg in self.arguments])
        first_value = self.arguments[0].value
        other_values = {arg.name: arg.value for arg in self.arguments[1:]}
        return first_value, other_values

    def collect_method(
        self,
    ) -> t.Tuple[t.Any, t.List[t.Any], t.Dict[str, t.Any]]:
        first_value = self.arguments[0].value
        positional_values = [
            arg.value for arg in self.arguments[1:] if arg.positional_only
        ]
        keyword_values = {
            arg.name: arg.value
            for arg in self.arguments[1:]
            if not arg.positional_only
        }

        return first_value, positional_values, keyword_values

    def collect(
        self,
    ) -> t.Tuple[t.List[t.Any], t.Dict[str, t.Any]]:
        positional_values = [
            arg.value for arg in self.arguments if arg.positional_only
        ]
        keyword_values = {
            arg.name: arg.value
            for arg in self.arguments
            if not arg.positional_only
        }

        return positional_values, keyword_values


def extended_is_instance(obj: t.Any, kind: t.Type) -> bool:
    """Extended version of isinstance that also checks composite types."""
    if t.get_origin(kind) is None:
        if isinstance(kind, t.ForwardRef):
            return False
        else:
            return isinstance(obj, kind)
    elif t.get_origin(kind) == t.Union:
        return any(
            extended_is_instance(obj, subkind) for subkind in t.get_args(kind)
        )
    elif t.get_origin(kind) == t.Optional:
        (subkind,) = t.get_args(kind)
        return obj is None or extended_is_instance(obj, subkind)
    elif t.get_origin(kind) in [t.List, list]:
        return isinstance(obj, list)
    else:
        raise NotImplementedError(
            f"Dynamic type checking not implemented for {kind}."
        )
