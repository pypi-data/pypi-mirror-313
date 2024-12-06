{% macro maxcompute__validate_sql(sql) -%}
    explain {{ sql }}
{% endmacro %}
