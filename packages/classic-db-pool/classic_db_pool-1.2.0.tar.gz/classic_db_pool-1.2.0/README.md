`classic-db-pool` — это библиотека для управления соединениями с базой данных
эффективным способом. Она позволяет создавать пул соединений с базой данных,
который может использоваться несколькими запросами или процессами одновременно.
Это гарантирует, что ваше приложение всегда имеет доступ к готовому
к использованию соединению без необходимости ожидания первоначальной
настройки соединения каждый раз.

## Вклад

Этот проект является форком проекта [Embrace](https://hg.sr.ht/~olly/embrace-sql).

## Установка

Для установки classic-db-pool вы можете использовать pip:

```bash
pip install classic-db-pool
```

## Использование

Вот несколько примеров использования classic-db-pool.

```python
from classic.db_pool import ConnectionPool
import pymssql


pool = ConnectionPool(
    lambda: pymssql.connect(
        server='server',
        database='database',
        user='user',
        password='password',
    ),
    limit=1,
)


with pool.connect() as conn:
    conn.cursor().execute('SQL query')
```

