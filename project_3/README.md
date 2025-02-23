## Описание проекта

"Прогноз погоды с маршрутом" — это веб-приложение на Flask, которое предоставляет:

- Прогноз погоды для различных городов.
- Графическое отображение прогноза.
- Возможность построить маршрут на интерактивной карте с погодными данными по каждому городу.

## API и визуализация

- **OpenWeather API**: получение информации о погоде для указанных городов.
- **Folium**: создание интерактивных карт.
- **Plotly.js**: отображение данных в виде графиков.

## Основные функции

- Получение прогноза на 1, 3 или 5 дней.
- Визуализация температуры и вероятности осадков на графиках.
- Построение маршрута с маркерами для городов на карте.
- Обновление данных в зависимости от выбранного города и временного периода.
- Интеграция с OpenWeather API для актуальных погодных данных.

## Использование

1. Перейдите на главную страницу (/).
2. Введите список городов для маршрута.
3. Выберите временной интервал (1, 3 или 5 дней).
4. Нажмите "Построить маршрут".
5. На странице /result появятся:
    - Графики прогноза погоды.
    - Интерактивная карта с маршрутом и прогнозами для каждого города.