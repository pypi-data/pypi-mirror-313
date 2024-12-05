from __future__ import annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING, Literal as _Literal

import pydantic as _pydantic

from mdit.target.rich import PanelConfig as _PanelConfig


class LogLevelStyle(_pydantic.BaseModel):
    rich_config: _PanelConfig
    opened: bool
    color: _Literal["primary", "secondary", "success", "danger", "warning", "info", "light", "dark", "muted"]
    icon: str
    octicon: str | None = None
    chevron: _Literal["right-down", "down-up"] | None = None,
    animate: _Literal["fade-in", "fade-in-slide-down"] | None = None,
    margin: _Literal["auto", 0, 1, 2, 3, 4, 5] | tuple[_Literal["auto", 0, 1, 2, 3, 4, 5], ...] | None = None,
    classes_container: list[str] = []
    classes_title: list[str] = []
    classes_body: list[str] = []
    signature: list[_Literal["caller_name", "time"]] = []



def log_level(
    rich_config: _PanelConfig,
    opened: bool = False,
    color: _Literal["primary", "secondary", "success", "danger", "warning", "info", "light", "dark", "muted"] = "primary",
    icon: str = "",
    octicon: str | None = None,
    classes_container: list[str] | None = None,
    classes_title: list[str] | None = None,
    classes_body: list[str] | None = None,
    signature: tuple[_Literal["caller_name", "time"]] | None = ("time", "caller_name"),

) -> LogLevelStyle:
    return LogLevelStyle(
        rich_config=rich_config,
        opened=opened,
        color=color,
        icon=icon,
        octicon=octicon,
        classes_container=classes_container or [],
        classes_title=classes_title or [],
        classes_body=classes_body or [],
        signature=signature or [],
    )