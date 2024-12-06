from dbt.adapters.base import AdapterPlugin

from dbt.adapters.gaussdbdws.column import GaussDBDWSColumn
from dbt.adapters.gaussdbdws.connections import GaussDBDWSConnectionManager, GaussDBDWSCredentials
from dbt.adapters.gaussdbdws.impl import GaussDBDWSAdapter
from dbt.adapters.gaussdbdws.relation import GaussDBDWSRelation
from dbt.include import gaussdbdws


Plugin = AdapterPlugin(
    adapter=GaussDBDWSAdapter,
    credentials=GaussDBDWSCredentials,
    include_path=gaussdbdws.PACKAGE_PATH,
)
