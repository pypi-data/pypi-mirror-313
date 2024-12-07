dig_ass_critic_protos
==

## Ответственный разработчик

@bakulin

## Фичи
1. Кастомный header
2. Кастомный request
3. Клиент для critic навыков. Использует loguru для warnings

## Зависимости

`python3.13 -m pip install -r requirements.txt`

## Тесты

- `sudo docker compose up --build`

### Линтеры

Работают частично, не удалось исключить [DigitalAssistantCritic_pb2_grpc.py](src/dig_ass_critic_protos/DigitalAssistantCritic_pb2_grpc.py) из проверки

```shell
pip install black flake8-pyproject mypy
black .
flake8
mypy .
```