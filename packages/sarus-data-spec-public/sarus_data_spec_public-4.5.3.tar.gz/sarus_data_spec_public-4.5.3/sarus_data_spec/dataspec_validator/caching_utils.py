import typing
from functools import wraps
from sarus_data_spec.attribute import attach_properties
import sarus_data_spec.typing as st


def check_existence_in_attribute_or_cache_after(
    attribute_name: str,
) -> typing.Callable[
    [typing.Callable[[typing.Any, st.DataSpec], bool]],
    typing.Callable[[typing.Any, st.DataSpec], bool],
]:
    """This decorator is to be used  for methods of
    the dataspec validator that take as input the dataspec
    and return a boolean.
    It first checks if the attribute already exits, and returns it,
    otherwise it executes the method and then caches the result."""

    def cache_and_check(
        func: typing.Callable[[typing.Any, st.DataSpec], bool],
    ) -> typing.Callable[[typing.Any, st.DataSpec], bool]:
        @wraps(func)
        def wrapper_fn(
            validator: typing.Any,
            dataspec: st.DataSpec,
        ) -> bool:
            assert isinstance(dataspec, st.DataSpec)
            existing_attribute = dataspec.attribute(attribute_name)
            if existing_attribute is not None:
                return existing_attribute[attribute_name] == str(True)
            outcome = func(validator, dataspec)
            attach_properties(
                dataspec,
                name=attribute_name,
                properties={attribute_name: str(outcome)},
            )
            return outcome

        return wrapper_fn

    return cache_and_check
