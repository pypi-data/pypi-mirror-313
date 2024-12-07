from __future__ import annotations

import shutil
import time
import uuid
import warnings
from functools import lru_cache
from io import SEEK_SET
from pathlib import Path
from tempfile import TemporaryFile
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

import fused_batch
import fused_batch.models.request as request_models
from fused_batch._auth import AUTHORIZATION
from fused_batch._deserialize import (
    zip_to_join_args,
    zip_to_join_singlefile_args,
    zip_to_map_args,
)
from fused_batch._deserialize_parquet import parquet_to_df
from fused_batch._global_api import set_api, set_api_class
from fused_batch._options import PROD_DEFAULT_BASE_URL
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
    UdfAccessToken,
    UdfAccessTokenList,
)
from fused_batch.models.api._folder import Folder
from fused_batch.models.internal import Jobs, RunResponse
from fused_batch.models.internal.job import CoerceableToJobId, _object_to_job_id
from fused_batch.models.request import WHITELISTED_INSTANCE_TYPES
from fused_batch.models.udf._udf_registry import UdfRegistry
from fused_batch.models.udf.base_udf import (
    METADATA_FUSED_EXPLORER_TAB,
    METADATA_FUSED_ID,
    METADATA_FUSED_SLUG,
)
from fused_batch.models.udf.udf import AnyBaseUdf, RootAnyBaseUdf
from fused_batch.warnings import FusedNonProductionWarning


class FusedAPI:
    """API for running jobs in the Fused service."""

    base_url: str

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        set_global_api: bool = True,
        credentials_needed: bool = True,
    ):
        """Create a FusedAPI instance.

        Keyword Args:
            base_url: The Fused instance to send requests to. Defaults to `https://www.fused.io/server/v1`.
            set_global_api: Set this as the global API object. Defaults to True.
            credentials_needed: If True, automatically attempt to log in. Defaults to True.
        """
        if credentials_needed:
            AUTHORIZATION.initialize()
        base_url = base_url or OPTIONS.base_url

        self.base_url = base_url
        self._check_is_prod()

        if set_global_api:
            set_api(self)

    def _check_is_prod(self):
        if self.base_url != PROD_DEFAULT_BASE_URL:
            warnings.warn(
                "FusedAPI is connected to non-production", FusedNonProductionWarning
            )

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
        url = f"{self.base_url}/sample_args/map"

        body: Dict[str, Any] = config.model_dump()
        params = request_models.SampleMapRequest(
            file_id=file_id, chunk_id=chunk_id, n_rows=n_rows
        )

        self._check_is_prod()
        r = requests.post(
            url=url,
            params=params.model_dump(),
            json=body,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return zip_to_map_args(r.content, n_rows=n_rows)

    def _whole_file_sample_map(
        self,
        config: MapJobStepConfig,
        *,
        file_id: Union[str, int],
        n_rows: Optional[int] = None,
    ) -> MapInput:
        assert isinstance(config, MapJobStepConfig)
        url = f"{self.base_url}/sample_args/whole_file"

        body: Dict[str, Any] = config.model_dump()
        params = request_models.WholeFileSampleMapRequest(
            file_id=file_id, n_rows=n_rows
        )

        self._check_is_prod()
        r = requests.post(
            url=url,
            params=params.model_dump(),
            json=body,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return zip_to_map_args(r.content, n_rows=n_rows)

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
        url = f"{self.base_url}/table/download/bbox"

        params = request_models.GetTableBboxRequest(
            path=path,
            bbox_minx=minx,
            bbox_miny=miny,
            bbox_maxx=maxx,
            bbox_maxy=maxy,
            n_rows=n_rows,
            columns=columns,
            clip=clip,
            buffer=buffer,
        )

        self._check_is_prod()
        r = requests.get(
            url=url,
            params=params.model_dump(),
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return parquet_to_df(r.content)

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
        url = f"{self.base_url}/sample_args/join"
        body: Dict[str, Any] = config.model_dump()

        params = request_models.SampleJoinRequest(
            file_id=file_id, chunk_id=chunk_id, n_rows=n_rows
        )

        self._check_is_prod()
        r = requests.post(
            url=url,
            params=params.model_dump(),
            json=body,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return zip_to_join_args(r.content, n_rows=n_rows)

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
        url = f"{self.base_url}/sample_args/join_singlefile"
        body: Dict[str, Any] = config.model_dump()

        params = request_models.SampleSingleFileJoinRequest(
            file_id=file_id, chunk_id=chunk_id, n_rows=n_rows
        )

        self._check_is_prod()
        r = requests.post(
            url=url,
            params=params.model_dump(),
            json=body,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return zip_to_join_singlefile_args(r.content, n_rows=n_rows)

    def start_job(
        self,
        config: Union[JobConfig, JobStepConfig],
        *,
        instance_type: Optional[WHITELISTED_INSTANCE_TYPES] = None,
        region: Optional[str] = None,
        disk_size_gb: Optional[int] = None,
        additional_env: Optional[Sequence[str]] = ("FUSED_CREDENTIAL_PROVIDER=ec2",),
        image_name: Optional[str] = None,
    ) -> RunResponse:
        """Execute an operation

        Args:
            config: the configuration object to run in the job.

        Keyword Args:
            instance_type: The AWS EC2 instance type to use for the job. Acceptable strings are "m5.large", "m5.xlarge", "m5.2xlarge", "m5.4xlarge", "m5.8xlarge", "m5.12xlarge", "m5.16xlarge", "r5.large", "r5.xlarge", "r5.2xlarge", "r5.4xlarge", "r5.8xlarge", "r5.12xlarge", or "r5.16xlarge". Defaults to None.
            region: The AWS region in which to run. Defaults to None.
            disk_size_gb: The disk size to specify for the job. Defaults to None.
            additional_env: Any additional environment variables to be passed into the job, each in the form KEY=value. Defaults to None.
            image_name: Custom image name to run. Defaults to None for default image.
        """
        url = f"{self.base_url}/run"

        if isinstance(config, JobStepConfig):
            config = JobConfig(steps=[config])

        body = {"config": config.model_dump()}
        if additional_env:
            body["additional_env"] = additional_env
        if image_name:
            body["image_name"] = image_name

        params = request_models.StartJobRequest(
            region=region,
            instance_type=instance_type,
            disk_size_gb=disk_size_gb,
        )

        self._check_is_prod()
        r = requests.post(
            url=url,
            params=params.model_dump(),
            json=body,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return RunResponse.model_validate_json(r.content)

    def save_udf(
        self,
        udf: AnyBaseUdf,
        slug: Optional[str] = None,
        id: Optional[str] = None,
        allow_public_read: bool = False,
        allow_public_list: bool = False,
    ) -> UdfRegistry:
        url = f"{self.base_url}/udf/by-id/{id}" if id else f"{self.base_url}/udf/new"
        body = request_models.SaveUdfRequest(
            slug=slug,
            udf_body=udf.model_dump_json(),
            allow_public_read=allow_public_read,
            allow_public_list=allow_public_list,
        )

        self._check_is_prod()
        r = requests.post(
            url=url,
            json=body.model_dump(),
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        # TODO: body
        return r.json()

    def delete_saved_udf(self, id: str):
        url = f"{self.base_url}/udf/by-id/{id}"

        self._check_is_prod()
        r = requests.delete(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        # TODO: body
        return r.json()

    def _get_udf(
        self,
        email_or_id: str,
        id: Optional[str] = None,
    ):
        if id is None:
            email_or_id = id
            email_or_id = self._whoami()["email"]

        url = f"{self.base_url}/udf/by-user-email/{email_or_id}/by-slug/{id}"

        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def _get_public_udf(
        self,
        id: str,
    ):
        url = f"{self.base_url}/udf/public/by-slug/{id}"

        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def _get_code_by_url(self, url: str):
        req_url = f"{self.base_url}/code-proxy/by-url"

        r = requests.get(
            url=req_url,
            params={
                "url": url,
            },
            headers=self._generate_headers(credentials_needed=False),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def get_udfs(
        self,
        n: int = 5,
        *,
        skip: int = 0,
        per_request: int = 25,
        max_requests: Optional[int] = 1,
        by: Literal["name", "id", "slug"] = "name",
        whose: Literal["self", "public", "community", "team"] = "self",
    ):
        request_count = 0
        has_content = True
        udfs = []

        assert per_request >= 0

        while has_content:
            if whose == "self":
                url = f"{self.base_url}/udf/self"
            elif whose == "public" or whose == "community":
                url = f"{self.base_url}/udf/public"
            elif whose == "team":
                url = f"{self.base_url}/udf/exec-env/self"
            else:
                raise ValueError(
                    'Invalid value for `whose`, should be one of: "self", "public", "community", "team"'
                )

            params = request_models.ListUdfsRequest(
                skip=skip,
                limit=per_request,
            )
            skip += per_request

            r = requests.get(
                url=url,
                params=params.model_dump(),
                headers=self._generate_headers(),
                timeout=OPTIONS.request_timeout,
            )
            raise_for_status(r)
            udfs_this_request = r.json()
            if udfs_this_request:
                udfs.extend(udfs_this_request)
            else:
                has_content = False

            request_count += 1
            if len(udfs) >= n or (
                max_requests is not None and request_count == max_requests
            ):
                break

        deserialized_udfs = {}
        for udf in udfs:
            if "udf_body" in udf and udf["udf_body"]:
                try:
                    deserialized_udf = RootAnyBaseUdf.model_validate_json(
                        udf["udf_body"]
                    ).root
                    udf_id = (
                        deserialized_udf.name
                        if by == "name"
                        else (
                            udf["id"]
                            if by == "id"
                            else (udf["slug"] if by == "slug" else None)
                        )
                    )

                    # Restore metadata fields if they were not already present
                    if not deserialized_udf._get_metadata_safe(METADATA_FUSED_ID):
                        deserialized_udf._set_metadata_safe(
                            METADATA_FUSED_ID, udf["id"]
                        )
                    if not deserialized_udf._get_metadata_safe(METADATA_FUSED_SLUG):
                        deserialized_udf._set_metadata_safe(
                            METADATA_FUSED_SLUG, udf["slug"]
                        )

                    filtered_public_udf = (
                        whose == "public"
                        and deserialized_udf._get_metadata_safe(
                            METADATA_FUSED_EXPLORER_TAB
                        )
                        == "community"
                    ) or (
                        whose == "community"
                        and deserialized_udf._get_metadata_safe(
                            METADATA_FUSED_EXPLORER_TAB
                        )
                        != "community"
                    )

                    if udf_id is not None and not filtered_public_udf:
                        deserialized_udfs[udf_id] = deserialized_udf
                except Exception as e:
                    warnings.warn(
                        f"UDF {udf['slug']} ({udf['id']}) could not be deserialized: {e}"
                    )
        return UdfRegistry(deserialized_udfs)

    def get_udf_access_tokens(
        self,
        n: Optional[int] = None,
        *,
        skip: int = 0,
        per_request: int = 25,
        max_requests: Optional[int] = 1,
        _whose: Literal["self", "all"] = "self",
    ) -> UdfAccessTokenList:
        request_count = 0
        has_content = True
        tokens = []

        assert per_request >= 0

        while has_content:
            url = f"{self.base_url}/udf-access-token/{_whose}"

            params = request_models.ListUdfAccessTokensRequest(
                skip=skip,
                limit=per_request,
            )
            skip += per_request

            r = requests.get(
                url=url,
                params=params.model_dump(),
                headers=self._generate_headers(),
                timeout=OPTIONS.request_timeout,
            )
            raise_for_status(r)
            tokens_this_request = r.json()
            if tokens_this_request:
                tokens.extend(tokens_this_request)
            else:
                has_content = False

            request_count += 1
            if n is not None and (
                len(tokens) >= n
                or (max_requests is not None and request_count == max_requests)
            ):
                break

        tokens_deserialized = UdfAccessTokenList()
        for token in tokens:
            tokens_deserialized.append(UdfAccessToken.model_validate(token))

        return tokens_deserialized

    def get_udf_access_token(
        self,
        token: Union[str, UdfAccessToken],
    ) -> UdfAccessToken:
        if isinstance(token, UdfAccessToken):
            token = token.token
        url = f"{self.base_url}/udf-access-token/by-token/{token}"

        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return UdfAccessToken.model_validate_json(r.content)

    def delete_udf_access_token(
        self,
        token: Union[str, UdfAccessToken],
    ) -> UdfAccessToken:
        if isinstance(token, UdfAccessToken):
            token = token.token
        url = f"{self.base_url}/udf-access-token/by-token/{token}"

        r = requests.delete(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return UdfAccessToken.model_validate_json(r.content)

    def update_udf_access_token(
        self,
        token: Union[str, UdfAccessToken],
        *,
        client_id: Optional[str] = None,
        cache: Optional[bool] = None,
        metadata_json: Optional[Dict[str, Any]] = None,
        enabled: Optional[bool] = None,
    ) -> UdfAccessToken:
        if isinstance(token, UdfAccessToken):
            token = token.token
        url = f"{self.base_url}/udf-access-token/by-token/{token}"

        body = request_models.UpdateUdfAccessTokenRequest(
            client_id=client_id,
            cache=cache,
            metadata_json=metadata_json,
            enabled=enabled,
        ).model_dump()  # type: ignore

        r = requests.post(
            url=url,
            json=body,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return UdfAccessToken.model_validate_json(r.content)

    def create_udf_access_token(
        self,
        udf_email_or_name_or_id: Optional[str] = None,
        /,
        udf_name: Optional[str] = None,
        *,
        udf_email: Optional[str] = None,
        udf_id: Optional[str] = None,
        client_id: Union[str, Ellipsis, None] = ...,
        cache: bool = True,
        metadata_json: Optional[Dict[str, Any]] = None,
        enabled: bool = True,
    ) -> UdfAccessToken:
        """
        Create a token for running a UDF. The token allows anyone who has it to run
        the UDF, with the parameters they choose. The UDF will run under your environment.

        The token does not allow running any other UDF on your account.

        Args:
            udf_email_or_name_or_id: A UDF ID, email address (for use with udf_name), or UDF name.
            udf_name: The name of the UDF to create the

        Keyword Args:
            udf_email: The email of the user owning the UDF, or, if udf_name is None, the name of the UDF.
            udf_id: The backend ID of the UDF to create the token for.
            client_id: If specified, overrides which realtime environment to run the UDF under.
            cache: If True, UDF tiles will be cached.
            metadata_json: Additional metadata to serve as part of the tiles metadata.json.
            enable: If True, the token can be used.
        """
        if udf_id is not None:
            if (
                udf_name is not None
                or udf_email is not None
                or udf_email_or_name_or_id is not None
            ):
                warnings.warn(
                    "All other ways of specifying the UDF are ignored in favor of udf_id.",
                )
                udf_name = None
                udf_email = None
        elif udf_name is not None:
            if udf_email_or_name_or_id is not None:
                if udf_email is not None:
                    warnings.warn(
                        "All other ways of specifying the UDF are ignored in favor of the first argument and udf_name.",
                    )
                udf_email = udf_email_or_name_or_id
        elif udf_email_or_name_or_id is not None:
            if udf_name is not None:
                udf_email = udf_email_or_name_or_id
            else:
                # Need to figure out what exactly the first argument is and how it specifies a UDF
                is_valid_uuid = True
                try:
                    uuid.UUID(udf_email_or_name_or_id)
                except ValueError:
                    is_valid_uuid = False
                if is_valid_uuid:
                    udf_id = udf_email_or_name_or_id
                elif "/" in udf_email_or_name_or_id:
                    udf_email, udf_name = udf_email_or_name_or_id.split("/", maxsplit=1)
                else:
                    udf_name = udf_email_or_name_or_id
                    udf_email = self._whoami()["email"]
        else:
            raise ValueError("No UDF specified to create an access token for.")

        if client_id is Ellipsis:
            client_id = self._automatic_realtime_client_id()

        if client_id is Ellipsis:
            raise ValueError("Failed to detect realtime client ID")

        url = f"{self.base_url}/udf-access-token/new"

        metadata_json = metadata_json or {}

        body = request_models.CreateUdfAccessTokenRequest(
            udf_email=udf_email,
            udf_slug=udf_name,
            udf_id=udf_id,
            client_id=client_id,
            cache=cache,
            metadata_json=metadata_json,
            enabled=enabled,
        ).model_dump()  # type: ignore

        r = requests.post(
            url=url,
            json=body,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return UdfAccessToken.model_validate_json(r.content)

    def get_jobs(
        self,
        n: int = 5,
        *,
        skip: int = 0,
        per_request: int = 25,
        max_requests: Optional[int] = 1,
    ) -> Jobs:
        """Get the job history.

        Args:
            n: The number of jobs to fetch. Defaults to 5.

        Keyword Args:
            skip: Where in the job history to begin. Defaults to 0, which retrieves the most recent job.
            per_request: Number of jobs per request to fetch. Defaults to 25.
            max_requests: Maximum number of requests to make. May be None to fetch all jobs. Defaults to 1.

        Returns:
            The job history.
        """
        request_count = 0
        has_content = True
        jobs = []
        original_skip = skip

        assert per_request >= 0

        while has_content:
            url = f"{self.base_url}/job/self"

            params = request_models.ListJobsRequest(
                skip=skip,
                limit=per_request,
            )
            skip += per_request

            r = requests.get(
                url=url,
                params=params.model_dump(),
                headers=self._generate_headers(),
                timeout=OPTIONS.request_timeout,
            )
            raise_for_status(r)
            jobs_this_request = r.json()
            if jobs_this_request:
                jobs.extend(jobs_this_request)
            else:
                has_content = False

            request_count += 1
            if len(jobs) >= n or (
                max_requests is not None and request_count == max_requests
            ):
                break

        return Jobs(
            jobs=jobs[:n],
            n=n,
            skip=original_skip,
            per_request=per_request,
            max_requests=max_requests,
        )

    def get_job_config(self, job: CoerceableToJobId) -> JobConfig:
        job_id = _object_to_job_id(job)
        url = f"{self.base_url}/job/by-id/{job_id}/config"

        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
            allow_redirects=False,
        )
        raise_for_status(r)

        redirect_location = r.headers["location"]

        r2 = requests.get(
            url=redirect_location,
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r2)

        return JobConfig.model_validate_json(r2.content)

    def get_status(self, job: CoerceableToJobId) -> RunResponse:
        """Fetch the status of a running job

        Args:
            job: the identifier of a job or a `RunResponse` object.

        Returns:
            The status of the given job.
        """
        job_id = _object_to_job_id(job)
        url = f"{self.base_url}/run/by-id/{job_id}"

        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return RunResponse.model_validate_json(r.content)

    def get_logs(
        self,
        job: CoerceableToJobId,
        since_ms: Optional[int] = None,
    ) -> List[Any]:
        """Fetch logs for a job

        Args:
            job: the identifier of a job or a `RunResponse` object.
            since_ms: Timestamp, in milliseconds since epoch, to get logs for. Defaults to None for all logs.

        Returns:
            Log messages for the given job.
        """
        job_id = _object_to_job_id(job)
        url = f"{self.base_url}/logs/{job_id}"
        params = {}
        if since_ms is not None:
            params["since_ms"] = since_ms
        r = requests.get(
            url=url,
            params=params,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def tail_logs(
        self,
        job: CoerceableToJobId,
        refresh_seconds: float = 1,
        sample_logs: bool = True,
        timeout: Optional[float] = None,
        get_logs_retries: int = 1,
    ):
        """Continuously print logs for a job

        Args:
            job: the identifier of a job or a `RunResponse` object.
            refresh_seconds: how frequently, in seconds, to check for new logs. Defaults to 1.
            sample_logs: if true, print out only a sample of logs. Defaults to True.
            timeout: if not None, how long to continue tailing logs for. Defaults to None for indefinite.
            get_logs_retries: Number of additional retries for log requests. Defaults to 1.
        """
        # TODO: Move this to the RunResponse object
        start_time = time.time()
        job = self.get_status(job)
        print(f"Logs for: {job.job_id}")

        def _tail_get_logs(
            job: RunResponse, since_ms: Optional[int] = None
        ) -> List[Any]:
            for _ in range(get_logs_retries + 1):
                try:
                    return self.get_logs(job, since_ms=since_ms)
                except requests.exceptions.RequestException:
                    # TODO: Don't use bare except
                    print("Server did not respond with logs")
                    # TODO: Backoff strategy
                    time.sleep(refresh_seconds)
            raise ValueError("Server did not respond with logs")

        r = _tail_get_logs(job)
        if job.status not in ["running", "pending"]:
            print(f"Job is not running ({job.status})")
            return

        if len(r) == 0:
            print("Configuring packages and waiting for logs...")
            while len(r) == 0:
                time.sleep(refresh_seconds)
                r = _tail_get_logs(job)
                if timeout is not None and time.time() - start_time > timeout:
                    raise TimeoutError("Timed out waiting for logs")

        last_message: Optional[str] = None
        last_since_ms: Optional[int] = None
        while True:
            time.sleep(refresh_seconds)
            r = _tail_get_logs(job, since_ms=last_since_ms)
            # If any results -- there may be none because we are filtering them with since_ms
            if len(r):
                current_message: str = r[-1]["message"]
                if last_message != current_message:
                    # If the most recent log line has changed, print it out
                    last_message = current_message
                    last_since_ms = r[-1]["timestamp"]

                    if sample_logs:
                        print(current_message.rstrip())
                    else:
                        for message in r:
                            print(message["message"].rstrip())

            if "ERROR" in current_message or self.get_status(job).status != "running":
                # Try to detect exit scenarios: an error has occured and the job will stop,
                # or the job is no longer in a running state.
                return

            if timeout is not None and time.time() - start_time > timeout:
                raise TimeoutError("Timed out")

    def wait_for_job(
        self,
        job: CoerceableToJobId,
        poll_interval_seconds: float = 5,
        timeout: Optional[float] = None,
    ) -> RunResponse:
        """Block the Python kernel until the given job has finished

        Args:
            job: the identifier of a job or a `RunResponse` object.
            poll_interval_seconds: How often (in seconds) to poll for status updates. Defaults to 5.
            timeout: The length of time in seconds to wait for the job. Defaults to None.

        Raises:
            TimeoutError: if waiting for the job timed out.

        Returns:
            The status of the given job.
        """
        # TODO: Move this to the RunResponse object
        start_time = time.time()
        status = self.get_status(job)
        while not status.terminal_status:
            time.sleep(poll_interval_seconds)
            status = self.get_status(job)
            if timeout is not None and time.time() - start_time > timeout:
                raise TimeoutError("Timed out waiting for job")
        return status

    def cancel_job(self, job: CoerceableToJobId) -> RunResponse:
        """Cancel an existing job

        Args:
            job: the identifier of a job or a `RunResponse` object.

        Returns:
            A new job object.
        """
        job_id = _object_to_job_id(job)
        url = f"{self.base_url}/run/by-id/{job_id}/cancel"

        self._check_is_prod()
        r = requests.post(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return RunResponse.model_validate_json(r.content)

    def _whoami(self) -> Any:
        """
        Returns information on the currently logged in user
        """
        url = f"{self.base_url}/user/self"

        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def _list_realtime_instances(self, *, whose: str = "self") -> List[Any]:
        """
        Returns information about available realtime instances
        """
        url = f"{self.base_url}/realtime-instance"
        if whose == "self":
            url += "/available"
        else:
            assert whose == "public", "whose must be 'public' or 'self'"

        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def _automatic_realtime_client_id(self) -> Optional[str]:
        client_id = OPTIONS.realtime_client_id
        if client_id is None:
            instances = self._list_realtime_instances()
            if len(instances):
                client_id = instances[0]["client_id"]
            if OPTIONS.save_user_settings and client_id:
                OPTIONS.realtime_client_id = client_id

        return client_id

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
        request = request_models.OpenTableRequest(
            path=path,  # type: ignore
        )
        url = f"{self.base_url}/table/open"
        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            params=request.model_dump(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        table = Table.model_validate(r.json())
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

        request = request_models.OpenDatasetFolderRequest(
            path=path,  # type: ignore
            fetch_minimal_table_metadata=should_fetch_minimal_table_metadata,
            fetch_table_metadata=should_fetch_table_metadata,
            max_depth=max_depth,
        )
        mode_str = "table" if table_mode else "dataset"
        url = f"{self.base_url}/{mode_str}/open_folder"
        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            params=request.model_dump(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        folder = Folder.model_validate(r.json())
        for table in folder.tables:
            post_open_table(
                table=table,
                fetch_samples=fetch_samples,
            )

        return folder

    @overload
    def list(self, path: str, *, details: Literal[True]) -> List[ListDetails]:
        ...

    @overload
    def list(self, path: str, *, details: Literal[False] = False) -> List[str]:
        ...

    def list(self, path: str, *, details: bool = False):
        list_request_url = f"{self.base_url}/files/list{'-details' if details else ''}"
        params = request_models.ListPathRequest(path=path)
        r = requests.get(
            url=list_request_url,
            params=params.model_dump(),
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        result = r.json()
        if details:
            result = [ListDetails.model_validate(detail) for detail in result]
        return result

    def delete(
        self,
        path: str,
        max_deletion_depth: Union[int, Literal["unlimited"]] = 2,
    ) -> bool:
        delete_request_url = f"{self.base_url}/files/delete"

        params = request_models.DeletePathRequest(
            path=path,
            max_deletion_depth=max_deletion_depth,
        )

        r = requests.delete(
            url=delete_request_url,
            params=params.model_dump(),
            json="{}",
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def _resolve(
        self,
        path: str,
    ) -> List[str]:
        resolve_request_url = f"{self.base_url}/files/resolve"

        params = request_models.ResolvePathRequest(
            path=path,
        )

        r = requests.post(
            url=resolve_request_url,
            params=params.model_dump(),
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def get(self, path: str) -> bytes:
        get_request_url = f"{self.base_url}/files/get"
        params = request_models.GetPathRequest(path=path)
        r = requests.get(
            url=get_request_url,
            params=params.model_dump(),
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
            allow_redirects=True,
        )
        raise_for_status(r)
        return r.content

    def download(self, path: str, local_path: Union[str, Path]) -> None:
        get_request_url = f"{self.base_url}/files/get"
        params = request_models.GetPathRequest(path=path)
        r = requests.get(
            url=get_request_url,
            params=params.model_dump(),
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
            allow_redirects=True,
            stream=True,
        )
        raise_for_status(r)
        with open(local_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    def sign_url(self, path: str) -> str:
        sign_request_url = f"{self.base_url}/files/sign"
        params = request_models.SignPathRequest(path=path)
        r = requests.get(
            url=sign_request_url,
            params=params.model_dump(),
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def sign_url_prefix(self, path: str) -> Dict[str, str]:
        sign_prefix_request_url = f"{self.base_url}/files/sign_prefix"
        params = request_models.SignPathRequest(path=path)
        r = requests.get(
            url=sign_prefix_request_url,
            params=params.model_dump(),
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def _get_table_names(self, path: str) -> List[str]:
        list_request_url = f"{self.base_url}/files/list"
        params = request_models.ListPathRequest(path=path)
        r = requests.get(
            url=list_request_url,
            params=params.model_dump(),
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)

        tables: List[str] = []
        for s3_path in r.json():
            table_name = s3_path.rstrip("/").split("/")[-1]
            tables.append(table_name)

        return tables

    def upload(self, path: str, data: Union[bytes, BinaryIO]) -> None:
        """Upload a binary blob to a cloud location"""
        upload_url = f"{self.base_url}/files/upload"
        params = request_models.UploadRequest(path=path)
        r = requests.put(
            url=upload_url,
            params=params.model_dump(),
            headers=self._generate_headers(
                {"Content-Type": "application/octet-stream"}
            ),
            data=data,
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)

    def _upload_tmp(self, extension: str, data: Union[bytes, BinaryIO]) -> str:
        """Upload a binary blob to a temporary cloud location, and return the new URL"""
        upload_temp_url = f"{self.base_url}/files/upload-temp"
        params = request_models.UploadTempRequest(extension=extension)
        r = requests.post(
            url=upload_temp_url,
            params=params.model_dump(),
            headers=self._generate_headers(
                {"Content-Type": "application/octet-stream"}
            ),
            data=data,
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def _replace_df_input(
        self, input: Union[str, List[str], Path, gpd.GeoDataFrame]
    ) -> Union[str, List[str]]:
        """If the input is a DataFrame, upload it and return a URL to it. Otherwise return input unchanged."""
        if isinstance(input, gpd.GeoDataFrame):
            with TemporaryFile() as tmp:
                input.to_parquet(tmp)
                tmp.seek(0, SEEK_SET)
                input = self._upload_tmp(extension="parquet", data=tmp)
        elif isinstance(input, Path):
            with open(input, "rb") as f:
                extension = input.name.rsplit(".", 1)[-1]
                input = self._upload_tmp(extension=extension, data=f)
        return input

    def _health(self) -> bool:
        """Check the health of the API backend"""
        r = requests.get(f"{self.base_url}/health", timeout=OPTIONS.request_timeout)
        raise_for_status(r)
        return True

    def auth_token(self) -> str:
        """
        Returns the current user's Fused environment (team) auth token
        """
        url = f"{self.base_url}/execution-env/token"

        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def _generate_headers(
        self,
        headers: Optional[Dict[str, str]] = None,
        *,
        credentials_needed: bool = True,
    ) -> Dict[str, str]:
        if headers is None:
            headers = {}

        common_headers = {
            "Fused-Py-Version": fused_batch.__version__,
            **headers,
        }

        if AUTHORIZATION.is_configured() or credentials_needed:
            common_headers[
                "Authorization"
            ] = f"{AUTHORIZATION.credentials.auth_scheme} {AUTHORIZATION.credentials.access_token}"

        return common_headers

    @lru_cache
    def dependency_whitelist(self) -> str:
        sign_request_url = f"{self.base_url}/internal/dependency-whitelist"
        r = requests.get(
            url=sign_request_url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()


set_api_class(FusedAPI)
