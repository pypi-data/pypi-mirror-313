from __future__ import annotations as _annotations

from typing import TypeAlias, Mapping, Sequence


Serializable: TypeAlias = (
    Mapping[str, "Serializable"]
    | Sequence["Serializable"]
    | str | int | float | bool | None
)
