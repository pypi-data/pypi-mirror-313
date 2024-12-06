# agi-med-exp

Стандартизированный компонент отдела для экспериментов 

## Ответственный разработчик

@zhelvakov

## Общая информация

- Стандартный конфиг
- Даталоадер для ЦА

## Тесты

- `sudo docker compose up --build`


### Линтеры

```shell
pip install black flake8-pyproject mypy
black .
flake8
mypy .
```