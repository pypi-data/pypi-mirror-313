from .query import sql, SQL
from fast_depends import inject, Depends
import os

try:
    import chdb
except ImportError:
    import warnings

    warnings.warn("chdb not found")


@sql
def remote_table_secure(host: str, database: str, table: str, user: str, password: str):
    """
    remoteSecure('{{host}}', '{{database}}', '{{table}}', '{{user}}', '{{password}}')
    """


def _inject_env_variable(name: str):
    def _internal():
        return os.environ[name]

    return _internal


@sql
def remote_table_secure_ch_cloud(
    database: str,
    table: str,
    host: str = Depends(_inject_env_variable("CLICKHOUSE_CLOUD_HOST")),
    password: str = Depends(_inject_env_variable("CLICKHOUSE_CLOUD_PASSWORD")),
):
    """
    remoteSecure('{{host}}', '{{database}}', '{{table}}', 'default', '{{password}}')
    """


# SQL.register_global("remote_table_secure_ch_cloud", remote_table_secure_ch_cloud)


# @sql
# def load_remote_table(target_table: str):
#     """
#     insert into table function {{remote_table_secure_ch_cloud('source_calaccess', target_table )}}
#     select *
#         ,now64() as record_ts
#     from calaccess.{{target_table}}
#     where record_hash not in (
#         select record_hash
#         from {{remote_table_secure_ch_cloud('source_calaccess', target_table )}}
#     )
#     """
