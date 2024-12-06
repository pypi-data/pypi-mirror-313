{% macro gaussdbdws__any_value(expression) -%}

    min({{ expression }})

{%- endmacro %}
