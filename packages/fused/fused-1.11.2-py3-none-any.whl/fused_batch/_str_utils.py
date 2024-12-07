from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, TypeVar, Union
from urllib.parse import urlparse

if TYPE_CHECKING:
    from fused_batch.models.api.dataset import Table
    from fused_batch.models.internal.dataset import DatasetInputV2Table

T = TypeVar("T")


def is_url(path):
    prefixes = ["http://", "https://", "www."]
    return any(path.startswith(prefix) for prefix in prefixes)


def detect_passing_local_file_as_str(input: T) -> Union[T, Path]:
    if isinstance(input, str):
        try:
            parsed_url = urlparse(input)
            if parsed_url.scheme:
                # Do not do any rewriting if an explicit URL is passed in
                return input
        except:  # noqa: E722
            # Fall through to checking whether it exists as file
            pass

        as_path = Path(input)
        is_maybe_file = as_path.exists()

        if is_maybe_file:
            return as_path
    return input


def append_url_part(base: str, part: str) -> str:
    if base.endswith("/"):
        return f"{base[:-1]}/{part}"
    else:
        return f"{base}/{part}"


def table_to_name(table: Union[str, Table, DatasetInputV2Table]) -> str:
    # Table
    if hasattr(table, "name"):
        return table.name
    # DatasetInputV2Table
    if hasattr(table, "url"):
        table = table.url

    if table.endswith("/"):
        return table[:-1].rsplit("/", maxsplit=1)[-1]
    else:
        return table.rsplit("/", maxsplit=1)[-1]
