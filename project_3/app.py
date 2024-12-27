from flask import Flask, render_template, request
from weather import WeatherReceiver, weather_key_parameters
from convert import GetCoords
from dashboard import generate_graphs
import json
import subprocess

application = Flask(__name__)


@application.route('/')
def home():
    return render_template('index.html')


@application.route('/result', methods=['POST'])
def process_result():
    selected_cities = request.form.getlist('cities[]')
    with open('selected_cities.json', 'w', encoding='utf-8') as output_file:
        json.dump(selected_cities, output_file, ensure_ascii=False)

    subprocess.run(['python', 'map.py'])
    results = []

    for city in selected_cities:
        try:
            longitude, latitude = GetCoords(COORDS_API_KEY).get_coords_by_address(city)
            WeatherReceiver(WEATHER_API_KEY).get_weather(latitude, longitude)
            weather_details = weather_key_parameters()

            for entry in weather_details:
                city_weather = {
                    'city_name': city,
                    'day_temp': entry['max_temp'],
                    'day_rain': entry['day_forecast']['rain_probability'],
                    'day_humidity': entry['day_forecast']['humidity'],
                    'day_wind': entry['day_forecast']['wind_speed'],
                    'night_temp': entry['min_temp'],
                    'night_rain': entry['night_forecast']['rain_probability'],
                    'night_humidity': entry['night_forecast']['humidity'],
                    'night_wind': entry['night_forecast']['wind_speed'],
                }
                results.append(city_weather)
        except Exception:
            return render_template('error.html', message="Указанный город не найден")

    # Генерация HTML графиков
    temperature_graph, precipitation_graph = generate_graphs()

    return render_template('result.html', data=results, temp_graph=temperature_graph, rain_graph=precipitation_graph)


COORDS_API_KEY = '5cbf1bfd-9264-477c-b05c-2af092e99e54'
WEATHER_API_KEY = 'JK2fkykcucX7HIE0GGyAN48zxRLVmjeA'

if __name__ == '__main__':
    application.run(debug=True)
