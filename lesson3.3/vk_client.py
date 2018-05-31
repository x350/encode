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

TOKEN = 'e29f1d1ba6d14f16a03332576dc7f695e7825357764580eced7513cb749ca8fc4eafe168b9dee28914979'
TOKEN1 = '0bfa324ecf01b18d8c6d4e425f8efd14aae2bf3cee264f15c072cafc82164783918d27083761e7e489429'


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
    print(find_common_friends(72506872, 4058481, TOKEN1))

#
