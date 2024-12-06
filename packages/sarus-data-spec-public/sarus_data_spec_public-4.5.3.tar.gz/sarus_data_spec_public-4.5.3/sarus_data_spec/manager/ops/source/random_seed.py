import typing as t

from sarus_data_spec.manager.ops.base import ScalarImplementation


class RandomSeed(ScalarImplementation):
    async def value(self) -> t.Any:
        assert self.scalar.is_random_seed()
        return self.scalar.protobuf().spec.random_seed.value
