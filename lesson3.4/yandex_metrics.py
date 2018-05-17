from pprint import pprint
from urllib.parse import urlencode
import requests

APP_ID = 'f2acc0cafc9c4bf0a86ad11d3e373fcb'
url = 'https://x350.github.io/'

# AUTH_URL = 'https://oauth.yandex.ru/authorize'
# auth_data = dict(
#     response_type='token',
#     client_id=APP_ID
# )
# print('?'.join((AUTH_URL, urlencode(auth_data))))

TOKEN = 'AQAAAAAA3zeoAAUBLPwgbjQcQkmOvZPTgai6y5g'


class YaMetrikaManagement:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Authorization': 'OAuth {}'.format(self.token)}

    @property
    def counters(self):
        header = self.get_headers()
        try:
            response = requests.get('https://api-metrika.yandex.ru/management/v1/counters', headers=header)
        except Exception as ex:
            print(f"Exception: {ex}")
            exit(1)

        return [c['id'] for c in response.json().get('counters',[])]

    def get_counter_info(self, counter_id):
        try:
            response = requests.get(
                'https://api-metrika.yandex.ru/management/v1/counter/{}'.format(counter_id),
                headers=self.get_headers()
            )
        except Exception as ex:
            print(f"Exception: {ex}")
            exit(1)
        return response.json()


ya_user1 = YaMetrikaManagement(TOKEN)
print("Счетчики пользователя: {}\n".format(ya_user1.counters))


class Counter:
    metrik_url = 'https://api-metrika.yandex.ru/stat/v1/data'

    def __init__(self, token, counter_id):
        self.token = token
        self.counter_id = counter_id

    def get_metrik_counter(self):
        try:
            response = requests.get('?'.join((self.metrik_url, urlencode(dict(
                ids=str(self.counter_id),
                metrics='ym:s:visits,ym:s:pageviews,ym:s:users',
                oauth_token=self.token
            ))))).json()
        except Exception as ex:
            print(f"Exception: {ex}")
            exit(1)
        print("Визиты - {},\nПросмотры - {},\nПосетители - {}.\n".format(*[int(i) for i in response.get('totals', [])]))


ya_user1 = YaMetrikaManagement(TOKEN)
for item in ya_user1.counters:
    print(f"Статистика для счетчика - {item}:")
    ya1 = Counter(TOKEN, item)
    ya1.get_metrik_counter()
