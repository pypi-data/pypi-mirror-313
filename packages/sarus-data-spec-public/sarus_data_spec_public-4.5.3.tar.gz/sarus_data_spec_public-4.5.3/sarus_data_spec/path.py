from __future__ import annotations

from collections import defaultdict
import typing as t

from sarus_data_spec.base import Base
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st


class Path(Base[sp.Path]):
    def prototype(self) -> t.Type[sp.Path]:
        return sp.Path

    def label(self) -> str:
        return self._protobuf.label

    def sub_paths(self) -> t.List[st.Path]:
        return [Path(path) for path in self._protobuf.paths]

    def select(self, select_path: st.Path) -> t.List[st.Path]:
        assert select_path.label() == self.label()

        if len(select_path.sub_paths()) == 0:
            return self.sub_paths()

        final_sub_paths = []
        for sub_path in select_path.sub_paths():
            for available_sub_path in self.sub_paths():
                if available_sub_path.label() == sub_path.label():
                    final_sub_paths.extend(available_sub_path.select(sub_path))

        return final_sub_paths

    def is_empty(self) -> bool:
        assert not self.has_sub_paths()
        return self.label() == ""

    def has_sub_paths(self) -> bool:
        return len(self._protobuf.paths) > 0

    def to_strings_list(self) -> t.List[t.List[str]]:
        paths = []
        proto = self._protobuf
        if len(proto.paths) == 0:
            return [[proto.label]]
        for path in proto.paths:
            out = Path(path).to_strings_list()
            for el in out:
                el.insert(
                    0,
                    proto.label,
                )
            paths.extend(out)
        return paths

    def to_dict(self) -> t.Dict[str, str]:
        list_paths = self.to_strings_list()
        return {
            ".".join(path[1:-1]): path[-1] for path in list_paths
        }  # always start with DATA


def paths(path_list: t.List[t.List[str]]) -> t.List[Path]:
    out = defaultdict(list)
    for path in path_list:
        try:
            first_el = path.pop(0)
        except IndexError:
            return []
        else:
            out[first_el].append(path)
    return [
        Path(
            sp.Path(
                label=element,
                paths=[path.protobuf() for path in paths(path_list)],
            )
        )
        for element, path_list in dict(out).items()
    ]


def path(label: str = "", paths: t.Optional[t.List[st.Path]] = None) -> Path:
    """Builds a Path out of a label and a set of sub-paths"""
    if paths is None:
        paths = []
    return Path(
        sp.Path(label=label, paths=[element.protobuf() for element in paths])
    )


def straight_path(nodes: t.List[str]) -> Path:
    """Returns linear path between elements in the list"""
    if len(nodes) == 0:
        raise ValueError("At least one node must be provided")
    curr_sub_path: t.List[st.Path] = []
    for el in reversed(nodes):
        update = path(label=el, paths=curr_sub_path)
        curr_sub_path = [update]
    return update


def append_to_straight_path(
    curr_path: t.Optional[st.Path], new_element: str
) -> st.Path:
    if curr_path is None:
        return straight_path([new_element])
    else:
        return straight_path(
            [
                *(element for element in curr_path.to_strings_list()[0]),
                new_element,
            ]
        )


if t.TYPE_CHECKING:
    test_path: st.Path = Path(sp.Path())
