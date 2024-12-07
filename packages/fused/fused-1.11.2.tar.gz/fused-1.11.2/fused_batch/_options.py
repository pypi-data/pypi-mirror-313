import warnings
from operator import attrgetter
from pathlib import Path
from typing import Any, List, Optional, Tuple, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictStr,
    field_validator,
)

from ._global_api import reset_api
from .warnings import FusedIgnoredWarning, FusedImportWarning

DEV_DEFAULT_BASE_URL = "http://localhost:8783/v1"
PROD_DEFAULT_BASE_URL = "https://www.fused.io/server/v1"
PREVIEW_DEFAULT_BASE_URL = "https://www-preview.fused.io/server/v1"
STAGING_DEFAULT_BASE_URL = "https://www-staging.fused.io/server/v1"


OPTIONS_PATH = Path("~/.fused/settings.toml").expanduser()


class OptionsBaseModel(BaseModel):
    def __dir__(self) -> List[str]:
        # Provide method name lookup and completion. Only provide 'public'
        # methods.
        # This enables autocompletion
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
            "model_validate",
            "model_dump_json",
        }

        normal_dir = {
            name
            for name in dir(type(self))
            if (not name.startswith("_") and name not in PYDANTIC_METHODS)
        }
        pydantic_fields = set(self.model_fields.keys())
        return sorted(normal_dir | pydantic_fields)

    def _repr_html_(self) -> str:
        # Circular import because the repr needs the options
        from fused_batch._formatter.formatter_options import fused_options_repr

        return fused_options_repr(self)


class OpenOptions(OptionsBaseModel):
    """Options for opening tables and projects."""

    fetch_samples: Optional[StrictBool] = None
    """Whether to automatically fetch samples when opening tables"""

    fetch_table_metadata: Optional[StrictBool] = True
    """Whether to automatically fetch table metadata when opening projects"""

    fetch_minimal_table_metadata: Optional[StrictBool] = True
    """Whether to fetch only a minimal set of table metadata when opening projects"""

    auto_refresh_project: StrictBool = True
    """Automatically refresh project objects when accessing a key that is not present locally"""


class ShowOptions(OptionsBaseModel):
    """Options for showing debug information"""

    open_browser: Optional[StrictBool] = None
    """Whether to open a local browser window for debug information"""
    show_widget: Optional[StrictBool] = None
    """Whether to show debug information in an IPython widget"""

    format_numbers: Optional[StrictBool] = None
    """Whether to format numbers in object reprs"""

    materialize_virtual_folders: StrictBool = True
    """Whether to automatically materialize virtual project folders in reprs"""


class CacheOptions(OptionsBaseModel):
    """Options for caching samples"""

    enable: StrictBool = True
    """Whether to enable caching"""


class Options(OptionsBaseModel):
    base_url: str = PROD_DEFAULT_BASE_URL
    """Fused API endpoint"""

    open: OpenOptions = Field(default_factory=OpenOptions)
    """Options for `fused.open_table` and `fused.open_project`."""
    show: ShowOptions = Field(default_factory=ShowOptions)
    """Options for object reprs and how data are shown for debugging."""
    cache: CacheOptions = Field(default_factory=CacheOptions)
    """Options for caching data fused-py can retrieve, such as
    the sample for `run_local`."""

    max_workers: int = 16
    """Maximum number of threads, when multithreading requests"""

    request_timeout: Union[Tuple[float, float], float, None] = 120
    """Request timeout for the Fused service

    May be set to a tuple of connection timeout and read timeout"""

    realtime_client_id: Optional[StrictStr] = None
    """Client ID for realtime service."""

    save_user_settings: StrictBool = True
    """Save per-user settings such as credentials and environment IDs."""

    default_udf_run_engine: Optional[StrictStr] = None
    """Default engine to run UDFs, one of: `local`, `realtime`, `batch`."""

    default_validate_imports: StrictBool = False
    """Default for whether to validate imports in UDFs before `run_local`,
    `run_batch`."""

    prompt_to_login: StrictBool = False
    """Automatically prompt the user to login when importing Fused."""

    @field_validator("base_url")
    @classmethod
    def _validate_base_url(cls, v):
        reset_api()
        return v

    def save(self):
        """Save Fused options to `~/.fused/settings.toml`. They will be automatically
        reloaded the next time fused-py is imported.
        """
        try:
            import rtoml

            OPTIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
            # None (null) will not be serialized correctly in toml, so exclude it.
            # Any option which can be None should be None by default. Some open options
            # don't do this; should be updated to not be Optional.
            rtoml.dump(self.dict(exclude_none=True), OPTIONS_PATH)
        except ImportError:
            warnings.warn(
                "rtoml is not installed so options are not saved", FusedImportWarning
            )

    def _to_toml(self) -> str:
        try:
            import rtoml

            return rtoml.dumps(self.dict(exclude_none=True))
        except ImportError:
            warnings.warn(
                "rtoml is not installed so options are not saved", FusedImportWarning
            )

    model_config = ConfigDict(validate_assignment=True)


def _load_options():
    if OPTIONS_PATH.exists():
        try:
            import rtoml

            return Options.model_validate(rtoml.load(OPTIONS_PATH))
        except:  # noqa E722
            warnings.warn(
                f"Settings file {OPTIONS_PATH} exists but could not be loaded.",
                FusedIgnoredWarning,
            )

    return Options()


options = _load_options()
"""List global configuration options.

This object contains a set of configuration options that control global behavior of the library. This object can be used to modify the options.

Examples:
    Change the `request_timeout` option from its default value to 120 seconds:
    ```py
    fused.options.request_timeout = 120
    ```
"""


def set_option(option_name: str, option_value: Any):
    """
    Sets the value of a configuration option.

    This function updates the global `options` object with a new value for a specified option.
    It supports setting values for nested options using dot notation. For example, if the
    `options` object has a nested structure, you can set a value for a nested attribute
    by specifying the option name in the form "parent.child".

    Args:
        option_name: A string specifying the name of the option to set. This can be a simple
                     attribute name or a dot-separated path for nested attributes.
        option_value: The new value to set for the specified option. This can be of any type
                      that is compatible with the attribute being set.

    Raises:
        AttributeError: If the specified attribute path is not valid, either because a part
                        of the path does not exist or the final attribute cannot be set with
                        the provided value.

    Examples:
        Set the `request_timeout` top-level option to 120 seconds:
        ```python
        set_option('request_timeout', 120)
        ```


    """
    # Set a recursive option name
    # From https://stackoverflow.com/a/65355793 and comments
    if "." in option_name:
        split = option_name.split(".")
        parent = ".".join(split[:-1])
        base_name = split[-1]
        setattr(attrgetter(parent)(options), base_name, option_value)
        return

    setattr(options, option_name, option_value)


def _env(environment_name: str):
    """Set the environment."""
    if environment_name == "dev":
        _env = DEV_DEFAULT_BASE_URL
    elif environment_name == "stg":
        _env = STAGING_DEFAULT_BASE_URL
    elif environment_name == "prod":
        _env = PROD_DEFAULT_BASE_URL
    elif environment_name == "pre":
        _env = PREVIEW_DEFAULT_BASE_URL
    else:
        raise ValueError("Available options are `dev`, `stg`, `prod`, and `pre`.")

    setattr(options, "base_url", _env)
