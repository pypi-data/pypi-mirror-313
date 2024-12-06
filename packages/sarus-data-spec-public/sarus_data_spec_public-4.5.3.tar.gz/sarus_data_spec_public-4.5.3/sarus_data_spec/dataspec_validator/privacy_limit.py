from __future__ import annotations

import typing as t

import sarus_data_spec.typing as st


class DeltaEpsilonLimit:
    """A Privacy limit defined by explicitly listing the points.

    Note: that epsilon is decreasing as a function of delta.
    """

    def __init__(self, delta_epsilon_dict: t.Dict[float, float]):
        """The delta epsilon dict holds delta as keys and epsilon as values.
        {delta: epsilon}
        """
        assert min(delta_epsilon_dict.keys()) >= 0
        assert max(delta_epsilon_dict.keys()) <= 1
        assert min(delta_epsilon_dict.values()) >= 0
        self.delta_epsilon = delta_epsilon_dict.copy()

    def delta_epsilon_dict(self) -> t.Dict[float, float]:
        return self.delta_epsilon


if t.TYPE_CHECKING:
    _: st.PrivacyLimit = DeltaEpsilonLimit({0.0: 0.0})
