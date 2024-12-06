import typing as t

import pandas as pd

from sarus_data_spec.manager.ops.processor.standard.standard_op import (  # noqa: E501
    StandardScalarImplementation,
    StandardScalarStaticChecker,
)
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st


class ErrorEstimationStaticChecker(StandardScalarStaticChecker): ...


class ErrorEstimation(StandardScalarImplementation):
    """Computes the budget via standard rule
    depending on the number of columns of the
    parent dataspec"""

    async def value(self) -> t.Any:
        dataspecs = self.parents()

        if dataspecs[0].prototype() == sp.Scalar:
            true_value = await t.cast(st.Scalar, dataspecs[0]).async_value()
            dp_values = []
            for dataspec in dataspecs[1:]:
                dp_value = await t.cast(st.Scalar, dataspec).async_value()
                dp_values.append(abs(dp_value - true_value))

            return max(dp_values)
        else:
            true_value = t.cast(
                pd.Series,
                await dataspecs[0]
                .manager()
                .async_to(t.cast(st.Dataset, dataspecs[0]), pd.Series),
            )

            dp_values = []
            for dataspec in dataspecs[1:]:
                dp_value = t.cast(
                    pd.Series,
                    await dataspec.manager().async_to(
                        t.cast(st.Dataset, dataspec), pd.Series
                    ),
                )
                dp_values.append((dp_value - true_value).abs())
            results = pd.concat(dp_values, axis=1)
            return results.max(axis=1)
