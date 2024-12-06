{% macro gaussdbdws__describe_materialized_view(relation) %}
    {% set _indexes = run_query(get_show_indexes_sql(relation)) %}
    {% do return({'indexes': _indexes}) %}
{% endmacro %}
