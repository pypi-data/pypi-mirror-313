import os
import typing

from aioch import Client as AsyncClient
from clickhouse_driver import connect
from clickhouse_driver.dbapi.connection import Connection
from clickhouse_driver.dbapi.extras import NamedTupleCursor
from fast_depends import inject
from good_common.dependencies import AsyncBaseProvider, BaseProvider
from loguru import logger
from pydantic import Field, SecretStr, field_serializer
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConnectionProfile(BaseSettings):
    host: str = "localhost"
    port: int = 9000
    database: str = "default"
    user: str = "default"
    password: SecretStr | None = None
    secure: bool = False
    compression: bool = False

    @field_serializer("password", when_used="json")
    def dump_secret(self, v: SecretStr | None) -> str | None:
        if v is None:
            return None
        return v.get_secret_value()

    @classmethod
    def load_by_prefix(cls, prefix: str, config: typing.MutableMapping) -> typing.Self:
        config = {
            "host": config.get(f"{prefix}_HOST", "localhost"),
            "port": config.get(f"{prefix}_PORT", 9000),
            "database": config.get(f"{prefix}_DATABASE", "default"),
            "user": config.get(f"{prefix}_USER", "default"),
            "password": config.get(f"{prefix}_PASSWORD", None),
            "secure": config.get(f"{prefix}_SECURE", False),
            "compression": config.get(f"{prefix}_COMPRESSION", False),
        }
        return cls(**config)


class Clickhouse:
    def __init__(self, connection: Connection):
        self.connection = connection

    def __enter__(self) -> NamedTupleCursor:
        self.cursor = self.connection.cursor(cursor_factory=NamedTupleCursor)
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        # self.connection.close()


class ClickhouseProvider(BaseProvider[Clickhouse], Clickhouse):
    def __init__(self, profile: str | None = None, _debug: bool = False):
        super().__init__(_debug=_debug, profile=profile)

    def initializer(self, cls_args, cls_kwargs, fn_kwargs):
        # mode = {**cls_kwargs, **fn_kwargs}.get("profile", "cloud").upper()
        kwargs = {}

        profile_name = {**cls_kwargs, **fn_kwargs}.pop("profile", None)

        profile = (
            "CLICKHOUSE"
            if profile_name is None
            else "CLICKHOUSE_" + profile_name.upper()
        )

        if profile_name:
            # logger.info(f"Using Clickhouse profile: {profile}")
            kwargs = {
                **ConnectionProfile.load_by_prefix(profile, os.environ).model_dump(
                    mode="json",
                    exclude_none=True,
                ),
            }

        return cls_args, kwargs

    @classmethod
    def provide(cls, *args, **kwargs) -> Clickhouse:
        return Clickhouse(connection=connect(**kwargs))


class ClickhouseAsync:
    @inject
    def __init__(self, sync_client: Clickhouse = ClickhouseProvider(), profile="local"):
        self.connection = AsyncClient(_client=sync_client.connection._make_client())

    async def __aenter__(self):
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # await self.connection.disconnect()
        pass
        # await self.cursor.close()
        # await self.connection.close()


class ClickhouseAsyncProvider(AsyncBaseProvider[ClickhouseAsync], ClickhouseAsync):
    pass
