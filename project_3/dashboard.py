import plotly.express as px
import pandas as pd
import json


def create_weather_graphs():
    # Чтение данных о погоде из файла
    with open('weather_key_parameters.json', 'r') as weather_file:
        weather_info = json.load(weather_file)

    weather_df = pd.DataFrame(weather_info)
    weather_df['date'] = pd.to_datetime(weather_df['date'])  # Преобразование даты в формат datetime

    # График температуры
    temperature_chart = px.line(
        weather_df,
        x='date',
        y=['max_temp', 'min_temp'],
        labels={'value': 'Температура (°C)', 'date': 'Дата'},
        title='Прогноз температуры на ближайшие дни'
    )

    # График вероятности дождя
    rain_chart = px.bar(
        weather_df,
        x='date',
        y=[
            weather_df['day_forecast'].apply(lambda forecast: forecast['rain_probability']),
            weather_df['night_forecast'].apply(lambda forecast: forecast['rain_probability'])
        ],
        labels={'value': 'Вероятность дождя (%)', 'date': 'Дата'},
        title='Прогноз вероятности дождя'
    )
    rain_chart.update_layout(barmode='group', xaxis_tickangle=-45)

    # Генерация HTML-кода графиков
    temperature_html = temperature_chart.to_html(full_html=False)
    rain_html = rain_chart.to_html(full_html=False)

    return temperature_html, rain_html
