{% macro gaussdbdws__datediff(first_date, second_date, datepart) -%}

    {% if datepart == 'year' %}
        (date_part('year', ({{second_date}})::date) - date_part('year', ({{first_date}})::date))
    {% elif datepart == 'quarter' %}
        ({{ gaussdbdws__datediff(first_date, second_date, 'year') }} * 4 + date_part('quarter', ({{second_date}})::date) - date_part('quarter', ({{first_date}})::date))
    {% elif datepart == 'month' %}
        ({{ gaussdbdws__datediff(first_date, second_date, 'year') }} * 12 + date_part('month', ({{second_date}})::date) - date_part('month', ({{first_date}})::date))
    {% elif datepart == 'day' %}
        extract(day FROM ({{second_date}})::date - ({{first_date}})::date)
    {% elif datepart == 'week' %}
        floor({{ gaussdbdws__datediff(first_date, second_date, 'day') }} / 7)
    {% elif datepart == 'hour' %}
        ({{ gaussdbdws__datediff(first_date, second_date, 'day') }} * 24 + date_part('hour', ({{second_date}})::timestamp) - date_part('hour', ({{first_date}})::timestamp))
    {% elif datepart == 'minute' %}
        ({{ gaussdbdws__datediff(first_date, second_date, 'hour') }} * 60 + date_part('minute', ({{second_date}})::timestamp) - date_part('minute', ({{first_date}})::timestamp))
    {% elif datepart == 'second' %}
        ({{ gaussdbdws__datediff(first_date, second_date, 'minute') }} * 60 + floor(date_part('second', ({{second_date}})::timestamp)) - floor(date_part('second', ({{first_date}})::timestamp)))
    {% elif datepart == 'millisecond' %}
        ({{ gaussdbdws__datediff(first_date, second_date, 'second') }} * 1000 + floor(date_part('millisecond', ({{second_date}})::timestamp)) - floor(date_part('millisecond', ({{first_date}})::timestamp)))
    {% elif datepart == 'microsecond' %}
        ({{ gaussdbdws__datediff(first_date, second_date, 'second') }} * 1000000 + floor(date_part('microsecond', ({{second_date}})::timestamp)) - floor(date_part('microsecond', ({{first_date}})::timestamp)))
    {% else %}
        {{ exceptions.raise_compiler_error("Unsupported datepart for macro datediff in gaussdbdws: {!r}".format(datepart)) }}
    {% endif %}

{%- endmacro %}
