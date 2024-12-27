import requests


class CoordinatesFetcher:
    BASE_URL = 'https://geocode-maps.yandex.ru/1.x/'

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_response(self, query: str):
        response = requests.get(
            self.BASE_URL,
            params={
                'format': 'json',
                'apikey': self.api_key,
                'geocode': query
            }
        )

        if response.status_code == 200:
            return response.json().get('response')
        elif response.status_code == 403:
            print('Адрес или координаты не найдены.')
        else:
            print('Произошла ошибка, не связанная с адресом.')

    def get_coordinates(self, address: str):
        response_data = self.fetch_response(address)
        geo_objects = response_data['GeoObjectCollection']['featureMember'] if response_data else []

        # Проверка на пустой ответ
        if not geo_objects:
            print('Ответ от сервера пуст.')
            return

        try:
            point = geo_objects[0]['GeoObject']['Point']['pos']
            longitude, latitude = map(float, point.split())
            return longitude, latitude
        except (IndexError, ValueError):
            return None


# Пример использования:
# API_KEY = '5cbf1bfd-9264-477c-b05c-2af092e99e54'
# fetcher = CoordinatesFetcher(API_KEY)
# test_address = 'Гашека 7'
# print(fetcher.get_coordinates(test_address))
