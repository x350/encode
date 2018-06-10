from urllib.parse import urlencode
import requests
import time
import json


class VkData:
    AUTH_URL = 'https://oauth.vk.com/authorize'
    MY_ID = 450062677
    APP_ID = 6480250
    auth_data = {
        'client_id': APP_ID,
        'display': 'page',
        'scope': 'friends status',
        'response_type': 'token',  # 'code'
        'v': '5.78'
    }
    request_url = 'https://api.vk.com/method/'
    token = 'dcf7ad67cd8402758c543f60963b189e9b38b2643949c27585be2ffb118977331958a90551aca7f737f88'


# url = '?'.join((VkData.AUTH_URL, urlencode(VkData.auth_data)))
# print(url)

def get_vk_request(url, method, parametrs=None):
    try:
        response = requests.get(url + method, params=parametrs).json()
        time.sleep(0.34)
        if 'error' in response:
            print("Error request - {}".format(response['error']['error_msg']))
            return {}
        else:
            return response.get('response', {})
    except KeyError as er:
        print("KeyError: {}".format(er))
        exit(2)
    except Exception as e:
        print('Exception: {}'.format(e))
        exit(1)


def make_list_friends(user_id, token):
    method = 'friends.get'
    param = dict(user_id=user_id, access_token=token, v=5.78)
    return get_vk_request(VkData.request_url, method, param).get('items', None)


def make_list_groups(user_id, token):
    method = 'groups.get'
    param = dict(user_id=user_id, access_token=token, v=5.78)
    return get_vk_request(VkData.request_url, method, param).get('items', [])


def content_groups(group_id, token):
    method = 'groups.getById'
    param = dict(group_id=group_id, access_token=token, fields='members_count', v=5.78)
    try:
        response = requests.get(VkData.request_url + method, params=param).json()
        time.sleep(0.34)
        if 'error' in response:
            print("Error request - {}".format(response['error']['error_msg']))
            return {}
        else:
            result = response.get('response', {})[0]
            return {'name': result['name'], 'gid': result['id'], 'members_count': result['members_count']}
    except KeyError as er:
        print("KeyError: {}".format(er))
        # exit(2)
    except Exception as e:
        print('Exception: {}'.format(e))
        exit(1)


def make_set_groups(list_vk_id):
    count_common = len(list_vk_id)
    count_curent = 0
    friends_group_set = set()
    for item in list_vk_id:
        rr = make_list_groups(item, VkData.token)
        for i in rr:
            if i:
                friends_group_set.add(i)
        print('Обработано {}% друзей'.format(count_curent * 100//count_common))
        count_curent += 1
    return friends_group_set


def make_groups_describe_list(iterrible_object):
    result_list = []
    count_unique_groups = len(iterrible_object)
    curent_groups_count = 0
    for item in iterrible_object:
        result_list.append(content_groups(item, VkData.token))
        print('Обработано {}% уникальных групп'.format(curent_groups_count * 100 // count_unique_groups))
        curent_groups_count += 1
    return result_list


def resolve_name(screen_name):
    method = 'utils.resolveScreenName'
    param = dict(screen_name=screen_name, access_token=VkData.token, v=5.78)
    response = get_vk_request(VkData.request_url, method, param)
    if not response:
        print('Пользователь, с таким никнеймом - не существует!')
        exit(3)
    elif response['type'] != 'user':
        print("Это не пользователь, а {}!".format(response['type']))
        exit(3)
    else:
        return response['object_id']


def detect_activated_user(client_id, token):
    method = 'users.get'
    param = dict(user_id=client_id, access_token=token, v=5.78)
    response = get_vk_request(VkData.request_url, method, param)[0]
    if 'deactivated' in response.keys():
        print('Пользователь c id {}- деактивирован.'.format(response['id']))
        exit(4)


if __name__ == '__main__':
    client_id = input("ВВедите исследуемый VK_ID: ")
    if not client_id.isdigit():
        client_id = resolve_name(client_id)

    detect_activated_user(client_id, VkData.token)

    list_friends = make_list_friends(client_id, VkData.token)
    friends_group_set = make_set_groups(list_friends)
    list_id = [client_id]
    user_group_set = make_set_groups(list_id)

    unique_groups = user_group_set - friends_group_set

    result_list = make_groups_describe_list(unique_groups)

    with open('groups.json', 'w', encoding='utf-8') as file:
            json.dump(result_list, file)

    with open('groups.json', 'r', encoding='utf-8') as file:
        print(json.load(file))
