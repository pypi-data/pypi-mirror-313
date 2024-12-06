import typing as t

from sarus_data_spec.manager.ops.base import ScalarImplementation


class PrivacyParams(ScalarImplementation):
    async def value(self) -> t.Any:
        assert self.scalar.is_privacy_params()
        points = self.scalar.protobuf().spec.privacy_params.points
        if len(points) != 1:
            raise NotImplementedError(
                "The PrivacyParams contains more than 1 point in the privacy "
                "profile."
            )
        return list(points)
