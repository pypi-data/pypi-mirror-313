{% macro gaussdbdws__last_day(date, datepart) -%}

    {%- if datepart == 'quarter' -%}
    CAST(
        {{ dbt.dateadd('day', '-1', dbt.dateadd('month', '3', dbt.date_trunc('quarter', date)) ) }}
        AS date)
    {%- elif datepart == 'month' -%}
    CAST(
        {{ dbt.dateadd('day', '-1', dbt.dateadd('month', '1', dbt.date_trunc('month', date)) ) }}
        AS date)
    {%- elif datepart == 'year' -%}
    CAST(
        {{ dbt.dateadd('day', '-1', dbt.dateadd('month', '12', dbt.date_trunc('year', date)) ) }}
        AS date)
    {%- else -%}
    {{ exceptions.raise_compiler_error("Unsupported datepart for last_day in gaussdbdws: {!r}".format(datepart)) }}
    {%- endif -%}

{%- endmacro %}
