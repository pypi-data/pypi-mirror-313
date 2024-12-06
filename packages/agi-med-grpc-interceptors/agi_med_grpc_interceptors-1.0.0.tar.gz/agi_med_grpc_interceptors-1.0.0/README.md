# agi-med-grpc-interceptors

Стандартные middlewares для grpc

## Ответственный разработчик

@zhelvakov

## Общая информация

- LoggingInterceptor - работает на loguru. Принимает metadata, забирает все хедеры и пытается использовать как контекст, по-умолчанию дополнительно прописывает uuid в контекст. Обработка ошибок может быть переопределена с помощью метода exception_handler


### Линтеры

```shell
pip install black flake8-pyproject mypy
black .
flake8
mypy .
```
