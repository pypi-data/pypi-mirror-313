# good-clickhouse

A Clickhouse client with fast_depends based dependency injection.

Sync:
```python
from fast_depends import inject
from good_clickhouse import Clickhouse, ClickhouseProvider


@inject
def some_task(
    clickhouse: Clickhouse = ClickhouseProvider(),
):
    with clickhouse.cursor() as cursor:
        cursor.execute('SELECT 1')
        return cursor.fetchall()


```

Async:
```python
from fast_depends import inject
from good_clickhouse import ClickhouseAsync, ClickhouseAsyncProvider


@inject
async def some_task(
    clickhouse: ClickhouseAsync = ClickhouseAsyncProvider(),
):
    async with clickhouse as client:
        results = await client.execute('SELECT 1')
        return results

```


@query decorator utility for composing queries.
```python
from good_clickhouse import query

@query
def complex_query(table_name: str, columns: list[str], filters: dict[str, str]):
    """
    select {{ columns | join(', ') }}
    from {{ table_name }}
    where {% for key, value in filters.items() -%}
            {{ key }} {{ value }}{% if not loop.last %} and {% endif %}
          {%- endfor %};
    """


columns = ["id", "name", "age"]
filters = {"age": "> 20", "name": "like 'John%'"}
rendered_query = complex_query("users", columns, filters)
print(rendered_query)
"""
> select id, name, age
> from users
> where age > 20 and name like 'John%'
"""

```