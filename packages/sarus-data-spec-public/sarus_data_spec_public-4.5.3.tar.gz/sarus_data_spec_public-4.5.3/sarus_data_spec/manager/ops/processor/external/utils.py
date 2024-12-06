import typing as t

from sarus_data_spec.json_serialisation import SarusJSONDecoder
import sarus_data_spec.typing as st


def static_arguments(
    transform: st.Transform,
) -> t.Tuple[
    t.Dict[int, t.Any],
    t.Dict[str, t.Any],
    t.List[int],
    t.Dict[t.Union[str, int], str],
]:
    """Return the external arguments serialized in the protobuf."""
    assert transform and transform.is_external()

    transform_spec = transform.protobuf().spec
    external_args = SarusJSONDecoder.decode_bytes(
        transform_spec.external.named_arguments
    )
    py_args = external_args["py_args"]
    py_kwargs = external_args["py_kwargs"]
    ds_args_pos = external_args["ds_args_pos"]
    ds_types = external_args["ds_types"]
    return py_args, py_kwargs, ds_args_pos, ds_types


def static_and_dynamic_arguments(
    transform: st.Transform, *ds_args: st.DataSpec, **ds_kwargs: st.DataSpec
) -> t.Tuple[t.List[t.Any], t.Dict[str, t.Any]]:
    """Return all the external arguments.

    This returns static arguments interleaved with Dataspecs.
    """
    py_args, py_kwargs, ds_args_pos, _ = static_arguments(transform)
    pos_values = {pos: val for pos, val in zip(ds_args_pos, ds_args)}
    kwargs = {**py_kwargs, **ds_kwargs}
    pos_args = {**pos_values, **py_args}
    args = [pos_args[i] for i in range(len(pos_args))]

    return args, kwargs
