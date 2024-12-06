{% macro gaussdbdws__get_rename_materialized_view_sql(relation, new_name) %}
    -- Step 1: Create a new materialized view with the new name
    create materialized view {{ new_name }} as (
        select * from {{ relation }}
    );

    -- Step 2: Drop the old materialized view
    drop materialized view {{ relation }};
{% endmacro %}
