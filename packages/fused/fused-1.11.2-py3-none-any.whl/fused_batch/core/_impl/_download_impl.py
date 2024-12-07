from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from typing import List
from urllib.parse import ParseResult, urlparse

import fsspec
import requests
from fsspec.implementations.dirfs import DirFileSystem
from loguru import logger

from fused_batch._global_api import get_api
from fused_batch._options import options as OPTIONS


def data_path() -> str:
    return "/tmp/fused"


def filesystem(protocol: str, **storage_options) -> fsspec.AbstractFileSystem:
    if protocol == "fd":
        # fused team directory
        api = get_api()
        if hasattr(api, "_resolve"):
            root = api._resolve("fd://")
            root_parsed = urlparse(root)
            return DirFileSystem(
                path=root, fs=fsspec.filesystem(root_parsed.scheme, **storage_options)
            )
        else:
            raise ValueError("Could not determine root of Fused team directory")
    return fsspec.filesystem(protocol, **storage_options)


def _download_requests(url: str) -> bytes:
    # this function is shared
    response = requests.get(url, headers={"User-Agent": ""})
    response.raise_for_status()
    return response.content


def _download_signed(url: str) -> bytes:
    api = get_api()
    return _download_requests(api.sign_url(url))


def _download_s3(url: str) -> bytes:
    try:
        return _download_signed(url)
    except:  # noqa E722
        s3 = filesystem("s3")
        with s3.open(url, "rb") as f:
            return f.read()


def _download_gcs(url: str) -> bytes:
    try:
        return _download_signed(url)
    except:  # noqa E722
        gcs = filesystem("gs")
        with gcs.open(url, "rb") as f:
            return f.read()


def download_folder_inner(parsed_url: ParseResult, url: str, path: str):
    if parsed_url.scheme in ["s3", "gs"]:
        api = get_api()
        all_files = api.sign_url_prefix(url)

        root_path = Path(path)
        to_remove = parsed_url.path.lstrip("/")

        def _download_single_file(filename: str, signed_url: str) -> None:
            logger.debug(f"Downloading {filename}...")
            content = _download_requests(signed_url)

            curr_path = root_path / Path(filename)
            curr_path.parent.mkdir(parents=True, exist_ok=True)

            with open(curr_path, "wb") as file:
                file.write(content)

        with ThreadPoolExecutor(max_workers=OPTIONS.max_workers) as pool:
            futures: List[Future] = []
            for filename, signed_url in all_files.items():
                if filename.startswith(to_remove):
                    filename = filename[len(to_remove) :]

                futures.append(
                    pool.submit(
                        _download_single_file,
                        filename=filename,
                        signed_url=signed_url,
                    )
                )
            pool.shutdown(wait=True)
    else:
        raise NotImplementedError(f"Unexpected URL scheme {parsed_url.scheme}")
