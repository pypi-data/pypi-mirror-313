from __future__ import annotations

import json
import shutil
from functools import lru_cache
from pathlib import Path
from typing import (
    Any,
    BinaryIO,
    Dict,
    List,
    Literal,
    Optional,
    Sequence,
    Union,
    overload,
)

import geopandas as gpd
import pandas as pd
import requests
from pydantic import BaseModel

from fused_batch._deserialize import (
    zip_to_join_args,
    zip_to_join_singlefile_args,
    zip_to_map_args,
)
from fused_batch._deserialize_parquet import parquet_to_df
from fused_batch._global_api import set_api
from fused_batch._options import options as OPTIONS
from fused_batch._request import raise_for_status
from fused_batch.api._open_dataset import post_open_table
from fused_batch.models import JoinInput, JoinSingleFileInput, MapInput
from fused_batch.models.api import (
    JobConfig,
    JobStepConfig,
    JoinJobStepConfig,
    JoinSinglefileJobStepConfig,
    ListDetails,
    MapJobStepConfig,
    Table,
)
from fused_batch.models.api._folder import Folder

DEFAULT_ENDPOINT = "http://localhost:8789"


class DockerHTTPRunnable(BaseModel):
    endpoint: str
    command: Any = None

    def run_and_get_bytes(self) -> bytes:
        """
        Run the command and return the bytes written to stdout.

        Raises an exception if an HTTP error status is returned.
        """
        r = requests.post(
            url=self.endpoint,
            json=self.command,
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.content

    def run_and_get_output(self) -> str:
        """
        Run the command and return the utf-8 string written to stdout.

        Raises an exception if an HTTP error status is returned.
        """
        return self.run_and_get_bytes().decode("utf-8")

    def run_and_tail_output(self) -> None:
        """
        Run the command and print output to stdout.

        Raises an exception if an HTTP error status is returned.
        """
        with requests.post(
            url=self.endpoint,
            json=self.command,
            timeout=OPTIONS.request_timeout,
            stream=True,
        ) as r:
            if r.encoding is None:
                r.encoding = "utf-8"
            raise_for_status(r)
            for line in r.iter_lines(decode_unicode=True):
                print(line)


class FusedDockerHTTPAPI:
    """API for running jobs in the Fused Docker container over an HTTP connection."""

    endpoint: str

    def __init__(
        self,
        endpoint: str = DEFAULT_ENDPOINT,
        *,
        set_global_api: bool = True,
    ):
        """Create a FusedDockerHTTPAPI instance.

        Args:
            endpoint: The HTTP endpoint to connect to. Defaults to `"http://localhost:8789"`.

        Keyword Args:
            set_global_api: Set this as the global API object. Defaults to True.
        """
        self.endpoint = endpoint.rstrip("/")

        if set_global_api:
            set_api(self)

    def sample_map(
        self,
        config: MapJobStepConfig,
        *,
        file_id: Optional[Union[str, int]] = None,
        chunk_id: Optional[int] = None,
        n_rows: Optional[int] = None,
    ) -> MapInput:
        """Fetch a sample of an operation

        Args:
            config: The configuration to sample from.

        Keyword Args:
            file_id: The identifier of this file. Defaults to None.
            chunk_id: The numeric index of the chunk within the file to fetch. Defaults to None.
            n_rows: The maximum number of rows to sample. Defaults to None for all rows in the chunk.
        """
        assert isinstance(config, MapJobStepConfig)
        sample_request = self._sample(
            config,
            file_id=file_id,
            chunk_id=chunk_id,
        )
        content = sample_request.run_and_get_bytes()
        return zip_to_map_args(content, n_rows=n_rows)

    def _whole_file_sample_map(
        self,
        config: MapJobStepConfig,
        *,
        file_id: Union[str, int],
        n_rows: Optional[int] = None,
    ) -> MapInput:
        assert isinstance(config, MapJobStepConfig)
        sample_request = self._sample(
            config,
            file_id=file_id,
            whole_file=True,
        )
        content = sample_request.run_and_get_bytes()
        return zip_to_map_args(content, n_rows=n_rows)

    def download_table_bbox(
        self,
        path: str,
        minx: float,
        miny: float,
        maxx: float,
        maxy: float,
        n_rows: Optional[int] = None,
        columns: Optional[List[str]] = None,
        clip: bool = True,
        buffer: Optional[float] = None,
    ) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
        args = [
            "bbox",
            "--output-to-stdout",
            "--base-path",
            path,
            "--bbox-minx",
            str(minx),
            "--bbox-miny",
            str(miny),
            "--bbox-maxx",
            str(maxx),
            "--bbox-maxy",
            str(maxy),
        ]
        if n_rows is not None:
            args.append("--n-rows")
            args.append(str(n_rows))
        if columns is not None:
            for column in columns:
                args.append("--columns")
                args.append(column)
        args.append("--clip" if clip else "--no-clip")
        if buffer is not None:
            args.append("--buffer")
            args.append(str(buffer))

        request = self._make_run_command("download-table", args)
        content = request.run_and_get_bytes()
        return parquet_to_df(content)

    def sample_join(
        self,
        config: JoinJobStepConfig,
        *,
        file_id: Optional[Union[str, int]] = None,
        chunk_id: Optional[int] = None,
        n_rows: Optional[int] = None,
    ) -> JoinInput:
        """Fetch a sample of an operation

        Args:
            config: The configuration to sample from.

        Keyword Args:
            file_id: The identifier of this file. Defaults to None.
            chunk_id: The numeric index of the chunk within the file to fetch. Defaults to None.
            n_rows: The maximum number of rows to sample from the left dataset. Defaults to None for all rows in the chunk.
        """
        assert isinstance(config, JoinJobStepConfig)
        sample_request = self._sample(
            config,
            file_id=file_id,
            chunk_id=chunk_id,
        )
        content = sample_request.run_and_get_bytes()
        return zip_to_join_args(content, n_rows=n_rows)

    def sample_single_file_join(
        self,
        config: JoinSinglefileJobStepConfig,
        *,
        file_id: Optional[Union[str, int]] = None,
        chunk_id: Optional[int] = None,
        n_rows: Optional[int] = None,
    ) -> JoinSingleFileInput:
        """Fetch a sample of an operation

        Args:
            config: The configuration to sample from.

        Keyword Args:
            file_id: The identifier of this file. Defaults to None.
            chunk_id: The numeric index of the chunk within the file to fetch. Defaults to None.
            n_rows: The maximum number of rows to sample from the left dataset. Defaults to None for all rows in the chunk.
        """
        assert isinstance(config, JoinSinglefileJobStepConfig)
        sample_request = self._sample(
            config,
            file_id=file_id,
            chunk_id=chunk_id,
        )
        content = sample_request.run_and_get_bytes()
        return zip_to_join_singlefile_args(content, n_rows=n_rows)

    def _sample(
        self,
        config: Union[MapJobStepConfig, JoinJobStepConfig, JoinSinglefileJobStepConfig],
        *,
        file_id: Optional[Union[str, int]] = None,
        chunk_id: Optional[int] = None,
        whole_file: bool = False,
    ) -> DockerHTTPRunnable:
        """Fetch a sample of an operation

        Args:
            config: The configuration to sample from.

        Keyword Args:
            file_id: The identifier of this file. Defaults to None.
            chunk_id: The numeric index of the chunk within the file to fetch. Defaults to None.
        """
        assert (
            isinstance(config, MapJobStepConfig)
            or isinstance(config, JoinJobStepConfig)
            or isinstance(config, JoinSinglefileJobStepConfig)
        )

        args = ["--output-to-stdout", "--config", config.model_dump_json()]

        if file_id is not None:
            args.append("--file-id")
            args.append(str(file_id))

        if chunk_id is not None:
            args.append("--chunk-id")
            args.append(str(chunk_id))

        if whole_file:
            args.append("--whole-file")

        return self._make_run_command("make-sample", args)

    def start_job(
        self,
        config: Union[JobConfig, JobStepConfig],
        **kwargs,
    ) -> DockerHTTPRunnable:
        """Execute an operation

        Args:
            config: the configuration object to run in the job.
        """
        assert (
            kwargs.get("region") is None
        ), "region may not be specified with FusedDockerHTTPAPI"
        assert (
            kwargs.get("instance_type") is None
        ), "instance_type may not be specified with FusedDockerHTTPAPI"
        assert (
            kwargs.get("disk_size_gb") is None
        ), "disk_size_gb may not be specified with FusedDockerHTTPAPI"
        assert (
            kwargs.get("additional_env") is None
        ), "additional_env may not be specified with FusedDockerHTTPAPI"
        assert (
            kwargs.get("image_name") is None
        ), "image_name may not be specified with FusedDockerHTTPAPI"

        if isinstance(config, JobStepConfig):
            config = JobConfig(steps=[config])

        args = ["--config", config.model_dump_json()]

        # TODO: This should return a RunResponse
        return self._make_run_command("run-config", args)

    def open_table(
        self,
        path: str,
        *,
        fetch_samples: Optional[bool] = None,
    ) -> Table:
        """Open a Table object given a path to the root of the table

        Args:
            path: The path to the root of the table on remote storage

        Keyword Args:
            fetch_samples: If True, fetch sample of each table when opening the dataset.

        Example:

            ```python
            table = fused.open_table(path="s3://my_bucket/path/to/dataset/table/")
            ```

        Returns:
            A Table object
        """
        args = ["--base-path", path, "--output-to-stdout"]

        runnable = self._make_run_command("open-table", args)
        content = runnable.run_and_get_bytes()
        table = Table.model_validate_json(content)
        post_open_table(table=table, fetch_samples=fetch_samples)
        return table

    def open_folder(
        self,
        path: str,
        *,
        fetch_minimal_table_metadata: Optional[bool] = None,
        fetch_table_metadata: Optional[bool] = None,
        fetch_samples: Optional[bool] = None,
        table_mode: bool = True,
        max_depth: Optional[int] = None,
    ) -> Folder:
        """Open all Table objects under the path.

        Args:
            path: The path to the root of the folder on remote storage

        Keyword Args:
            fetch_table_metadata: If True, fetch metadata on each table when getting dataset metadata.
            fetch_samples: If True, fetch sample of each table when opening the dataset.
            max_depth: Maximum depth of Tables to open. Beyond this tables will be opened virtually.

        Example:

            datasets = fused.open_folder(
                path="s3://my_bucket/path/to/folder/"
            )

        Returns:
            A list of Dataset objects
        """
        should_fetch_table_metadata = False
        if fetch_table_metadata is not None:
            should_fetch_table_metadata = fetch_table_metadata
        elif OPTIONS.open.fetch_table_metadata is not None:
            should_fetch_table_metadata = OPTIONS.open.fetch_table_metadata

        should_fetch_minimal_table_metadata = True
        if fetch_minimal_table_metadata is not None:
            should_fetch_minimal_table_metadata = fetch_minimal_table_metadata
        elif OPTIONS.open.fetch_minimal_table_metadata is not None:
            should_fetch_minimal_table_metadata = (
                OPTIONS.open.fetch_minimal_table_metadata
            )

        args = ["--base-path", path, "--output-to-stdout"]

        args.append("--fetch-table-metadata")
        args.append("True" if should_fetch_table_metadata else "False")
        args.append("--fetch-minimal-table-metadata")
        args.append("True" if should_fetch_minimal_table_metadata else "False")
        if max_depth is not None:
            args.append("--max-depth")
            args.append(f"{max_depth}")

        cmd = "open-table-folder" if table_mode else "open-dataset-folder"
        runnable = self._make_run_command(cmd, args)
        content = runnable.run_and_get_bytes()
        folder = Folder.model_validate_json(content)
        for table in folder.tables:
            post_open_table(
                table=table,
                fetch_samples=fetch_samples,
            )
        return folder

    def _make_run_command(
        self,
        command: str,
        args: Sequence[str],
    ) -> DockerHTTPRunnable:
        args_part = [command, *list(args)]
        return DockerHTTPRunnable(endpoint=f"{self.endpoint}/cli", command=args_part)

    def upload(self, path: str, data: Union[bytes, BinaryIO]) -> None:
        """Upload a binary blob to a cloud location"""
        raise NotImplementedError("upload is not implemented on FusedDockerAPI")

    def _replace_df_input(
        self, input: Union[str, List[str], gpd.GeoDataFrame]
    ) -> Union[str, List[str]]:
        if isinstance(input, gpd.GeoDataFrame):
            # TODO: Consider encoding in line?
            raise NotImplementedError(
                "Cannot pass GeoDataFrame input through FusedDockerHTTPAPI"
            )
        elif isinstance(input, Path):
            # TODO: Consider encoding in line?
            raise NotImplementedError(
                "Cannot pass Path input through FusedDockerHTTPAPI"
            )
        else:
            return input

    def _health(self) -> bool:
        """Check the health of the API backend"""
        r = requests.get(
            url=f"{self.endpoint}/health",
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return True

    @overload
    def list(self, path: str, *, details: Literal[True]) -> List[ListDetails]:
        ...

    @overload
    def list(self, path: str, *, details: Literal[False] = False) -> List[str]:
        ...

    def list(self, path: str, *, details: bool = False):
        args = ["--path", path]

        if details:
            args.append("--details")

        runnable = self._make_run_command("files-list", args)
        content = runnable.run_and_get_bytes()
        result = json.loads(content)
        if details:
            result = [ListDetails.model_validate(detail) for detail in result]
        return result

    def delete(self, path: str, max_deletion_depth: int | Literal["unlimited"]) -> bool:
        args = ["--path", path, "--max-deletion-depth", str(max_deletion_depth)]
        runnable = self._make_run_command("files-delete", args)
        content = runnable.run_and_get_bytes()
        return json.loads(content)

    def get(self, path: str) -> bytes:
        url = self.sign_url(path)
        r = requests.get(
            url=url,
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.content

    def download(self, path: str, local_path: Union[str, Path]) -> None:
        url = self.sign_url(path)
        r = requests.get(
            url=url,
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        with open(local_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    def sign_url(self, path: str) -> str:
        args = ["--path", path]

        runnable = self._make_run_command("files-sign-url", args)
        content = runnable.run_and_get_bytes()
        return json.loads(content)

    def sign_url_prefix(self, path: str) -> Dict[str, str]:
        args = ["--path", path]

        runnable = self._make_run_command("files-sign-url-prefix", args)
        content = runnable.run_and_get_bytes()
        return json.loads(content)

    def _get_table_names(self, path: str) -> List[str]:
        tables: List[str] = []
        for table_path in self.list(path):
            table_name = table_path.split("/")[-1]
            tables.append(table_name)

        return tables

    @lru_cache
    def dependency_whitelist(self) -> Dict[str, str]:
        runnable = self._make_run_command("dependency-whitelist", [])
        content = runnable.run_and_get_bytes()
        return json.loads(content)
