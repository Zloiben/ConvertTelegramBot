# Телеграмм Бот 

## Функционал: 
* Команда /convert. Конвертирует значение в нужную валюту
* Определяет нужно поприветствовать или попрощаться
Важно что поиск идет по ключевым словам указанным в файлах 

## Как запустить

1 Способ
```sh
docker-compose up --build
```

2 Способ 

Сначала установить зависимости
```sh
pip install -r requirements/PROD.txt
python main.py
```