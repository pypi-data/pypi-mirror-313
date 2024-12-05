from dbt.adapters.analyticdb.connections import AnalyticDBConnectionManager  # noqa
from dbt.adapters.analyticdb.connections import AnalyticDBCredentials
from dbt.adapters.analyticdb.relation import AnalyticDBRelation  # noqa
from dbt.adapters.analyticdb.column import AnalyticDBColumn  # noqa
from dbt.adapters.analyticdb.impl import AnalyticDBAdapter

from dbt.adapters.base import AdapterPlugin
from dbt.include import analyticdb


Plugin = AdapterPlugin(
    adapter=AnalyticDBAdapter,  # type: ignore[arg-type]
    credentials=AnalyticDBCredentials,
    include_path=analyticdb.PACKAGE_PATH,
)
