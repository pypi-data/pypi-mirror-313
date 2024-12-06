from dataclasses import dataclass, field
from typing import FrozenSet, List, Optional

from dbt.adapters.base.relation import BaseRelation
from dbt.adapters.contracts.relation import RelationConfig, RelationType
from dbt.adapters.relation_configs import (
    RelationConfigChangeAction,
    RelationResults,
)
from dbt_common.exceptions import DbtRuntimeError

from dbt.adapters.gaussdbdws.relation_configs import (
    MAX_CHARACTERS_IN_IDENTIFIER,
    GaussDBDWSIndexConfig,
    GaussDBDWSIndexConfigChange,
    GaussDBDWSMaterializedViewConfig,
    GaussDBDWSMaterializedViewConfigChangeCollection,
)


@dataclass(frozen=True, eq=False, repr=False)
class GaussDBDWSRelation(BaseRelation):
    renameable_relations: FrozenSet[RelationType] = field(
        default_factory=lambda: frozenset(
            {
                RelationType.View,
                RelationType.Table,
            }
        )
    )
    replaceable_relations: FrozenSet[RelationType] = field(
        default_factory=lambda: frozenset(
            {
                RelationType.View,
                RelationType.Table,
            }
        )
    )

    def __post_init__(self):
        # Check for length of GaussDBDWS table/view names.
        # Check self.type to exclude test relation identifiers
        if (
            self.identifier is not None
            and self.type is not None
            and len(self.identifier) > self.relation_max_name_length()
        ):
            raise DbtRuntimeError(
                f"Relation name '{self.identifier}' "
                f"is longer than {self.relation_max_name_length()} characters"
            )

    def relation_max_name_length(self):
        return MAX_CHARACTERS_IN_IDENTIFIER

    def get_materialized_view_config_change_collection(
        self, relation_results: RelationResults, relation_config: RelationConfig
    ) -> Optional[GaussDBDWSMaterializedViewConfigChangeCollection]:
        config_change_collection = GaussDBDWSMaterializedViewConfigChangeCollection()

        existing_materialized_view = GaussDBDWSMaterializedViewConfig.from_relation_results(
            relation_results
        )
        new_materialized_view = GaussDBDWSMaterializedViewConfig.from_config(relation_config)

        config_change_collection.indexes = self._get_index_config_changes(
            existing_materialized_view.indexes, new_materialized_view.indexes
        )

        # we return `None` instead of an empty `GaussDBDWSMaterializedViewConfigChangeCollection` object
        # so that it's easier and more extensible to check in the materialization:
        # `core/../materializations/materialized_view.sql` :
        #     {% if configuration_changes is none %}
        if config_change_collection.has_changes:
            return config_change_collection
        return None

    def _get_index_config_changes(
        self,
        existing_indexes: FrozenSet[GaussDBDWSIndexConfig],
        new_indexes: FrozenSet[GaussDBDWSIndexConfig],
    ) -> List[GaussDBDWSIndexConfigChange]:
        """
        Get the index updates that will occur as a result of a new run

        There are four scenarios:

        1. Indexes are equal -> don't return these
        2. Index is new -> create these
        3. Index is old -> drop these
        4. Indexes are not equal -> drop old, create new -> two actions

        *Note:*
            The order of the operations matters here because if the same index is dropped and recreated
            (e.g. via --full-refresh) then we need to drop it first, then create it.

        Returns: an ordered list of index updates in the form {"action": "drop/create", "context": <IndexConfig>}
        """
        drop_changes = [
            GaussDBDWSIndexConfigChange.from_dict(
                {"action": RelationConfigChangeAction.drop, "context": index}
            )
            for index in existing_indexes.difference(new_indexes)
        ]
        create_changes = [
            GaussDBDWSIndexConfigChange.from_dict(
                {"action": RelationConfigChangeAction.create, "context": index}
            )
            for index in new_indexes.difference(existing_indexes)
        ]
        return drop_changes + create_changes
