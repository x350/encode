from urllib.parse import urlencode
import requests
from pprint import pprint

AUTH_URL = 'https://oauth.vk.com/authorize'
APP_ID = 6480250
auth_data = {
    'client_id': APP_ID,
    'display': 'page',
    'scope': 'friends status',
    'response_type': 'token',  # 'code'
    'v': '5.74'
}

my_id = 450062677
target_id = 96318028

print('?'.join((AUTH_URL, urlencode(auth_data))))

TOKEN = '21c43c91e3e5137074f7ccfc737f316e8e3217d8f3457c329021ad34b3b6be2efba8bf092e450e43cb51b'

# response = requests.get(
#     'https://api.vk.com/method/status.set',
#     params=dict(v='5.74', access_token=TOKEN, text='status for netology')
#)

response = requests.get(
    'https://api.vk.com/method/friends.getMutual',
    params=dict(v='5.74', access_token=TOKEN, source_uid=my_id, target_uid=target_id)
)

pprint(response.json())


