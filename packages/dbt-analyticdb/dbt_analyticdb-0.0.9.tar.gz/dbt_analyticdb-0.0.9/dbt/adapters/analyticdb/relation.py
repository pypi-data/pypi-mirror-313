from dataclasses import dataclass, field

from dbt.adapters.base.relation import BaseRelation, Policy
from dbt_common.exceptions import DbtRuntimeError


@dataclass
class AnalyticDBQuotePolicy(Policy):
    database: bool = False
    schema: bool = True
    identifier: bool = True


@dataclass
class AnalyticDBIncludePolicy(Policy):
    database: bool = False
    schema: bool = True
    identifier: bool = True


@dataclass(frozen=True, eq=False, repr=False)
class AnalyticDBRelation(BaseRelation):
    quote_policy: AnalyticDBQuotePolicy = field(default_factory=lambda: AnalyticDBQuotePolicy())
    include_policy: AnalyticDBIncludePolicy = field(default_factory=lambda: AnalyticDBIncludePolicy())
    quote_character: str = "`"

    def __post_init__(self):
        if self.database != self.schema and self.database:
            raise DbtRuntimeError(
                f"Cannot set `database` to '{self.database}' in mysql!"
                "You can either unset `database`, or make it match `schema`, "
                f"currently set to '{self.schema}'"
            )

    def render(self):
        if self.include_policy.database and self.include_policy.schema:
            raise DbtRuntimeError(
                "Got a mysql relation with schema and database set to "
                "include, but only one can be set"
            )
        return super().render()
