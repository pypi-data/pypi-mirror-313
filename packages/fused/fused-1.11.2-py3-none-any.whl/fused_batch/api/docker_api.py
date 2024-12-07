from __future__ import annotations

import json
import shlex
import shutil
import subprocess
from base64 import b64encode
from functools import lru_cache
from io import SEEK_SET, BytesIO
from pathlib import Path
from typing import (
    BinaryIO,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Sequence,
    Union,
    overload,
)
from uuid import uuid4

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
from fused_batch._options import DEV_DEFAULT_BASE_URL, STAGING_DEFAULT_BASE_URL
from fused_batch._options import options as OPTIONS
from fused_batch._request import raise_for_status
from fused_batch.api._open_dataset import post_open_table
from fused_batch.api.api import FusedAPI
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

# TODO: Consider making this us-west-2, depending on where the user is logged in
# DEFAULT_REPOSITORY = "926411091187.dkr.ecr.us-east-1.amazonaws.com/fused-job2"
DEFAULT_REPOSITORY = "926411091187.dkr.ecr.us-west-2.amazonaws.com/fused-job2"
DEFAULT_TAG = "latest"

MAX_ERROR_MESSAGE_SIZE = 10000
JOB_MOUNT_PATH = "/job/job.json"
JOB_INPUT_MOUNT_PATH = "/job/input"
DEFAULT_JOB_INPUT_HOST = "/tmp"


class DockerRunnable(BaseModel):
    command: str

    def run_and_get_bytes(self) -> bytes:
        """
        Run the command and return the bytes written to stdout.

        Raises an exception if the return code is not 0.
        """
        # TODO: Disable shell here
        # Check is false because we check it ourselves next
        p = subprocess.run(self.command, shell=True, capture_output=True, check=False)
        if p.returncode:
            error_message = p.stderr.decode("utf-8")
            if len(error_message) > MAX_ERROR_MESSAGE_SIZE:
                error_message = (
                    error_message[:MAX_ERROR_MESSAGE_SIZE] + "... (truncated)"
                )
            if len(error_message) == 0:
                error_message = "No message on stderr"
            raise ValueError(f"Failed ({p.returncode}): {error_message}")
        return p.stdout

    def run_and_get_output(self) -> str:
        """
        Run the command and return the utf-8 string written to stdout.

        Raises an exception if the return code is not 0.
        """
        return self.run_and_get_bytes().decode("utf-8")

    def run_and_tail_output(self) -> None:
        """
        Run the command and print output to stdout.

        Raises an exception if the return code is not 0.
        """
        # TODO: Disable shell here
        subprocess.run(self.command, shell=True, check=True)


class FusedDockerAPI:
    """API for running jobs in the Fused Docker container."""

    repository: str
    tag: str
    mount_aws_credentials: bool
    mount_data_directory: Optional[str]
    mount_job_input_directory: Optional[str]
    additional_docker_args: Sequence[str]
    docker_command_wrapper: Optional[Callable[[str], str]]
    auth_token: Optional[str]
    is_staging: bool
    is_gcp: bool
    is_aws: bool

    def __init__(
        self,
        *,
        repository: str = DEFAULT_REPOSITORY,
        tag: str = DEFAULT_TAG,
        mount_aws_credentials: bool = False,
        mount_data_directory: Optional[str] = None,
        mount_job_input_directory: Optional[str] = DEFAULT_JOB_INPUT_HOST,
        additional_docker_args: Sequence[str] = (),
        docker_command_wrapper: Optional[Callable[[str], str]] = None,
        auth_token: Optional[str] = None,
        auto_auth_token: bool = True,
        set_global_api: bool = True,
        is_staging: Optional[bool] = None,
        is_gcp: bool = False,
        is_aws: bool = False,
        pass_config_as_file: bool = True,
    ):
        """Create a FusedDockerAPI instance.

        Keyword Args:
            repository: Repository name for jobs to start.
            tag: Tag name for jobs to start. Defaults to `'latest'`.
            mount_aws_credentials: Whether to add an additional volume for AWS credentials in the job. Defaults to False.
            mount_data_directory: If not None, path on the host to mount as the /data directory in the container. Defaults to None.
            mount_job_input_directory: If not None, path on the host to mount as the /job/input/ directory in the container. Defaults to None.
            additional_docker_args: Additional arguments to pass to Docker. Defaults to empty.
            docker_command_wrapper: Command to wrap the Docker execution in, e.g. `'echo {} 1>&2; exit 1'`. Defaults to None for no wrapping.
            auth_token: Auth token to pass to the Docker command. Defaults to automatically detect when auto_auth_token is True.
            auto_auth_token: Obtain the auth token from the (previous) global Fused API. Defaults to True.
            set_global_api: Set this as the global API object. Defaults to True.
            is_staging: Set this if connecting to the Fused staging environment. Defaults to None to automatically detect.
            is_gcp: Set this if running in GCP. Defaults to False.
            is_aws: Set this if running in AWS. Defaults to False.
            pass_config_as_file: If True, job configurations are first written to a temporary file and then passed to Docker. Defaults to True.
        """
        self.repository = repository
        self.tag = tag
        self.mount_aws_credentials = mount_aws_credentials
        self.mount_data_directory = mount_data_directory
        self.mount_job_input_directory = mount_job_input_directory
        self.additional_docker_args = additional_docker_args
        self.docker_command_wrapper = docker_command_wrapper
        self.is_gcp = is_gcp
        self.is_aws = is_aws
        self.pass_config_as_file = pass_config_as_file
        if auth_token or not auto_auth_token:
            self.auth_token = auth_token
        else:
            self.auth_token = FusedAPI(set_global_api=False).auth_token()

        if is_staging is not None:
            self.is_staging = is_staging
        else:
            # Autodetect whether staging flag should be set based on base_url.
            self.is_staging = OPTIONS.base_url in (
                STAGING_DEFAULT_BASE_URL,
                DEV_DEFAULT_BASE_URL,
            )

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
    ) -> DockerRunnable:
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

        args = ["--output-to-stdout"]
        if self.pass_config_as_file:
            config_path = self._make_config_path(config.model_dump_json())
            args.append("--config-from-file")
            args.append(JOB_MOUNT_PATH)
        else:
            config_path = None
            args.append("--config")
            args.append(config.model_dump_json())
        if file_id is not None:
            args.append("--file-id")
            args.append(str(file_id))

        if chunk_id is not None:
            args.append("--chunk-id")
            args.append(str(chunk_id))

        if whole_file:
            args.append("--whole-file")

        return self._make_run_command("make-sample", args, config_path=config_path)

    def start_job(
        self,
        config: Union[JobConfig, JobStepConfig],
        *,
        additional_env: Optional[Sequence[str]] = ("FUSED_CREDENTIAL_PROVIDER=ec2",),
        **kwargs,
    ) -> DockerRunnable:
        """Execute an operation

        Args:
            config: the configuration object to run in the job.

        Keyword Args:
            additional_env: Any additional environment variables to be passed into the job, each in the form KEY=value. Defaults to None.
        """
        assert (
            kwargs.get("region") is None
        ), "region may not be specified with FusedDockerAPI"
        assert (
            kwargs.get("instance_type") is None
        ), "instance_type may not be specified with FusedDockerAPI"
        assert (
            kwargs.get("disk_size_gb") is None
        ), "disk_size_gb may not be specified with FusedDockerAPI"
        assert (
            kwargs.get("image_name") is None
        ), "image_name may not be specified with FusedDockerAPI"

        if isinstance(config, JobStepConfig):
            config = JobConfig(steps=[config])

        if self.pass_config_as_file:
            config_path = self._make_config_path(config.model_dump_json())
            args = ["--config-from-file", JOB_MOUNT_PATH]
        else:
            config_path = None
            args = ["--config", config.model_dump_json()]

        # TODO: This should return a RunResponse
        return self._make_run_command(
            "run-config", args, env=additional_env, config_path=config_path
        )

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
        env: Optional[Sequence[str]] = None,
        config_path: Optional[str] = None,
    ) -> DockerRunnable:
        docker_args_part: List[str] = [*self.additional_docker_args]
        if env:
            for e in env:
                docker_args_part.append("-e")
                docker_args_part.append(shlex.quote(e))
        if self.auth_token:
            docker_args_part.append("-e")
            docker_args_part.append(f"FUSED_AUTH_TOKEN={self.auth_token}")
        if self.is_staging:
            docker_args_part.append("-e")
            docker_args_part.append("__FUSED_STAGING_LICENSE_CHECK=1")
        if self.mount_aws_credentials:
            docker_args_part.append("-v")
            docker_args_part.append(
                '"$HOME/.aws/credentials:/root/.aws/credentials:ro"'
            )
        if self.mount_data_directory is not None:
            docker_args_part.append("--mount")
            docker_args_part.append(
                f"type=bind,src={self.mount_data_directory},target=/data"
            )
            docker_args_part.append("-e")
            docker_args_part.append("FUSED_DATA_DIRECTORY=/data")
        if config_path is not None:
            docker_args_part.append("--mount")
            docker_args_part.append(
                f"type=bind,src={config_path},target={JOB_MOUNT_PATH}"
            )
        if self.mount_job_input_directory is not None:
            docker_args_part.append("--mount")
            docker_args_part.append(
                f"type=bind,src={self.mount_job_input_directory},target={JOB_INPUT_MOUNT_PATH}"
            )
        if self.is_gcp:
            docker_args_part.append("-e")
            docker_args_part.append("FUSED_GCP=1")
        if self.is_aws:
            docker_args_part.append("-e")
            docker_args_part.append("FUSED_AWS=1")

        args_part = [shlex.quote(a) for a in args]

        docker_image_name = f"{self.repository}:{self.tag}"

        job_command = shlex.quote(command)
        docker_command = f"docker run {' '.join(docker_args_part)} --rm {docker_image_name} {job_command} {' '.join(args_part)}"
        if self.docker_command_wrapper is not None:
            docker_command = self.docker_command_wrapper(docker_command)

        return DockerRunnable(command=docker_command)

    def _make_config_path(self, config_json: str) -> str:
        temp_file_name = f"/tmp/job_{uuid4()}.json"

        # TODO: Confirm temp_file_name doesn't already exist

        # We don't directly create the file in order to support running over SSH
        create_command = f"cat | base64 --decode > {temp_file_name}"
        if self.docker_command_wrapper is not None:
            create_command = self.docker_command_wrapper(create_command)

        b64data = b64encode(config_json.encode("utf-8"))

        # Don't capture output so that if the command errors, the output gets
        # sent back to the user
        subprocess.run(
            create_command,
            shell=True,
            check=True,
            input=b64data,
        )
        return temp_file_name

    def upload(self, path: str, data: Union[bytes, BinaryIO]) -> None:
        """Upload a binary blob to a cloud location"""
        raise NotImplementedError("upload is not implemented on FusedDockerAPI")

    def _replace_df_input(
        self, input: Union[str, List[str], gpd.GeoDataFrame]
    ) -> Union[str, List[str]]:
        replacement_bytes: Optional[bytes] = None
        extension: Optional[str] = None
        if isinstance(input, gpd.GeoDataFrame):
            with BytesIO() as tmp:
                input.to_parquet(tmp)
                tmp.seek(0, SEEK_SET)
                replacement_bytes = tmp.getvalue()
                extension = "parquet"
        elif isinstance(input, Path):
            with open(input, "rb") as f:
                replacement_bytes = f.read()
                extension = input.name.split(".", 1)[-1]

        if replacement_bytes is not None:
            assert (
                self.mount_job_input_directory
            ), "mount_job_input_directory must be set to pass DataFrame input"
            temp_file_name = f"df_{uuid4()}.{extension}"
            host_file_name = f"{Path(self.mount_job_input_directory) / temp_file_name}"
            container_file_name = f"file://{JOB_INPUT_MOUNT_PATH}/{temp_file_name}"

            # TODO: Confirm temp_file_name doesn't already exist

            # We don't directly create the file in order to support running over SSH
            # We use "base64 --decode" because Parquet as a binary file could interact with the shell in bad ways
            create_command = f"cat | base64 --decode > {host_file_name}"
            if self.docker_command_wrapper is not None:
                create_command = self.docker_command_wrapper(create_command)

            b64data = b64encode(replacement_bytes)

            # Don't capture output so that if the command errors, the output gets
            # sent back to the user
            subprocess.run(
                create_command,
                shell=True,
                check=True,
                input=b64data,
            )
            return container_file_name
        else:
            return input

    def _health(self) -> bool:
        """Check the health of the API backend"""
        runnable = self._make_run_command("version", [])
        runnable.run_and_get_output()
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


def ssh_command_wrapper(conn_string: str) -> Callable[[str], str]:
    """Creates a command wrapper that connects via SSH and sudo runs the command."""
    return (
        lambda command: f'ssh {conn_string} -t "sudo sh -c "{shlex.quote(shlex.quote(command))}""'
    )


def gcloud_command_wrapper(
    conn_string: str, *, zone: Optional[str] = None, project: Optional[str] = None
) -> Callable[[str], str]:
    """Creates a command wrapper that connects via gcloud and runs the command."""
    zone_arg = f"--zone {zone}" if zone else ""
    project_arg = f"--project {project}" if project else ""
    return (
        lambda command: f"gcloud compute ssh {zone_arg} {project_arg} {conn_string} --command {shlex.quote(command)}"
    )
