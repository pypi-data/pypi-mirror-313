from typing import Dict, List, cast
import warnings

try:
    from scipy.optimize import bisect
except ModuleNotFoundError:
    warnings.warn("Scipy not available")

from sarus_data_spec.dataset import Dataset
import sarus_data_spec.typing as st


async def differentiated_sampling_sizes(
    dataset: st.Dataset,
) -> Dict[st.Path, int]:
    """Get the sampling rates for each table"""
    parent_ds = cast(Dataset, dataset.parents()[0][0])
    parent_size = await parent_ds.manager().async_size(parent_ds)
    assert parent_size

    transform = dataset.transform().protobuf().spec.differentiated_sample
    if transform.HasField("fraction"):
        sampled_size = parent_size.statistics().size() * transform.fraction
    else:
        sampled_size = transform.size

    return await differentiated_sampling_sizes_bisection(
        parent_ds, int(sampled_size)
    )


async def differentiated_sampling_sizes_bisection(
    dataset: st.Dataset, sampled_size: int
) -> Dict[st.Path, int]:
    """Get the sampling rates for each table"""
    size = await dataset.manager().async_size(dataset)
    assert size
    size_stat = size.statistics()
    schema = await dataset.manager().async_schema(dataset)
    private_table_paths = schema.private_tables()
    public_table_paths = schema.public_tables()

    # test if min_table_size is not too high
    private_table_path_sizes = {
        table_path: size_stat.nodes_statistics(table_path)[0].size()
        for table_path in private_table_paths
    }
    public_table_path_sizes = {
        table_path: size_stat.nodes_statistics(table_path)[0].size()
        for table_path in public_table_paths
    }

    def new_size(max_table_size: float) -> int:
        return int(
            sum(
                [
                    min(
                        int(max_table_size),
                        table_path_size,
                    )
                    for table_path_size in private_table_path_sizes.values()
                ]
            )
            - sampled_size
        )

    private_size = sum(private_table_path_sizes.values())
    if private_size < sampled_size:
        # if already below sample size
        return {**private_table_path_sizes, **public_table_path_sizes}

    max_table_size = bisect(
        new_size, 0, private_size, xtol=len(private_table_path_sizes)
    )
    return {
        **{
            table_path: min(
                int(max_table_size),
                table_path_size,
            )
            for table_path, table_path_size in private_table_path_sizes.items()
        },
        **public_table_path_sizes,
    }


def sync_bisection(
    size_stat: st.Statistics, table_paths: List[st.Path], sampled_size: int
) -> Dict[st.Path, int]:
    table_path_sizes = {
        table_path: size_stat.nodes_statistics(table_path)[0].size()
        for table_path in table_paths
    }

    def new_size(max_table_size: float) -> int:
        return int(
            sum(
                [
                    min(
                        int(max_table_size),
                        table_path_size,
                    )
                    for table_path_size in table_path_sizes.values()
                ]
            )
            - sampled_size
        )

    if size_stat.size() < sampled_size:
        # if already below sample size
        return table_path_sizes

    max_table_size = bisect(
        new_size, 0, size_stat.size(), xtol=len(table_paths)
    )
    return {
        table_path: min(
            int(max_table_size),
            table_path_size,
        )
        for table_path, table_path_size in table_path_sizes.items()
    }
