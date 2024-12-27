import requests
import json


class WeatherReceiver:
    """
    Класс для получения данных о погоде с использованием API AccuWeather.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.location_url = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'
        self.forecast_url = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/'

    def get_location_key(self, lat, lon):
        """
        Получение ключа местоположения (locationKey) для дальнейшего запроса данных о погоде.
        """
        params = {
            'apikey': self.api_key,
            'q': f'{lat},{lon}'
        }
        try:
            response = requests.get(self.location_url, params=params)
            response.raise_for_status()
            return response.json().get('Key')
        except requests.RequestException as e:
            print(f"Ошибка получения locationKey: {e}")
            return None

    def get_weather(self, lat, lon):
        """
        Получение прогноза погоды на 5 дней и сохранение в JSON-файл.
        """
        location_key = self.get_location_key(lat, lon)
        if not location_key:
            print("Невозможно получить locationKey. Завершение операции.")
            return

        params = {
            'apikey': self.api_key,
            'metric': True,
            'details': True
        }
        try:
            response = requests.get(f'{self.forecast_url}{location_key}/', params=params)
            response.raise_for_status()
            data = response.json()
            with open('weather_forecast.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print("Данные о погоде успешно сохранены в 'weather_forecast.json'.")
        except requests.RequestException as e:
            print(f"Ошибка получения прогноза погоды: {e}")


def weather_key_parameters():
    """
    Выделение ключевых параметров прогноза погоды и сохранение их в JSON-файл.
    """
    try:
        with open('weather_forecast.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        daily_parameters = []
        for daily_forecast in data.get('DailyForecasts', []):
            params = {
                'date': daily_forecast['Date'],
                'max_temp': daily_forecast['Temperature']['Maximum']['Value'],
                'min_temp': daily_forecast['Temperature']['Minimum']['Value'],
                'avg_temp': (
                    daily_forecast['Temperature']['Maximum']['Value'] +
                    daily_forecast['Temperature']['Minimum']['Value']
                ) / 2,
                'day_forecast': {
                    'humidity': daily_forecast['Day'].get('RelativeHumidity', {}).get('Average'),
                    'wind_speed': daily_forecast['Day']['Wind']['Speed']['Value'],
                    'rain_probability': daily_forecast['Day']['RainProbability'],
                },
                'night_forecast': {
                    'humidity': daily_forecast['Night'].get('RelativeHumidity', {}).get('Average'),
                    'wind_speed': daily_forecast['Night']['Wind']['Speed']['Value'],
                    'rain_probability': daily_forecast['Night']['RainProbability']
                }
            }
            daily_parameters.append(params)

        with open('weather_key_parameters.json', 'w', encoding='utf-8') as file:
            json.dump(daily_parameters, file, ensure_ascii=False, indent=4)

        print("Ключевые параметры сохранены в 'weather_key_parameters.json'.")
        return daily_parameters

    except FileNotFoundError:
        print('Файл "weather_forecast.json" не найден. Убедитесь, что данные о погоде были загружены.')
    except Exception as e:
        print(f"Произошла ошибка при обработке данных: {e}")


if __name__ == '__main__':
    # Пример использования
    API_KEY = 'AGlRoTK491bc73SZrvSPGGx6fisQS586'
    LAT, LON = 55.7504461, 37.6174943

    weather = WeatherReceiver(API_KEY)
    weather.get_weather(LAT, LON)
    weather_key_parameters()
