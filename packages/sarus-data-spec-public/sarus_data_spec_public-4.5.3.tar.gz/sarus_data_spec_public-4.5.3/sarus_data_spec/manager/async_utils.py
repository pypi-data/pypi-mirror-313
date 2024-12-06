import asyncio
import asyncio.events as events
import typing as t

import pyarrow as pa

T = t.TypeVar("T")


def sync(coro: t.Coroutine) -> t.Any:
    """This runs an async function synchronously,
    even within an already runnning event loop,
    despite the apparent impossibility
    to nest loops within the same thread"""
    reset_at_completion = True
    try:
        curr_loop = asyncio.get_running_loop()
    except RuntimeError:
        reset_at_completion = False
    new_loop = asyncio.new_event_loop()
    new_loop._check_running = lambda: None  # type:ignore
    # method monkey patched since it raises an error
    # if another loop exists
    result = new_loop.run_until_complete(coro)
    if reset_at_completion:
        # this method allows to set the curr loop
        # as running,standard method asyncio.set_event_loop
        # does not work
        events._set_running_loop(curr_loop)
    new_loop.close()
    return result


def sync_iterator_from_async_iterator(
    async_iterator: t.AsyncIterator[T],
) -> t.Iterator[T]:
    """This methods returns an iterator from an async iterator.
    The generator method allows to execute one step at a time the
    anext method of the async generator.
    """
    # The loop used to generate batches
    new_loop = asyncio.new_event_loop()
    new_loop._check_running = lambda: None  # type:ignore
    # method monkey patched since it raises an error
    # if another loop exists

    def generator() -> t.Iterator[T]:
        """This method creates an iterator. At each generator
        step, the current loop is taken and suspended and the
        anext method of the async generator is executed in
        another loop
        """
        keep_on = True
        while keep_on:
            reset_at_completion = True
            try:
                curr_loop = asyncio.get_running_loop()
            except RuntimeError:
                reset_at_completion = False
            try:
                batch = new_loop.run_until_complete(async_iterator.__anext__())

            except StopAsyncIteration:
                keep_on = False
                if reset_at_completion:
                    events._set_running_loop(curr_loop)
            except Exception as exception:
                if reset_at_completion:
                    events._set_running_loop(curr_loop)
                new_loop.close()
                raise exception
            else:
                if reset_at_completion:
                    # asyncio.set_event_loop(curr_loop) not working
                    events._set_running_loop(curr_loop)
                yield batch
        new_loop.close()

    return generator()


def sync_iterator(
    async_iterator_coro: t.Coroutine,
) -> t.Iterator[t.Any]:
    """This methods returns an iterator from an async iterator coroutine.
    It first executes the coroutine to obtain an async generator.
    Then, generator method allows to execute one step at a time the
    anext method of the async generator.
    """
    async_gen = sync(async_iterator_coro)
    return sync_iterator_from_async_iterator(async_gen)


async def async_iter(data_list: t.Collection[T]) -> t.AsyncIterator[T]:
    """Convert a collection into an AsyncIterator."""
    for data in data_list:
        yield data


async def decoupled_async_iter(
    source: t.AsyncIterator[T], buffer_size: int = 100
) -> t.AsyncIterator[T]:
    """Create a consumer/producer pattern using an asyncio.Queue."""
    queue: asyncio.Queue = asyncio.Queue(maxsize=buffer_size)

    async def producer() -> None:
        async for x in source:
            await queue.put(x)
        await queue.put(None)  # producer finished

    # Launch the iteration of source iterator
    loop = asyncio.get_running_loop()
    loop.create_task(producer())

    while True:
        x = await queue.get()
        if x is None:
            queue.task_done()
            break
        queue.task_done()
        yield x


def to_recordbatch(
    output: t.Mapping[str, pa.Table],
) -> t.AsyncIterator[pa.RecordBatch]:
    """This function is inspired from arrow_recordbatch in
    sarus_data_spec/manager/ops/source/sql/arrow.py
    In order to create a recordbatch from different pyarrow tables, a struct is
    created where the corresponding other missing tables
    have been added as None"""
    struct_arrays = {
        table_path: pa.StructArray.from_arrays(
            arrays=[el.combine_chunks() for el in table.flatten()],
            names=table.column_names,
        )
        for table_path, table in output.items()
    }
    batches = []
    names = list(struct_arrays.keys())

    for current_table, arr_array in struct_arrays.items():
        # iterate over tables
        arrays_list = [
            pa.array(
                [None] * len(arr_array),
                type=struct.type,
            )
            if current_table != table
            else arr_array
            for table, struct in struct_arrays.items()
        ]
        fields = [
            pa.field(name=name, type=arr.type)
            for name, arr in zip(names, arrays_list)
        ]
        fields.append(
            pa.field(
                name="field_selected", type=pa.large_string(), nullable=False
            )
        )
        arrays_list.append(
            pa.array([current_table] * len(arr_array), type=pa.large_string())
        )
        batches.append(
            pa.RecordBatch.from_arrays(
                arrays_list, schema=pa.schema(fields=fields)
            )
        )
    return async_iter(batches)


def standardize_sql_query(
    parent_schema_name: str,
    query: t.Union[str, t.Mapping[t.Union[str, t.Tuple[str, ...]], str]],
) -> t.Mapping[str, str]:
    """It transforms any query variant (string, dict etc) in
    t.Mapping[str, str]. Moreover it applies the rules to preserve or not
    the parent schema in the map key which will be used as parecordbach name.

    If query is:
    {'a.b.c': sqlquerystr, 'a.d.e': sqlquerystr} -> override parent schema name
    {'a.b': sqlquerystr, 'a.c': sqlquerystr} override parent schema name
    {'b': sqlquerystr, 'c': sqlquerystr} preserve parent schema name
    {'a.b.c': sqlquerystr, 'd.e': sqlquerystr} preserve parent schema name
    {'a': 'q'} -> override parent schema name
    {'a.b': 'q'} -> override parent schema name
    sqlquerystr  -> preserve parent schema name
    """

    if isinstance(query, str):
        # we preserve the schema name of the parent
        queries = {parent_schema_name: query}
    else:
        if len(query) == 1:
            # we override the schema name
            queries = {
                key if isinstance(key, str) else ".".join(key): value
                for key, value in query.items()
            }
        else:
            # we override if prefix is the same otherwise we preserve
            prefixes = [
                key.split(".")[0] if isinstance(key, str) else key[0]
                for key in list(query.keys())
            ]
            if len(prefixes) == len(set(prefixes)):
                # all prefixes are the same, we preserve parents schema
                queries = {
                    f"{parent_schema_name}.{key}"
                    if isinstance(key, str)
                    else ".".join([parent_schema_name, *key]): value
                    for key, value in query.items()
                }
            else:
                # we override parents schema
                queries = {
                    key if isinstance(key, str) else ".".join(key): value
                    for key, value in query.items()
                }
    return queries
