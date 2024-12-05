from dbt.adapters.analyticdb.connections import MySQLConnectionManager  # noqa
from dbt.adapters.analyticdb.connections import MySQLCredentials
from dbt.adapters.analyticdb.relation import MySQLRelation  # noqa
from dbt.adapters.analyticdb.column import MySQLColumn  # noqa
from dbt.adapters.analyticdb.impl import MySQLAdapter

from dbt.adapters.base import AdapterPlugin
from dbt.include import analyticdb


Plugin = AdapterPlugin(
    adapter=MySQLAdapter,  # type: ignore[arg-type]
    credentials=MySQLCredentials,
    include_path=analyticdb.PACKAGE_PATH,
)
