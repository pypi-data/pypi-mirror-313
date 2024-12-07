from typing import Optional, Sequence

from pydantic import BaseModel

from .dataset import Table


class Folder(BaseModel):
    base_path: Optional[str] = None
    tables: Sequence[Table]
    folders: Sequence[str] = ()
