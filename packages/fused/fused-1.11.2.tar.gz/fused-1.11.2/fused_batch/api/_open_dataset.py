from typing import Optional

from fused_batch._options import options as OPTIONS
from fused_batch.models.api import Table
from fused_batch.models.api.job import _get_chunk


def post_open_table(
    table: Table,
    fetch_samples: Optional[bool] = None,
):
    should_fetch_samples = False
    if fetch_samples is not None:
        should_fetch_samples = fetch_samples
    elif OPTIONS.open.fetch_samples is not None:
        should_fetch_samples = OPTIONS.open.fetch_samples

    if should_fetch_samples:
        try:
            # TODO: refactor this
            base_path, table_name = table.url.rstrip("/").rsplit("/", maxsplit=1)
            first_chunk = table.chunk_metadata[0]
            table.sample = _get_chunk(
                base_path=base_path,
                tables=[table_name],
                file_id=first_chunk.file_id,
                chunk_id=first_chunk.chunk_id,
                n_rows=10,
            )
        except:  # noqa E722
            table.sample = None
