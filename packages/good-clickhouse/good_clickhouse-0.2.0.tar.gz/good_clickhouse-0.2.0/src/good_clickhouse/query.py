# from good_clickhouse import query
import functools
import inspect
import os
import re
import sys
from good_common.modeling import TypeInfo
import typing
import datetime

# import chdb
# from chdb import session as chs
# import chdb.dbapi as dbapi
import textwrap
import typing
from contextlib import AsyncExitStack, ExitStack, asynccontextmanager
from pathlib import Path

from fast_depends import inject, utils
from fast_depends.core import build_call_model
from fast_depends.library import CustomField
from jinja2 import BaseLoader, Environment, StrictUndefined
from loguru import logger
from pydantic import BaseModel

# import asyncio

# if "IPython" in sys.modules:
#     logger.info("Interactive mode detected. Applying nest_asyncio...")
# import nest_asyncio

# nest_asyncio.apply()


def get_clickhouse_type(
    typeinfo: TypeInfo,
    datetime64: bool = True,
    datetime_precision: int = 3,
    int64: bool = True,
) -> str:
    _type = None
    if not typeinfo:
        raise ValueError("typeinfo is required")
    if typeinfo.db_type:
        _type = typeinfo.db_type
    elif typeinfo.is_pydantic_model:
        _type = "String"
    elif typeinfo.type is str:
        _type = "String"
    elif typeinfo.type is int:
        if int64:
            _type = "Int64"
        else:
            _type = "Int32"
    elif typeinfo.type is float:
        _type = "Float64"
    elif typeinfo.type is datetime.date:
        _type = "Date"
    elif typeinfo.type is datetime.datetime:
        if datetime64:
            _type = f"DateTime64({datetime_precision})"
        else:
            _type = "DateTime"
    elif typeinfo.type is bool:
        _type = "Bool"
    elif typing.get_origin(typeinfo.type) is dict:
        if typeinfo.type == dict[str, str]:
            _type = "Map(String, String)"
        else:
            _type = "String"

    elif typeinfo.is_iterable and typeinfo.item_type:
        _inner_type = get_clickhouse_type(
            typeinfo.item_type,
            datetime64=datetime64,
            datetime_precision=datetime_precision,
            int64=int64,
        )
        _type = f"Array({_inner_type})"
    else:
        _type = "String"

    if typeinfo.is_optional and not _type.startswith("Map"):
        _type = f"Nullable({_type})"
    return _type


class ClickhouseColumn:
    def __init__(self, name, typeinfo: TypeInfo, **kwargs):
        self.name = name
        self.typeinfo = typeinfo
        self.type = get_clickhouse_type(typeinfo, **kwargs)
        if typeinfo.is_pydantic_model:
            self.json_serialize = True
        else:
            pass

    name: str
    type: str
    json_serialize: bool = False

    def __repr__(self) -> str:
        return f"{self.name} {self.type}"


def get_env_var(name: str, default: typing.Any = None, fail_if_missing: bool = False):
    if fail_if_missing:
        return os.environ[name]
    return os.environ.get(name, default)


def filter_quote(value: str) -> str:
    return f"'{value}'"


class Statement(str):
    def __new__(cls, value: str):
        return super().__new__(cls, value)

    def echo(self):
        print(self)
        return self


class SQL:
    instance_registry: typing.ClassVar[dict[str, typing.Self]] = {}

    __filters__: typing.ClassVar[dict[str, typing.Callable]] = {}

    __globals__: typing.ClassVar[dict[str, typing.Any]] = {}

    @classmethod
    def register_filter(cls, name: str, fn: typing.Callable):
        if name in ("quote"):
            raise ValueError("Cannot override built-in filter")

        if name in cls.__filters__:
            raise ValueError(f"Duplicate filter: {name}")
        cls.__filters__[name] = fn

    @classmethod
    def register_global(cls, name: str, value: typing.Any):
        if name in ("env"):
            raise ValueError("Cannot override built-in global")

        if name in cls.__globals__:
            raise ValueError(f"Duplicate global: {name}")
        cls.__globals__[name] = value

    @staticmethod
    def build_template(
        template: str,
        enable_async: bool = False,
        **values: dict[str, typing.Any] | None,
    ) -> str:
        # Dedent, and remove extra linebreak
        cleaned_template = textwrap.dedent(inspect.cleandoc(template))

        # Add linebreak if there were any extra linebreaks that
        # `cleandoc` would have removed
        ends_with_linebreak = template.replace(" ", "").endswith("\n\n")
        if ends_with_linebreak:
            cleaned_template += "\n"

        # Remove extra whitespaces, except those that immediately follow a newline symbol.
        # This is necessary to avoid introducing whitespaces after backslash `\` characters
        # used to continue to the next line without linebreak.
        cleaned_template = re.sub(r"(?![\r\n])(\b\s+)", " ", cleaned_template)

        env = Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
            undefined=StrictUndefined,
            loader=BaseLoader(),
            enable_async=enable_async,
        )

        env.globals["env"] = get_env_var

        env.filters["quote"] = filter_quote

        SQL.patch_env(env)

        jinja_template = env.from_string(cleaned_template)

        return jinja_template

    @classmethod
    def register(cls, name: str, query: typing.Self):
        cls.instance_registry[name] = query

    @classmethod
    def patch_env(cls, env: Environment):
        for name, query in cls.instance_registry.items():
            if name in env.globals:
                raise ValueError(f"Duplicate env variable: {name}")
            env.globals[name] = query

    def __init__(self, fn: typing.Callable, **kwargs):
        functools.update_wrapper(self, fn)
        self.fn = inject(fn)
        self.signature, self.annotation = utils.get_typed_signature(fn)
        # self.parameters = list(self.signature.parameters.keys())
        self.docstring = fn.__doc__
        self.template = typing.cast(str, self.docstring)
        self.__class__.register(fn.__name__, self)
        self._kwargs = kwargs
        self.overrides = {}

        if self.is_async():

            async def _return_args(*args, **kwargs):
                return args, kwargs

            signature = inspect.signature(fn)

            return_annotation = signature.return_annotation

            _return_args.__signature__ = signature.replace(
                return_annotation=inspect.Signature.empty
            )  # type: ignore

            self.call_model = build_call_model(_return_args)

            if issubclass(return_annotation, BaseModel):
                self.response_model = return_annotation

            self.call_model.response_model = None

        else:

            def _return_args(*args, **kwargs):
                return args, kwargs

            signature = inspect.signature(fn)

            return_annotation = signature.return_annotation

            _return_args.__signature__ = signature.replace(
                return_annotation=inspect.Signature.empty
            )

            self.call_model = build_call_model(_return_args)

            self.response_model = return_annotation

            self.call_model.response_model = None

    fn: typing.Callable
    template: str
    annotation: dict[str, typing.Any]
    signature: inspect.Signature
    docstring: str

    def is_async(self):
        return inspect.iscoroutinefunction(self.fn)

    @property
    def parameters(self):
        return list(self.signature.parameters.keys())

    @property
    def name(self):
        return self.fn.__name__

    def render_sync(self, *args, **kwargs):
        # logger.debug(f"Rendering {self.name} in sync mode")
        bound_arguments = self.signature.bind(*args, **kwargs)
        bound_arguments.apply_defaults()

        with ExitStack() as stack:
            resolved = self.call_model.solve(
                *args,
                stack=stack,
                dependency_overrides=self.overrides,
                cache_dependencies={},
                nested=False,
                **bound_arguments.arguments,
            )
            _, arguments = resolved

        template = self.build_template(
            template=self.template,
            # template_context=self.template_context,
            **arguments,
        )
        return Statement(template.render(**arguments))

    async def render_async(self, *args, **kwargs):
        # logger.debug(f"Rendering {self.name} in async mode")
        bound_arguments = self.signature.bind(*args, **kwargs)
        bound_arguments.apply_defaults()

        async with AsyncExitStack() as stack:
            resolved = await self.call_model.asolve(
                *args,
                stack=stack,
                dependency_overrides=self.overrides,
                cache_dependencies={},
                nested=True,
                **bound_arguments.arguments,
            )
            _, arguments = resolved

        template = self.build_template(
            self.template,
            enable_async=True,
            **arguments,
        )

        return Statement(await template.render_async(**arguments))

    def __call__(self, *args, **kwargs) -> Statement | typing.Awaitable[Statement]:
        """Render and return the template.

        Returns
        -------
        The rendered template as a Python ``str``.

        """
        if self.is_async():
            return self.render_async(*args, **kwargs)
        else:
            return self.render_sync(*args, **kwargs)

        # return SQL.render(self, *args, **kwargs)

    def __str__(self):
        return self.template

    def pretty(self):
        return textwrap.dedent(self.template)


def sql(fn: typing.Callable | str | None = None, **kwargs):
    """
    SQL decorator
    """

    if isinstance(fn, str):
        return SQL.render(fn, **kwargs)

    def _sql(fn):
        return SQL(fn, **kwargs)

    if fn is None:
        return _sql
    else:
        return _sql(fn)


@sql
def drop_table(database: str, name: str):
    """
    DROP TABLE IF EXISTS `{{database}}`.`{{name}}`;
    """


@sql
def table(
    database: str,
    name: str,
    columns: list[ClickhouseColumn],
    extra_columns: dict = {},
    column_defaults: dict = {},
    projection: str = "",
    engine: str = "MergeTree()",
    order_by: str = "",
    **settings,
):
    """
    CREATE TABLE IF NOT EXISTS `{{database}}`.`{{name}}` (
       {% for column in columns %}
       {{""| indent(4)}}{% if loop.first %}{% else %},{% endif -%}
          {{column.name}} {{column.type}}
          {%- if column.name in column_defaults %} DEFAULT {{column_defaults[column.name]}} {% endif %}\n
       {% endfor %}
       {% for name, type in extra_columns.items() %}
       ,{{name | indent(4)}} {{type}}
       {% endfor %}
       {% if projection -%}
         ,{{projection}}
       {% endif %}
    )
    engine = {{engine}}
    {{order_by}}
    {% if settings %}
    settings
    {%- for key, value in settings.items() %}
    {{key}} = {{value}} {% if loop.last %}{% else %},{% endif %}
    {% endfor %}
    {% endif %}
    ;
    """
