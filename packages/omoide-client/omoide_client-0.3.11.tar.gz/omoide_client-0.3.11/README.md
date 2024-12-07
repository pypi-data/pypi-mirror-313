# omoide-client

Python-клиент для сервера `Omoide`.

## Генерация клиента

Для создания новой версии требуется запущенный экземпляр `Omoide`.

```shell
openapi-python-client generate --url http://127.0.0.1:8080/api/openapi.json --output-path ./omoide_tmp --overwrite
```

Мне не удалось добиться от утилиты генерации чистого результата, так что я просто предпочитаю 
копировать каталог `omoide_api_client` из того, что было сгенерировано.

## Как пользоваться клиентом

Создание экземпляра простого клиента:

```python
from omoide_client import Client

client = Client(base_url='https://api.example.com')
```

Создание экземпляра клиента с аутентификацией:

```python
from omoide_client import AuthenticatedClient

client = AuthenticatedClient(base_url='https://api.example.com', token='SuperSecretToken')
```

Использование:

```python
from omoide_client.models import MyDataModel
from omoide_client.api.my_tag import get_my_data_model
from omoide_client.types import Response

with client as client:
    my_data: MyDataModel = get_my_data_model.sync(client=client)
    response: Response[MyDataModel] = get_my_data_model.sync_detailed(client=client)
```

То же самое, но асинхронно:

```python
from omoide_client.models import MyDataModel
from omoide_client.api.my_tag import get_my_data_model
from omoide_client.types import Response

async with client as client:
    my_data: MyDataModel = await get_my_data_model.asyncio(client=client)
    response: Response[MyDataModel] = await get_my_data_model.asyncio_detailed(client=client)
```

При необходимости использовать отдельный сертификат для SSL.

```python
from omoide_client import AuthenticatedClient

client = AuthenticatedClient(
    base_url='https://internal_api.example.com', 
    token='SuperSecretToken',
    verify_ssl='/path/to/certificate_bundle.pem',
)
```

Можно также отключить проверку сертификата (это небезопасно):

```python
from omoide_client import AuthenticatedClient

client = AuthenticatedClient(
    base_url='https://internal_api.example.com', 
    token='SuperSecretToken', 
    verify_ssl=False
)
```

Стоит иметь в виду:

1. Все сочетания путь-метод станут модулями с четырьмя функциями:
    1. `sync`: Блокирующий запрос, возвращающий ответ или `None`.
    2. `sync_detailed`: Блокирующий запрос, всегда возвращающий `Request` (с полем `parsed` если он был успешен).
    3. `asyncio`: То же самое, что и `sync` только неблокирующий.
    4. `asyncio_detailed`: То же самое, что и `sync_detailed` только неблокирующий.

2. Все аргументы пути/тела запроса/строки запроса становятся аргументами метода клиента.
3. Если у ручки были теги, первый тег становится именем модуля для функции клиента.
4. Все ручки без тегов окажутся в модуле `omoide_client.api.default`

## Расширенная настройка

Объект `Client` обладает рядом расширенных настроек, которые можно посмотреть в его коде. 

Также есть возможность дополнительной настройки нижележащих `httpx.Client` или `httpx.AsyncClient`:

```python
from omoide_client import Client

def log_request(request):
    print(f'Request event hook: {request.method} {request.url} - Waiting for response')

def log_response(response):
    request = response.request
    print(f'Response event hook: {request.method} {request.url} - Status {response.status_code}')

client = Client(
    base_url='https://api.example.com',
    httpx_args={'event_hooks': {'request': [log_request], 'response': [log_response]}},
)

# Or get the underlying httpx client to modify directly with client.get_httpx_client() or client.get_async_httpx_client()
```

Существует также возможность замены клиента `httpx`, но это собьёт все настройки:

```python
import httpx
from omoide_client import Client

client = Client(
    base_url='https://api.example.com',
)
# Note that base_url needs to be re-set, as would any shared cookies, headers, etc.
client.set_httpx_client(httpx.Client(base_url='https://api.example.com', proxies='http://localhost:8030'))
```

## Публикация клиента

```shell
uv build
uv publish --token <token>
```
