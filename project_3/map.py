import folium
from folium.plugins import AntPath
import requests
import json


def fetch_coordinates(city_name):
    """
    Получение координат города с использованием OpenWeatherMap API.
    """
    api_key = '97fc9f22b03e417267b5731c5c24c83a'
    api_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}'
    response = requests.get(api_url)
    city_data = response.json()[0]
    return city_data['lat'], city_data['lon']


def load_city_list(filename):
    """
    Загрузка списка городов из указанного JSON файла.
    """
    with open(filename, 'r') as json_file:
        return json.load(json_file)


def create_route_map(city_list, output_filename):
    """
    Создание маршрута на карте с маркерами городов и сохранением в HTML файл.
    """
    coordinates = []
    city_weather_data = []

    # Получение координат и информации о погоде для городов
    for city in city_list:
        latitude, longitude = fetch_coordinates(city)
        coordinates.append((latitude, longitude))
        city_weather_data.append((city, latitude, longitude))

    # Создание карты, центрированной на первом городе
    route_map = folium.Map(location=coordinates[0], zoom_start=5)

    # Добавление маркеров на карту
    for city_name, latitude, longitude in city_weather_data:
        folium.Marker(
            location=[latitude, longitude],
            popup=f"<b>{city_name}</b><br>Координаты: {latitude:.2f}, {longitude:.2f}",
            icon=folium.Icon(color='blue', icon='cloud')
        ).add_to(route_map)

    # Добавление маршрута между городами
    AntPath(locations=coordinates, weight=5, color='blue').add_to(route_map)

    # Сохранение карты в файл
    route_map.save(output_filename)


if __name__ == '__main__':
    city_filename = 'selected_cities.json'
    map_output_file = 'static/map.html'

    cities = load_city_list(city_filename)
    create_route_map(cities, map_output_file)
