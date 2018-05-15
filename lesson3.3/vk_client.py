from urllib.parse import urlencode
import requests

# AUTH_URL = 'https://oauth.vk.com/authorize'
# APP_ID = 6480250
# auth_data = {
#     'client_id': APP_ID,
#     'display': 'page',
#     'scope': 'friends status',
#     'response_type': 'token',  # 'code'
#     'v': '5.74'
# }
#
# print('?'.join((AUTH_URL, urlencode(auth_data))))


my_id = 450062677
target_id = 96318028
olga_id = 488003955

TOKEN = '21c43c91e3e5137074f7ccfc737f316e8e3217d8f3457c329021ad34b3b6be2efba8bf092e450e43cb51b'


def find_common_friends(source_id, target_id, token):
    response = requests.get(
        'https://api.vk.com/method/friends.getMutual',
        params=dict(v='5.74', access_token=token, source_uid=source_id, target_uid=target_id)
    ).json()
    resp = response.get('response', [])
    for item in resp:
        print('For User_ID = {} -> page: {}'.format(item, ''.join(('https://vk.com/id', str(item)))))


if __name__ == '__main__':
    find_common_friends(my_id, target_id, TOKEN)


