from dataclasses import dataclass, field
from typing import Any, Set, FrozenSet, List, Dict
from typing_extensions import Self

import agate
from dbt.adapters.contracts.relation import RelationConfig
from dbt.adapters.relation_configs import (
    RelationConfigBase,
    RelationConfigValidationMixin,
    RelationConfigValidationRule,
    RelationResults,
)
from dbt_common.exceptions import DbtRuntimeError

from dbt.adapters.gaussdbdws.relation_configs.constants import MAX_CHARACTERS_IN_IDENTIFIER
from dbt.adapters.gaussdbdws.relation_configs.index import (
    GaussDBDWSIndexConfig,
    GaussDBDWSIndexConfigChange,
)


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class GaussDBDWSMaterializedViewConfig(RelationConfigBase, RelationConfigValidationMixin):
    """
    This config follows the specs found here:
    https://support.huaweicloud.com/sqlreference-830-dws/dws_06_0357.html

    The following parameters are configurable by dbt:
    - table_name: name of the materialized view
    - query: the query that defines the view
    - indexes: the collection (set) of indexes on the materialized view

    Applicable defaults for non-configurable parameters:
    - method: `heap`
    - tablespace_name: `default_tablespace`
    - with_data: `True`
    """

    table_name: str = ""
    query: str = ""
    indexes: FrozenSet[GaussDBDWSIndexConfig] = field(default_factory=frozenset)

    @property
    def validation_rules(self) -> Set[RelationConfigValidationRule]:
        # index rules get run by default with the mixin
        return {
            RelationConfigValidationRule(
                validation_check=self.table_name is None
                or len(self.table_name) <= MAX_CHARACTERS_IN_IDENTIFIER,
                validation_error=DbtRuntimeError(
                    f"The materialized view name is more than {MAX_CHARACTERS_IN_IDENTIFIER} "
                    f"characters: {self.table_name}"
                ),
            ),
        }

    @classmethod
    def from_dict(cls, config_dict: dict) -> Self:
        kwargs_dict = {
            "table_name": config_dict.get("table_name"),
            "query": config_dict.get("query"),
            "indexes": frozenset(
                GaussDBDWSIndexConfig.from_dict(index) for index in config_dict.get("indexes", {})
            ),
        }
        materialized_view: Self = super().from_dict(kwargs_dict)  # type: ignore
        return materialized_view

    @classmethod
    def from_config(cls, relation_config: RelationConfig) -> Self:
        materialized_view_config = cls.parse_config(relation_config)
        materialized_view = cls.from_dict(materialized_view_config)
        return materialized_view

    @classmethod
    def parse_config(cls, relation_config: RelationConfig) -> Dict:
        indexes: List[Dict[Any, Any]] = relation_config.config.get("indexes", [])  # type: ignore
        config_dict = {
            "table_name": relation_config.identifier,
            "query": getattr(relation_config, "compiled_code", None),
            "indexes": [GaussDBDWSIndexConfig.parse_model_node(index) for index in indexes],
        }
        return config_dict

    @classmethod
    def from_relation_results(cls, relation_results: RelationResults) -> Self:
        materialized_view_config = cls.parse_relation_results(relation_results)
        materialized_view = cls.from_dict(materialized_view_config)
        return materialized_view

    @classmethod
    def parse_relation_results(cls, relation_results: RelationResults) -> dict:
        indexes: agate.Table = relation_results.get("indexes", agate.Table(rows={}))
        config_dict = {
            "indexes": [
                GaussDBDWSIndexConfig.parse_relation_results(index) for index in indexes.rows
            ],
        }
        return config_dict


@dataclass
class GaussDBDWSMaterializedViewConfigChangeCollection:
    indexes: List[GaussDBDWSIndexConfigChange] = field(default_factory=list)

    @property
    def requires_full_refresh(self) -> bool:
        return any(index.requires_full_refresh for index in self.indexes)

    @property
    def has_changes(self) -> bool:
        return self.indexes != []
