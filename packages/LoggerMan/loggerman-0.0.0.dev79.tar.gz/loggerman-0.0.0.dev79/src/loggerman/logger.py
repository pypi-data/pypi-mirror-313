from __future__ import annotations

from enum import Enum as _Enum
import datetime as _datetime
from typing import NamedTuple as _NamedTuple, Sequence as _Sequence, TYPE_CHECKING as _TYPE_CHECKING
import inspect as _inspect
import sys as _sys
import traceback as _traceback
from functools import wraps as _wraps, partial as _partial
from pathlib import Path as _Path
from contextlib import contextmanager as _contextmanager

import actionman as _actionman
import mdit as _mdit
from exceptionman import Traceback as _Traceback
import pyserials as _ps
import rich
import rich.traceback
import rich._inspect
import rich.pretty
import rich.panel
import rich.box
import rich.markdown
import rich.text

from loggerman import style as _style


if _TYPE_CHECKING:
    from types import ModuleType, TracebackType
    from typing import Literal, Sequence, Callable, Type, Iterable, Any
    from protocolman import Stringable
    from mdit.protocol import MDTargetConfig, RichTargetConfig, ContainerContentInputType
    from mdit import MDContainer
    from loggerman.style import LogLevelStyle
    from loggerman.protocol import Serializable


class LogLevel(_Enum):
    DEBUG = 0
    SUCCESS = 1
    INFO = 2
    NOTICE = 3
    WARNING = 4
    ERROR = 5
    CRITICAL = 6

class _LogLevelData(_NamedTuple):
    level: LogLevel
    style: LogLevelStyle


class Logger:

    def __init__(self):
        self._doc: _mdit.Document | None = None
        self._initialized: bool = False
        self._realtime_levels: list = []
        self._github: bool = False
        self._github_debug: bool = True
        self._next_section_num: list[int] = []
        self._default_exit_code: int | None = None
        self._exception_handler: dict[Type[Exception], Callable | tuple[Callable, dict[str, Any]]] | None = None
        self._level: dict[str, _LogLevelData] = {}
        self._out_of_section: bool = True
        self._target_configs_md: dict[str, _mdit.MDTargetConfig | dict] | None = None
        self._target_configs_rich: dict[str, _mdit.RichTargetConfig | dict] | None = None
        self._target_default_md: str = ""
        self._target_default_rich: str = ""
        self._console: rich.console.Console | None = None
        self._list_entries: bool = True
        self._curr_list_key: str | None = None
        self._prefix_caller_name: str = ""
        self._prefix_time: str = ""
        self._actionman_logger: _actionman.log.Logger | None = None
        return

    @property
    def report(self) -> _mdit.Document:
        return self._doc

    def initialize(
        self,
        realtime_levels: Sequence[str | int | LogLevel] | None = None,
        console_config: _mdit.target.rich.ConsoleConfig | dict | None = None,
        github: bool | None = None,
        github_debug: bool = True,
        title_number: int | _Sequence[int] = 1,
        exception_handler: dict[Type[Exception], Callable | tuple[Callable, dict[str, Any]]] | None = None,
        exit_code_critical: int | None = None,
        target_configs_md: dict[str, _mdit.MDTargetConfig | dict] | None = None,
        target_configs_rich: dict[str, _mdit.RichTargetConfig | dict] | None = None,
        target_default_md: str = "sphinx",
        target_default_rich: str = "console",
        list_entries: bool = True,
        current_list_key: str | None = None,
        level_style_debug: LogLevelStyle = _style.log_level(
            color="muted",
            icon="🔘",
            rich_config=_mdit.target.rich.PanelConfig(
                title_style=_mdit.target.rich.StyleConfig(color="#fff", bgcolor=(103, 115, 132), bold=True),
            ),

        ),
        level_style_success: LogLevelStyle = _style.log_level(
            color="success",
            icon="✅",
            rich_config=_mdit.target.rich.PanelConfig(
                title_style=_mdit.target.rich.StyleConfig(color="#fff", bgcolor=(0, 47, 23), bold=True),
            ),
        ),
        level_style_info: LogLevelStyle = _style.log_level(
            color="info",
            icon="ℹ️",
            rich_config=_mdit.target.rich.PanelConfig(
                title_style=_mdit.target.rich.StyleConfig(color="#fff", bgcolor=(6, 36, 93), bold=True),
            ),
        ),
        level_style_notice: LogLevelStyle = _style.log_level(
            color="warning",
            icon="❗",
            rich_config=_mdit.target.rich.PanelConfig(
                title_style=_mdit.target.rich.StyleConfig(color="#fff", bgcolor=(101, 42, 2), bold=True),
            ),
        ),
        level_style_warning: LogLevelStyle = _style.log_level(
            color="warning",
            icon="🚨",
            rich_config=_mdit.target.rich.PanelConfig(
                title_style=_mdit.target.rich.StyleConfig(color="#fff", bgcolor=(101, 42, 2), bold=True),
            ),
        ),
        level_style_error: LogLevelStyle = _style.log_level(
            color="danger",
            icon="🚫",
            rich_config=_mdit.target.rich.PanelConfig(
                title_style=_mdit.target.rich.StyleConfig(color="#fff", bgcolor=(78, 17, 27), bold=True),
            ),
        ),
        level_style_critical: LogLevelStyle = _style.log_level(
            color="danger",
            opened=True,
            icon="⛔",
            rich_config=_mdit.target.rich.PanelConfig(
                title_style=_mdit.target.rich.StyleConfig(color="#fff", bgcolor=(78, 17, 27), bold=True),
            ),
        ),
        prefix_caller_name: str = "🔔 ",
        prefix_time: str = "⏰ ",
    ):
        def process_exit_code():
            error_msg_exit_code = (
                "Argument `exit_code_on_error` must be a positive integer or None, "
                f"but got '{exit_code_critical}' (type: {type(exit_code_critical)})."
            )
            if isinstance(exit_code_critical, int):
                if exit_code_critical <= 0:
                    raise ValueError(error_msg_exit_code)
            elif exit_code_critical is not None:
                raise TypeError(error_msg_exit_code)
            self._default_exit_code = exit_code_critical
            return

        if self._initialized:
            return
        if realtime_levels:
            for level in realtime_levels:
                self._realtime_levels.append(self._get_level_name(level))
        self._github_debug = github_debug
        self._next_section_num = list(title_number) if isinstance(title_number, _Sequence) else [1] * title_number
        self._exception_handler = exception_handler or {}
        process_exit_code()
        self._level = {
            "debug": _LogLevelData(level=LogLevel.DEBUG, style=level_style_debug),
            "success": _LogLevelData(level=LogLevel.SUCCESS, style=level_style_success),
            "info": _LogLevelData(level=LogLevel.INFO, style=level_style_info),
            "notice": _LogLevelData(level=LogLevel.NOTICE, style=level_style_notice),
            "warning": _LogLevelData(level=LogLevel.WARNING, style=level_style_warning),
            "error": _LogLevelData(level=LogLevel.ERROR, style=level_style_error),
            "critical": _LogLevelData(level=LogLevel.CRITICAL, style=level_style_critical),
        }
        self._target_configs_md = target_configs_md
        self._target_configs_rich = target_configs_rich or {"console": _mdit.target.console()}
        self._target_default_md = target_default_md
        self._target_default_rich = target_default_rich
        in_github = github if github is not None else _actionman.in_gha()
        self._github = in_github
        if console_config is None:
            console_config = _mdit.target.rich.ConsoleConfig(
                color_system="truecolor" if in_github else "auto",
                force_terminal=True if in_github else None,
                width=88 if in_github else None,
            )
        elif isinstance(console_config, dict):
            console_config = _mdit.target.rich.ConsoleConfig(**console_config)
        self._console = console_config.make(
            force_terminal=True if in_github else console_config.force_terminal
        )
        self._actionman_logger = _actionman.log.Logger(console=self._console)
        self._list_entries = list_entries
        self._curr_list_key = current_list_key
        self._prefix_caller_name = prefix_caller_name
        self._prefix_time = prefix_time
        self._initialized = True
        return self

    @staticmethod
    def traceback(
        trace: tuple[Type[BaseException], BaseException, TracebackType] | None = None,
        code_width: int = 88,
        extra_lines: int = 3,
        theme: str | None = None,
        word_wrap: bool = False,
        show_locals: bool = False,
        indent_guides: bool = True,
        locals_max_length: int = 10,
        locals_max_string: int = 80,
        locals_hide_dunder: bool = True,
        locals_hide_sunder: bool = False,
        suppress: Iterable[str | ModuleType] = (),
        max_frames: int = 100,
    ):
        if trace is None:
            exc_type, exc_value, traceback = _sys.exc_info()
            if exc_type is None or exc_value is None or traceback is None:
                return
        else:
            exc_type, exc_value, traceback = trace
        rich_traceback = _Traceback(
            _Traceback.extract(exc_type, exc_value, traceback, show_locals=show_locals),
            code_width=code_width,
            extra_lines=extra_lines,
            theme=theme,
            word_wrap=word_wrap,
            show_locals=show_locals,
            indent_guides=indent_guides,
            locals_max_length=locals_max_length,
            locals_max_string=locals_max_string,
            locals_hide_dunder=locals_hide_dunder,
            locals_hide_sunder=locals_hide_sunder,
            suppress=suppress,
            max_frames=max_frames,
        )
        return _mdit.element.rich(rich_traceback)

    @staticmethod
    def inspect(
        obj: object,
        title: str | None = None,
        show_value: bool = True,
        show_sunder: bool = False,
        show_dunder: bool = False,
        show_methods: bool = False,
        show_help: bool = False,
        show_docs: bool = False,
        sort: bool = True,
    ):
        rich_inspect = rich._inspect.Inspect(
            obj,
            title=title,
            methods=show_methods,
            help=show_help,
            docs=show_docs,
            private=show_sunder,
            dunder=show_dunder,
            sort=sort,
            value=show_value,
        )
        return _mdit.element.rich(rich_inspect)

    @staticmethod
    def pretty(
        obj: object,
        title: str | None = None,
        footer: str | None = None,
        highlighter: rich.console.HighlighterType | None = None,
        indent_size: int = 4,
        justify: rich.console.JustifyMethod | None = None,
        overflow: rich.console.OverflowMethod | None = None,
        no_wrap: bool = False,
        indent_guides: bool = True,
        max_length: int | None = None,
        max_string: int | None = None,
        max_depth: int | None = None,
        expand_all: bool = False,
        margin: int = 0,
        insert_line: bool = False,
        box: rich.box.Box = rich.box.ROUNDED,
        expand: bool = True,
        title_align: Literal["left", "center", "right"] = "left",
        footer_align: Literal["left", "center", "right"] = "right",
        safe_box: bool = True,
    ):
        rich_pretty = rich.pretty.Pretty(
            obj,
            highlighter=highlighter,
            indent_size=indent_size,
            justify=justify,
            overflow=overflow,
            no_wrap=no_wrap,
            indent_guides=indent_guides,
            max_length=max_length,
            max_string=max_string,
            max_depth=max_depth,
            expand_all=expand_all,
            margin=margin,
            insert_line=insert_line,
        )
        panel = rich.panel.Panel(
            rich_pretty,
            title=title,
            subtitle=footer,
            box=box,
            expand=expand,
            title_align=title_align,
            subtitle_align=footer_align,
            safe_box=safe_box,
        )
        return _mdit.element.rich(panel)

    @staticmethod
    def data_block(
        data: Serializable,
        output: Literal["yaml", "json", "toml"] = "yaml",
        caption: Stringable | None = None,
        line_num: bool = False,
        line_num_start: int | None = None,
        emphasize_lines: list[int] | None = None,
        indent: int = 4,
        sort_keys: bool = False,
    ):
        str_writer = {
            "yaml": _ps.write.to_yaml_string,
            "json": _partial(_ps.write.to_json_string, sort_keys=sort_keys, indent=indent),
            "toml": _partial(_ps.write.to_toml_string, sort_keys=sort_keys),
        }[output]
        return _mdit.element.code_block(
            str_writer(data),
            language=output,
            caption=caption,
            line_num=line_num,
            line_num_start=line_num_start,
            emphasize_lines=emphasize_lines,
        )

    def sectioner(
        self,
        title: ContainerContentInputType = None,
        key: str | None = None,
        conditions: str | list[str] | None = None,
        handler: dict[Type[Exception], Callable | tuple[Callable, dict[str, Any]]] | None = None,
    ):
        """Decorator for sectioning a function or method."""
        def section_decorator(func: Callable):
            @_wraps(func)
            def section_wrapper(*args, **kwargs):
                if title:
                    self.section(title=title, key=key, conditions=conditions)
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    return exception_handler(handler, e, func, args, kwargs)
                else:
                    if title:
                        self.section_end()
                    return result
            return section_wrapper

        def exception_handler(section_handler, e, func, args, kwargs):
            for handler_dict in (section_handler, self._exception_handler):
                for exc_type, handler_specs in handler_dict.items():
                    if isinstance(e, exc_type):
                        if isinstance(handler_specs, (list, tuple)):
                            exc_handler, handler_kwargs = handler_specs
                        else:
                            exc_handler = handler_specs
                            handler_kwargs = {}
                        to_raise, return_val = exc_handler(self, e, func, args, kwargs, **handler_kwargs)
                        if to_raise:
                            raise to_raise
                        return return_val
            raise e

        handler = handler or {}
        return section_decorator

    @_contextmanager
    def sectioning(
        self,
        title: ContainerContentInputType,
        key: str | None = None,
        conditions: str | list[str] | None = None,
    ):
        self.section(title=title, key=key, conditions=conditions)
        yield
        self.section_end()
        return

    def section(
        self,
        title: ContainerContentInputType,
        key: str | None = None,
        conditions: str | list[str] | None = None,
    ):
        if not self._initialized:
            self.initialize()
        heading_configs = self._target_configs_rich[self._target_default_rich].heading
        heading = _mdit.element.heading(
            title,
            level=self._next_section_num,
            explicit_number=True,
            config_rich=heading_configs[min(len(self._next_section_num), len(heading_configs)) - 1]
        )
        if self._realtime_levels:
            self._print(heading.source(target="console"))
        if not self._doc:
            self._doc = _mdit.document(
                heading=heading,
                target_configs_md=self._target_configs_md,
                target_configs_rich=self._target_configs_rich,
            )
            for level_name, log_level in self._level.items():
                self._doc.target_configs["console"].dropdown_class[level_name] = log_level.style.rich_config
        else:
            self._doc.open_section(heading=heading, key=key, conditions=conditions)
        self._curr_list_key = None
        self._out_of_section = False
        self._next_section_num.append(1)
        return

    @property
    def current_section_level(self) -> int:
        return self._doc.current_section_level

    def section_end(self, target_level: int | None = None):
        target_level = target_level or self.current_section_level - 1
        self._doc.close_section(target_level=target_level)
        self._next_section_num = self._next_section_num[:target_level + 1]
        self._next_section_num[-1] += 1
        self._out_of_section = True
        self._curr_list_key = None
        return

    def log(
        self,
        level: LogLevel | str | int,
        title: Stringable,
        *content: ContainerContentInputType | MDContainer,
        sys_exit: bool | None = None,
        exit_code: int | None = None,
        file: Stringable | None = None,
        line: int | None = None,
        line_end: int | None = None,
        column: int | None = None,
        column_end: int | None = None,
        stack_up: int = 0,
    ):
        if self._out_of_section:
            self.section(title=self._get_caller_name(stack_up+1))
        if self._list_entries and self._curr_list_key is None:
            self._curr_list_key = self._doc.current_section.body.append(
                content=_mdit.element.ordered_list(
                    target_configs=self._doc.target_configs
                ),
            )
        self._submit_log(
            level=level,
            title=title,
            content=content,
            file=file,
            line=line,
            line_end=line_end,
            column=column,
            column_end=column_end,
            stack_up=stack_up + 1
        )
        level_name = self._get_level_name(level)
        level = self._level[level_name]
        if level.level is LogLevel.CRITICAL:
            if sys_exit is None:
                sys_exit = self._default_exit_code is not None
        if level is LogLevel.CRITICAL and sys_exit:
            _sys.stdout.flush()
            _sys.stderr.flush()
            _sys.stdin.flush()
            exit_code = exit_code or self._default_exit_code
            _sys.exit(exit_code)
        return

    def debug(
        self,
        title: Stringable,
        *content,
        stack_up: int = 0,
    ) -> None:
        return self.log(LogLevel.DEBUG, title, *content, stack_up=stack_up + 1)

    def success(
        self,
        title: Stringable,
        *content,
        stack_up: int = 0,
    ) -> None:
        return self.log(LogLevel.SUCCESS, title, *content, stack_up=stack_up + 1)

    def info(
        self,
        title: Stringable,
        *content,
        stack_up: int = 0,
    ) -> None:
        return self.log(LogLevel.INFO, title, *content, stack_up=stack_up + 1)

    def notice(
        self,
        title: Stringable,
        *content,
        file: Stringable | None = None,
        line: int | None = None,
        line_end: int | None = None,
        column: int | None = None,
        column_end: int | None = None,
        stack_up: int = 0,
    ) -> None:
        return self.log(
            LogLevel.NOTICE,
            title,
            *content,
            file=file,
            line=line,
            line_end=line_end,
            column=column,
            column_end=column_end,
            stack_up=stack_up + 1
        )

    def warning(
        self,
        title: Stringable,
        *content,
        file: Stringable | None = None,
        line: int | None = None,
        line_end: int | None = None,
        column: int | None = None,
        column_end: int | None = None,
        stack_up: int = 0,
    ) -> None:
        return self.log(
            LogLevel.WARNING,
            title,
            *content,
            file=file,
            line=line,
            line_end=line_end,
            column=column,
            column_end=column_end,
            stack_up=stack_up + 1
        )

    def error(
        self,
        title: Stringable,
        *content,
        file: Stringable | None = None,
        line: int | None = None,
        line_end: int | None = None,
        column: int | None = None,
        column_end: int | None = None,
        stack_up: int = 0,
    ) -> None:
        return self.log(
            LogLevel.ERROR,
            title,
            *content,
            file=file,
            line=line,
            line_end=line_end,
            column=column,
            column_end=column_end,
            stack_up=stack_up + 1
        )

    def critical(
        self,
        title: Stringable,
        *content,
        sys_exit: bool | None = None,
        exit_code: int | None = None,
        file: Stringable | None = None,
        line: int | None = None,
        line_end: int | None = None,
        column: int | None = None,
        column_end: int | None = None,
        stack_up: int = 0,
    ):
        return self.log(
            LogLevel.CRITICAL,
            title,
            *content,
            sys_exit=sys_exit,
            exit_code=exit_code,
            file=file,
            line=line,
            line_end=line_end,
            column=column,
            column_end=column_end,
            stack_up=stack_up + 1
        )

    def _submit_log(
        self,
        level: LogLevel | str | int,
        title: Stringable,
        content: tuple,
        file: Stringable | None = None,
        line: int | None = None,
        line_end: int | None = None,
        column: int | None = None,
        column_end: int | None = None,
        stack_up: int = 0,
    ):
        level_name = self._get_level_name(level)
        level = self._level[level_name]
        sig = self._get_sig(level=level.style, stack_up=stack_up + 1)
        dropdown = _mdit.element.dropdown(
            title=title,
            body=list(content),
            footer=sig,
            opened=level.style.opened,
            color=level.style.color,
            icon=level.style.icon,
            octicon=level.style.octicon,
            chevron=level.style.chevron,
            animate=level.style.animate,
            margin=level.style.margin,
            classes_container=level.style.classes_container,
            classes_title=level.style.classes_title,
            classes_body=level.style.classes_body,
            config_rich=level.style.rich_config,
            target_configs=self._doc.target_configs,
            target_default=self._target_default_md,
        )
        if self._curr_list_key is not None:
            output_console = self._doc.current_section.body[self._curr_list_key].content.append(
                content=dropdown, conditions=[level_name]
            )
            list_number = output_console.number
        else:
            output_console = dropdown
            list_number = None
            self._doc.current_section.body.append(dropdown, conditions=[level_name])
        # Only print logs for realtime levels, except for when in GitHub Actions and debugging is enabled,
        # in which case all non-realtime logs are printed as debug messages.
        if level_name not in self._realtime_levels and not (self._github and self._github_debug):
            return
        if not self._github:
            self._print(output_console.source(target="console", filters=["console"]))
            return
        # In GitHub
        if level_name not in self._realtime_levels:
            # GHA Debug
            self._actionman_logger.debug(output_console.source(target="console", filters=["console"]))
            return
        dropdown_rich = dropdown.source(target="console", filters=["console"])
        group_title = dropdown_rich.title
        dropdown_rich.title = None
        if list_number:
            sec_num = rich.text.Text(f"{list_number:>3}. ")
            sec_num.append(group_title)
            group_title = sec_num
        self._actionman_logger.group(
            dropdown_rich,
            title=group_title,
        )
        annotation_type = self._get_github_annotation_type(level.level)
        if annotation_type:
            self._actionman_logger.annotation(
                typ=annotation_type,
                title=title,
                message=f"Click on the title above to see details.",
                filename=file,
                line_start=line,
                line_end=line_end,
                column_start=column,
                column_end=column_end,
            )
        return

    def _get_sig(self, level: LogLevelStyle, stack_up: int = 0) -> _mdit.MDContainer | None:
        if not level.signature:
            return
        signature = []
        for sig in level.signature:
            if sig == "caller_name":
                caller = self._get_caller_name(stack_up=stack_up + 1)
                signature.append(_mdit.inline_container(self._prefix_caller_name, _mdit.element.code_span(caller)))
            if sig == "time":
                timestamp = _datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                signature.append(_mdit.inline_container(self._prefix_time, _mdit.element.code_span(timestamp)))
        return _mdit.inline_container(*signature, separator=" ")

    @staticmethod
    def _get_level_name(level: str | int | LogLevel) -> str:
        if isinstance(level, LogLevel):
            return level.name.lower()
        if isinstance(level, int):
            return LogLevel(level).name.lower()
        return level

    @staticmethod
    def _get_level_enum(level: str | int | LogLevel) -> LogLevel:
        if isinstance(level, LogLevel):
            return level
        if isinstance(level, int):
            return LogLevel(level)
        return LogLevel[level.upper()]

    def _print(self, renderable):
        # Flush the standard output and error streams to ensure the text is printed immediately
        # and not buffered in between other print statements (e.g. tracebacks).
        _sys.stdout.flush()
        _sys.stderr.flush()
        self._console.print(renderable)
        return

    @staticmethod
    def _get_open_exception():
        exception = _sys.exc_info()[1]
        if not exception:
            return
        name = exception.__class__.__name__
        traceback = _traceback.format_exc()
        return name, exception, traceback

    @staticmethod
    def _get_github_annotation_type(level: LogLevel) -> Literal["notice", "warning", "error"] | None:
        mapping = {
            LogLevel.NOTICE: "notice",
            LogLevel.WARNING: "warning",
            LogLevel.ERROR: "error",
            LogLevel.CRITICAL: "error",
        }
        return mapping[level] if level in mapping else None

    @staticmethod
    def _get_caller_name(stack_up: int = 0) -> str:
        stack = _inspect.stack()
        # The caller is the second element in the stack list
        caller_frame = stack[stack_up + 1]
        caller_module = _inspect.getmodule(caller_frame.frame)
        if caller_module:
            caller_module_name = caller_module.__name__
        else:
            caller_filename = caller_frame.filename
            caller_filepath = _Path(caller_filename)
            caller_module_name = caller_filepath.stem
        # Get the function or method name
        func_name = caller_frame.function
        # Combine them to get a fully qualified name
        if func_name == "<module>":
            fully_qualified_name = f"{caller_module_name}:{caller_frame.lineno}"
        else:
            fully_qualified_name = f"{caller_module_name}.{func_name}"
        return fully_qualified_name
