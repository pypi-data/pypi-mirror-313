from typing import Optional

from pydantic import BaseModel, PrivateAttr, StrictStr


class FusedProjectAware(BaseModel):
    _project_url: Optional[StrictStr] = PrivateAttr()
    """Project base path that table names will be resolved relative to"""
