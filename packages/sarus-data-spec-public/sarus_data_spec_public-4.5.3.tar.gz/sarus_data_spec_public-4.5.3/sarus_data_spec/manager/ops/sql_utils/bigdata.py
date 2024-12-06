# pylint: disable=too-many-return-statements
from __future__ import annotations

from itertools import zip_longest
import typing as t
import warnings
import re

try:
    from scipy.stats import binom
except ModuleNotFoundError:
    warnings.warn("scipy not installed")

from sarus_data_spec.path import straight_path
import sarus_data_spec.typing as st

try:
    import sqlalchemy as sa
except ModuleNotFoundError:
    warnings.warn("sqlalchemy not installed")

T = t.TypeVar("T")


def split_quote(
    name: str, ident_quote: t.Optional[str] = None
) -> t.Tuple[str, ...]:
    """Extract qualified column or table names.
    It supports names containing dots or special characters.
    If ident_quote is provided it will quote all the name parts accordinly
    otherwise it will leave names as they are.
    If an empty string is provided it will unquote

    Args:
        name (str):
        ident_quote (str): the quote identifier

    Returns:
        Tuple[str, ...]:
    """

    def is_quoted(name: str) -> bool:
        return any([name.startswith(quote) for quote in ['"', "`", "["]])

    regex = re.compile(r"""((?:[^."\[\]]|"[^"]*"|\[[^\[]*\])+)""")
    parts = [
        sub_name for sub_name in regex.split(name) if sub_name not in [".", ""]
    ]

    if ident_quote is not None:
        parts = [
            f"{ident_quote}{part[1:-1]}{ident_quote}"
            if is_quoted(part)
            else f"{ident_quote}{part}{ident_quote}"
            for part in parts
        ]
    return tuple(parts)


def access_table_or_col(
    metadata_or_table: t.Any, key: str, create_cte: bool = True
) -> t.Any:
    """access child from an metadata_or_table.
    metadata_or_table: t.Union[
        sa.MetaData, sa.Table, t.Dict[str, sa.Table],  sa.sql.Selectable]

    if sa.sql.Selectable:
        returns the underlying sa.sql.expression.ColumnElement
    if sa.Table:
        returns sa.sql.expression.ColumnElement using the key.
    if create_cte is True access column using a column table expression (cte).
        returns a sa.sql.Selectable. In this cases the column is aliased
        by sqlalchemy.
    if metadata:
        returns sa.Table if no schema.
        if metadata was generated with schemas, it becomes of the form:
        metadata.tables = {'schema.table_name': table}
        which is a problem. It is thus split into:
        {'schema': {'table_name': table}}
        to make it usable.
    if t.Dict[str, sa.Table]:
        returns sa.Table using from key.
    """
    if isinstance(metadata_or_table, (sa.sql.Selectable, sa.Table)):
        if create_cte:
            return sa.select(
                # label('') tells SQLAlchemy to handle the alias for such col
                # without it will generate an alias with the same name as col
                # with it will assign a non-ambigous and allowed alias
                getattr(metadata_or_table.exported_columns, key).label(""),
            ).cte()
        if isinstance(metadata_or_table, sa.sql.Selectable):
            return metadata_or_table.exported_columns[0]
        return getattr(metadata_or_table.c, key)

    if isinstance(metadata_or_table, sa.MetaData):
        result: t.Dict[str, t.Any] = {}
        for child_key, child_value in metadata_or_table.tables.items():
            first_key, *rest = split_quote(child_key, "")
            if rest:
                if first_key not in result:
                    result[first_key] = {".".join(rest): child_value}
                else:
                    result[first_key][".".join(rest)] = child_value
            else:
                result[first_key] = child_value
        return result[key]
    else:
        # it is a dict on the form
        return metadata_or_table[key]


def grouped(
    iterable: t.Iterable[T], n: int = 2
) -> t.Iterable[t.Tuple[T, ...]]:
    """s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), ..."""
    return zip_longest(*[iter(iterable)] * n)


class SqlOperations:
    """It stores sql queries to be executed for bigdata computations.
    List of sql operations to be performed for bigdata. Results are
    stored in a dict: {path: {operation: result}}
    """

    def __init__(self, group_by: int = 1) -> None:
        self.queries: t.List[
            t.Tuple[sa.sql.ClauseElement, t.Optional[st.Type]]
        ] = []
        self.group_by = group_by

    def append(
        self,
        query: t.Optional[sa.sql.ClauseElement],
        result_type: t.Optional[st.Type] = None,
    ) -> None:
        if query is not None:
            self.queries.append((query, result_type))

    def extend(self, queries: t.Optional[SqlOperations]) -> None:
        if queries:
            self.queries.extend(queries.queries)

    async def execute(
        self,
        dataset: st.Dataset,
    ) -> t.Dict[st.Path, t.Dict[str, t.Any]]:
        """Execute all queries and reformat it as:
        {path: {operation: result}}. If types are provided they are passed to
        async_sql.
        """
        if len(self.queries) == 0:
            return {}

        results = []
        for grouped_queries in grouped(self.queries, self.group_by):
            queries = [query for query in grouped_queries if query]
            result_types: t.List[t.Optional[st.Type]] = [
                query[1] for query in queries
            ]
            assert len(set(result_types)) == 1
            final_query: t.Union[sa.ClauseElement, sa.CompoundSelect]
            if len(queries) > 1:
                final_query = sa.union_all(
                    *[
                        t.cast(sa.sql.selectable.Select, statement)
                        for statement, result_type in queries
                    ]
                )
            else:
                (final_query, _) = queries[0]

            rendered = sqlalchemy_query_to_string(final_query)
            query_result = await dataset.manager().async_sql(
                dataset, rendered, result_type=result_types[0]
            )
            results.extend(
                [
                    tuple(raw.values())
                    async for batch in query_result
                    for raw in batch.to_pylist()
                ]
            )

        # Reformat results as {path: {operation: result}}
        result_dict: t.Dict[st.Path, t.Dict[str, t.Any]] = {}
        str2path: t.Dict[str, st.Path] = {}
        for path_str, operation, *result in results:
            result_length = len(result)

            if path_str in str2path:
                path = str2path[path_str]
            else:
                splitted_path = (
                    [path_str]
                    if not path_str
                    else list(split_quote(path_str, ""))
                )
                path = straight_path(splitted_path)
                str2path[path_str] = path

            if path not in result_dict:
                if result_length == 1:
                    result_dict[path] = {operation: result[0]}
                elif result_length == 2:
                    result_dict[path] = {operation: {result[0]: result[1]}}
                else:
                    result_dict[path] = {operation: result}
            else:
                path_dict = result_dict[path]
                if result_length == 1:
                    if operation not in path_dict:
                        path_dict[operation] = result[0]
                    else:
                        if isinstance(path_dict[operation], t.List):
                            path_dict[operation].append(result[0])
                        else:
                            path_dict[operation] = [
                                path_dict[operation],
                                result[0],
                            ]

                elif result_length == 2:
                    if operation not in path_dict:
                        path_dict[operation] = {}
                    path_dict[operation][result[0]] = result[1]
                else:
                    path_dict[operation] = result
        return result_dict


def path_to_quoted_string(path: st.Path) -> str:
    """It transforms a path into a quoted string.
    eg:
    (my_schema, my.table) -> "my_schema"."my.table"

    where (my_schema, my.table) is the tuple representation of the st.Path

    Used to create sql queries and table objects manipulated by sqlachemy
    metadata.
    """
    return ".".join(f'"{path}"' for path in path.to_strings_list()[0])


def sqlalchemy_query_to_string(sa_query: sa.sql.ClauseElement) -> str:
    """Compiles the sqlalchemy query into a string"""
    return str(sa_query.compile(compile_kwargs={"literal_binds": True}))


def find_optimal_multiplier_fraction(
    n_start: int,
    min_sample: int,
    p_optimal: float = 0.9999,
    tol: float = 1e-4,
) -> float:
    """
    For a random subsample, this function calculates the optimal multiplier
    for a fraction derived from the ratio of the minimum sample size
    to the original sample size. The multiplier is determined such that it
    reach the probability (p_optimal) of obtaining
    a random subsample with a size greater than the minimum sample size.

    Parameters
    ----------
    n_start : int
        Original sample size.
    min_sample : int
        Minimum sample size or target sample size.
    p_optimal : float, optional
        Minimum probability threshold that the subsample size is at least
        min_sample. Default is 0.9999.
    tol : float, optional
        Tolerance for the bisection search. Default is 1e-4.

    Returns
    -------
    float
        Optimal multiplier for the fraction (min_sample/n_start).

    Note
    ----
    If the fraction is greater than or equal to 1, the function returns 1.

    """
    if min_sample == 0 or n_start == 0:
        return 0.0

    fraction = min_sample / n_start
    if fraction >= 1:
        return 1.0

    lower: float = 0.0
    upper = 1 / fraction
    while upper - lower > tol:
        mid = (upper + lower) / 2
        proba = 1 - binom.cdf(min_sample, n_start, mid * fraction)
        if proba < p_optimal:
            lower = mid
        else:
            upper = mid

    return upper
