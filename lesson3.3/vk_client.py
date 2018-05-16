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
TOKEN1 = '54fb9fc1357d58b299e75f33b0eada3a9fcccb7a6cb6a6d80b5c8796b90274c14c6c751ebd328592e9afd'


def find_common_friends(source_id, friend_id, token):
    token = token
    try:
        response = requests.get(
            'https://api.vk.com/method/friends.getMutual',
            params=dict(v='5.74', access_token=token, source_uid=source_id, target_uid=friend_id)
        ).json()
    except Exception as e:
        print('Exception: {}'.format(e))
        exit(2)

    # print(response)
    if response.get('error', []):
        print('Response error - {}'.format(response['error']['error_msg']))
        exit(1)
    resp = response.get('response', [])

    page_list = []
    for item in resp:
        page = ''.join(('https://vk.com/id', str(item)))
        # print('For User_ID = {} -> page: {}'.format(item, page))
        page_list.append(page)
    return list(zip(resp, page_list))


if __name__ == '__main__':
    print(find_common_friends(my_id, target_id, TOKEN1))


