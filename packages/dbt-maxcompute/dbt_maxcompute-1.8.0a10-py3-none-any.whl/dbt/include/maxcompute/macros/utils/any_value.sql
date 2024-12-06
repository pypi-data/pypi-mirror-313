{# https://help.aliyun.com/zh/maxcompute/user-guide/any-value #}
{% macro maxcompute__any_value(expression) -%}

    any_value({{ expression }})

{%- endmacro %}
