# 🗺️ Route Screenshot Generator

Автоматическая генерация PNG-изображений маршрутов между точками на Яндекс.Картах.

## 📦 Установка

```bash
git clone https://github.com/konspolyakov/en-route-screenshot.git
cd en-route-screenshot
pip install -r requirements.txt
playwright install
```
## ⚙️ Настройка 
Скопируйте `config_example.yaml` в `config.yaml`
```bash
cp config_example.yaml config.yaml
```
В файле `config.yaml` необходимо указать свой ключ для API yandex "JavaScript API и HTTP Геокодер", получить который можно [здесь](https://developer.tech.yandex.ru/) 

## 🚀 Запуск
```bash
python generate.py
```

## 📝 Входной CSV:
Скопируйте `routes_example.csv` в `routes.csv`
```bash
cp routes_example.csv routes.csv
```
И заполните строки вашими данные в нужном формате

## 🖼️ Результат
В папке `output/` — PNG-файлы маршрутов с кастомными метками.
