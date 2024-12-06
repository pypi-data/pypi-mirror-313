{% macro gaussdbdws__get_replace_table_sql(relation, sql) -%}

    {%- set sql_header = config.get('sql_header', none) -%}
    {{ sql_header if sql_header is not none }}

    -- Drop the existing table if it exists
    DROP TABLE IF EXISTS {{ relation }};

    -- Create a new table
    CREATE TABLE {{ relation }}
        {% set contract_config = config.get('contract') %}
        {% if contract_config.enforced %}
            {{ get_assert_columns_equivalent(sql) }}
            {{ get_table_columns_and_constraints() }}
            {%- set sql = get_select_subquery(sql) %}
        {% endif %}
    AS (
        {{ sql }}
    );

{%- endmacro %}
