from dbt.adapters.gaussdbdws.relation_configs.constants import (
    MAX_CHARACTERS_IN_IDENTIFIER,
)
from dbt.adapters.gaussdbdws.relation_configs.index import (
    GaussDBDWSIndexConfig,
    GaussDBDWSIndexConfigChange,
)
from dbt.adapters.gaussdbdws.relation_configs.materialized_view import (
    GaussDBDWSMaterializedViewConfig,
    GaussDBDWSMaterializedViewConfigChangeCollection,
)
