"""LoggerMan"""
from __future__ import annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

import mdit as _mdit

from loggerman import style
from loggerman.logger import Logger, LogLevel


if _TYPE_CHECKING:
    from typing import Type, Sequence, Callable
    from mdit.protocol import TargetConfig, ANSITargetConfig
    from loggerman.style import LogLevelStyle


logger = Logger()


def create(
    realtime_levels: Sequence[str | int | LogLevel] | None = None,
    console_config: _mdit.target.rich.ConsoleConfig | dict = _mdit.target.rich.ConsoleConfig(),
    github: bool | None = None,
    github_debug: bool = True,
    title_number: int | Sequence[int] = 1,
    exception_handler: dict[Type[Exception], Callable] | None = None,
    exit_code_critical: int | None = None,
    target_configs_md: dict[str, _mdit.MDTargetConfig | dict] | None = None,
    target_configs_rich: dict[str, _mdit.RichTargetConfig | dict] | None = None,
    target_default_md: str = "sphinx",
    target_default_rich: str = "console",
    list_entries: bool = True,
    current_list_key: str = "",
    level_style_debug: LogLevelStyle = style.log_level(
        color="muted",
        icon="🔘",
        rich_config=_mdit.target.rich.PanelConfig(
            title_style=_mdit.target.rich.StyleConfig(color="#fff", bgcolor="#6c757d", bold=True),
        ),

    ),
    level_style_success: LogLevelStyle = style.log_level(
        color="success",
        icon="✅",
        rich_config=_mdit.target.rich.PanelConfig(
            title_style=_mdit.target.rich.StyleConfig(color="#fff", bgcolor="#28a745", bold=True),
        ),
    ),
    level_style_info: LogLevelStyle = style.log_level(
        color="info",
        icon="ℹ️",
        rich_config=_mdit.target.rich.PanelConfig(
            title_style=_mdit.target.rich.StyleConfig(color="#fff", bgcolor="#17a2b8", bold=True),
        ),
    ),
    level_style_notice: LogLevelStyle = style.log_level(
        color="warning",
        icon="❗",
        rich_config=_mdit.target.rich.PanelConfig(
            title_style=_mdit.target.rich.StyleConfig(color="#fff", bgcolor="#f0b37e", bold=True),
        ),
    ),
    level_style_warning: LogLevelStyle = style.log_level(
        color="warning",
        icon="🚨",
        rich_config=_mdit.target.rich.PanelConfig(
            title_style=_mdit.target.rich.StyleConfig(color="#fff", bgcolor="#f0b37e", bold=True),
        ),
    ),
    level_style_error: LogLevelStyle = style.log_level(
        color="danger",
        icon="🚫",
        rich_config=_mdit.target.rich.PanelConfig(
            title_style=_mdit.target.rich.StyleConfig(color="#fff", bgcolor="#dc3545", bold=True),
        ),
    ),
    level_style_critical: LogLevelStyle = style.log_level(
        color="danger",
        opened=True,
        icon="⛔",
        rich_config=_mdit.target.rich.PanelConfig(
            title_style=_mdit.target.rich.StyleConfig(color="#fff", bgcolor="#dc3545", bold=True),
        ),
    ),
    prefix_caller_name: str = "🔔 ",
    prefix_time: str = "⏰ ",
) -> Logger:
    return Logger().initialize(**locals())
