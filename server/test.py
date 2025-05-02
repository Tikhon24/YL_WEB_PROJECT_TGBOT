# файл для тестирования сервера вручную
import requests


def main():
    server = 'http://127.0.0.1:5000'
    route = '/get_ad_id'
    response = requests.get('{}{}'.format(server, route))
    ads_id = response.json()['ad_id']
    print(ads_id)
    server = 'http://127.0.0.1:5000'
    route = '/add_ad'
    data = {
        'title': 'Robert Paulsen',
        'description': 'Челик из БК',
        'price': '100500',
        'image': '123',
        'user_tag': '@robertpaulsen',
        'ads_id': ads_id,
        'message_id': '12345100500'
    }
    response = requests.post('{}{}'.format(server, route), json=data)
    print(response.json())


main()