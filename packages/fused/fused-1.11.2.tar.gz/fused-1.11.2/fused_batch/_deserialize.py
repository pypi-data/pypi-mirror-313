"""
This module is responsible for creating sample UDF contexts for each algorithm (join, map, etc) for development purposes.
"""
from enum import Enum
from io import BytesIO
from typing import Dict, List, Literal, Optional
from zipfile import ZipFile

import geopandas as gpd
import pandas as pd
import pyarrow.parquet as pq
from pydantic import BaseModel

from fused_batch.models import JoinInput, JoinSingleFileInput, MapInput
from fused_batch.models.api import AnyJobStepConfig
from fused_batch.models.udf import Chunk, ChunkMetadata, Chunks


class ArgsType(str, Enum):
    MAP = "map"
    JOIN = "join"
    JOIN_SINGLEFILE = "join_singlefile"


class ArgsMetadata(BaseModel):
    args_version: Literal["1"] = "1"
    args_type: ArgsType
    step_config: AnyJobStepConfig


def extract_sidecar_inputs(zf: ZipFile, prefix: str) -> Dict[str, bytes]:
    prefix = prefix.rstrip("/")
    sidecar_input_buffers: Dict[str, bytes] = {}
    sidecar_input_paths = [
        info for info in zf.filelist if info.filename.startswith(prefix)
    ]
    for sidecar_input in sidecar_input_paths:
        table_name = sidecar_input.filename.split("/")[-1]
        sidecar_input_buffers[table_name] = zf.read(sidecar_input)

    return sidecar_input_buffers


def extract_chunk(zf: ZipFile, prefix: str, *, n_rows: Optional[int] = None) -> Chunk:
    prefix = prefix.rstrip("/")
    with zf.open(f"{prefix}/data") as f:
        metadata = pq.read_metadata(f)
        if b"geo" in metadata.metadata:
            data = gpd.read_parquet(f)
        else:
            data = pd.read_parquet(f)

    data = data[:n_rows]

    metadata = ChunkMetadata.model_validate_json(
        zf.read(f"{prefix}/row_group_metadata")
    )
    sidecar_inputs = extract_sidecar_inputs(zf, f"{prefix}/sidecar_inputs")

    return Chunk(data=data, metadata=metadata, sidecar=sidecar_inputs)


def zip_to_map_args(buffer: bytes, *, n_rows: Optional[int] = None) -> MapInput:
    with BytesIO(buffer) as bio, ZipFile(bio, mode="r") as zf:
        args_metadata = ArgsMetadata.model_validate_json(zf.read("fused_args/metadata"))
        assert args_metadata.args_version == "1"
        assert args_metadata.args_type == ArgsType.MAP

        chunk = extract_chunk(zf, "map", n_rows=n_rows)
        return MapInput(
            step_config=args_metadata.step_config,
            data=chunk.data,
            metadata=chunk.metadata,
            sidecar=chunk.sidecar,
        )


def zip_to_join_args(buffer: bytes, *, n_rows: Optional[int] = None) -> JoinInput:
    with BytesIO(buffer) as bio, ZipFile(bio, mode="r") as zf:
        args_metadata = ArgsMetadata.model_validate_json(zf.read("fused_args/metadata"))
        assert args_metadata.args_version == "1"
        assert args_metadata.args_type == ArgsType.JOIN

        left_chunk = extract_chunk(zf, "join", n_rows=n_rows)

        num_rights = int(zf.read("join/num_rights").decode("utf-8"))
        right_chunks: List[Chunk] = []
        for i in range(num_rights):
            prefix = f"join/right/{i}"
            right_chunk = extract_chunk(zf, prefix)
            right_chunks.append(right_chunk)

        return JoinInput(
            step_config=args_metadata.step_config,
            left=left_chunk,
            right=Chunks.from_list(right_chunks),
        )


def zip_to_join_singlefile_args(
    buffer: bytes, *, n_rows: Optional[int] = None
) -> JoinSingleFileInput:
    with BytesIO(buffer) as bio, ZipFile(bio, mode="r") as zf:
        args_metadata = ArgsMetadata.model_validate_json(zf.read("fused_args/metadata"))
        assert args_metadata.args_version == "1"
        assert args_metadata.args_type == ArgsType.JOIN_SINGLEFILE

        left_chunk = extract_chunk(zf, "join", n_rows=n_rows)

        with zf.open("join/right/data") as f:
            metadata = pq.read_metadata(f)
            if b"geo" in metadata.metadata:
                right_data = gpd.read_parquet(f)
            else:
                right_data = pd.read_parquet(f)

        return JoinSingleFileInput(
            step_config=args_metadata.step_config, left=left_chunk, right=right_data
        )
