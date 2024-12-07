from enum import Enum


class JoinType(str, Enum):
    LEFT = "left"
    INNER = "inner"
