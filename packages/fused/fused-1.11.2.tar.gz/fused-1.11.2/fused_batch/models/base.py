from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict

from fused_batch._global_api import get_api

if sys.version_info >= (3, 9):
    from importlib.resources import files
else:
    from importlib_resources import files

if TYPE_CHECKING:
    from fused_batch.api import FusedAPI

# Pydantic methods to remove in __dir__
PYDANTIC_METHODS = {
    "Config",
    "construct",
    "copy",
    "from_orm",
    "json",
    "parse_file",
    "parse_obj",
    "schema",
    "schema_json",
    "update_forward_refs",
    "validate",
    "model_config",
    "model_construct",
    "model_copy",
    "model_dump",
    "model_dump_json",
    "model_extra",
    "model_fields",
    "model_fields_set",
    "model_json_schema",
    "model_parametrized_name",
    "model_post_init",
    "model_rebuild",
    "model_validate",
    "model_validate_json",
    "model_validate_strings",
    "parse_raw",
    "model_computed_fields",
}


migration_version = (
    files("fused_batch")
    .joinpath("MIGRATION_VERSION")
    .read_text(encoding="utf-8")
    .strip("\n")
)
if migration_version is None:
    raise ValueError("Migration version not found.")


class FusedBaseModel(BaseModel):
    version: str = migration_version
    # _vobj__migrations: List[Any] = []

    @property
    def _api(self) -> FusedAPI:
        # Note that this does not import the FusedAPI class for circular import reasons
        # We assume that the API has already been instantiated before a model is created
        return get_api()

    def __dir__(self) -> List[str]:
        """Provide method name lookup and completion. Only provide 'public'
        methods.
        """
        # This enables autocompletion.
        normal_dir = {
            name
            for name in dir(type(self))
            if not name.startswith("_") and name not in PYDANTIC_METHODS
        }
        pydantic_fields = set(self.model_fields.keys())

        return sorted(normal_dir | pydantic_fields)

    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    # @model_validator(mode="before")
    # @classmethod
    # def versioning(cls, values):
    #     # Only validate versioning if the class has a _validate_version attribute.
    #     if "version" not in values or not hasattr(cls, "_validate_version"):
    #         return values
    #
    #     if len(cls._vobj__migrations) == 0:
    #         # Class has no migrations.
    #         return values
    #
    #     for version, migration, migration_cls in cls._vobj__migrations:
    #         # Migrate obj from current version through upper range.
    #         if cls == migration_cls:
    #             asset_version = values.get("version")
    #             if not asset_version:
    #                 logger.info(
    #                     "Asset has no version. Assuming it's 0.0.0.",
    #                 )
    #                 asset_version = "0.0.0"
    #             if asset_version < version:
    #                 logger.trace(f"Migrating to version {version}...")
    #                 values = migration(values)
    #                 values["version"] = version
    #                 logger.trace(f"Migration to version {version} complete.")
    #             else:
    #                 logger.trace(
    #                     f"Asset version is {values['version']}. Therefore, skipping migration to version {version}.",
    #                     cls,
    #                 )
    #
    #     return values


UserMetadataType = Optional[Dict[str, Any]]
