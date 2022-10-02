Установка
===================
1. Запустить проект с помощью докера:
   ```bash
   docker-compose up -d --build
   ```

Документация API
===================


### GET '/get_load_data'

- Возвращает данные о загрузке процессора, ОЗУ и видеокарты (если имеется)

Пример ответа:

```json

    {
        "cpu": 1.0, 
        "ram": 22.6, 
        "gpu": null
    }
```

### POST '/get_load_data'

- Возвращает данные об определенных типах загрузки
- Тело запроса:

    ```json
    {
        "load_types":["cpu", "gpu"]
    }
    ```
- Поле load_types является обязательным и содержит массив с перечислением ожидаемых типов загрузки "cpu", "ram", "gpu". Можно запрашивать один тип или несколько.

Пример ответа:

    ```json
    {
        "cpu": 0.4, 
        "gpu": null
    }
    ```

### GET '/get_all_data'

- возвращает все записи из redis

Пример ответа:

    ```json
    {
        "02:10:18:45:19": {"method": "GET", "info": {"cpu": 1.0, "ram": 22.6, "gpu": null}}, 
        "02:10:18:51:23": {"method": "POST", "info": {"cpu": 0.4, "gpu": null}}
    }
    ```

### POST '/remove_data'

- удаляет записи за промежуток времени, либо все записи, если промежуток не указан
- Тело запроса:

    ```json
    {
        "start":"02:10:18:45:19",
        "end":"02:10:18:51:23"
    }
    ```
