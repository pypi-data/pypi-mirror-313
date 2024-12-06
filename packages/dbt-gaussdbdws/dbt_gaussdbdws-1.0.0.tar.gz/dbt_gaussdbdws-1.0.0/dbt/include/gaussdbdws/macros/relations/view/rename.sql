{% macro gaussdbdws__get_rename_view_sql(relation, new_name) %}
    alter view if exists {{ relation }} rename to {{ new_name }}
{% endmacro %}
