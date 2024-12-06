-- https://help.aliyun.com/zh/maxcompute/user-guide/cast
{% macro maxcompute__cast(field, type) %}
    cast({{field}} as {{type}})
{% endmacro %}
