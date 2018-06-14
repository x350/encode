import requests
import time
import json

REQUEST_URL = 'https://api.vk.com/method/'
CONNECTION_ATTEMPS = 20
VERSION_API_VK = 5.78

with open('config.json', 'r', encoding='utf-8') as file:
    TOKEN = json.load(file)['token']


def get_vk_request(url, method, token=TOKEN, version=VERSION_API_VK, fields_in_param={}):
    parametrs = dict(access_token=token, v=version)
    parametrs.update(fields_in_param)
    for i in range(CONNECTION_ATTEMPS):
        response = requests.get(url + method, params=parametrs).json()
        if 'response' in response:
            return response.get('response', {})
        elif 'error' in response:
            if response['error']['error_code'] == 6:
                continue
            else:
                print("Error request - {}".format(response['error']['error_msg']))
                return {}
        else:
            print(" Ошибка ответа")
            return {}
    print("Ошибка осединения")
    return {}


def make_list_friends(user_id):
    method = 'friends.get'
    fields_param = dict(user_id=user_id)
    return get_vk_request(REQUEST_URL, method, fields_in_param=fields_param).get('items', None)


def make_list_groups(user_id):
    method = 'groups.get'
    fields_param = dict(user_id=user_id)
    return get_vk_request(REQUEST_URL, method, fields_in_param=fields_param).get('items', [])


def content_groups(group_id):
    method = 'groups.getById'
    fields_param = dict(group_id=group_id, fields='members_count')
    result = get_vk_request(REQUEST_URL, method, fields_in_param=fields_param)[0]
    try:
        return {'name': result['name'], 'gid': result['id'], 'members_count': result['members_count']}
    except KeyError as er:
        print("KeyError: {}".format(er))


def make_set_groups(list_vk_id):
    count_common = len(list_vk_id)
    friends_group_set = set()
    for index, item in enumerate(list_vk_id):
        rr = make_list_groups(item)
        for i in rr:
            if i:
                friends_group_set.add(i)
        print('Обработано {}% друзей'.format(index * 100//count_common))

    return friends_group_set


def make_groups_describe_list(iterable_object):
    result_list = []
    count_unique_groups = len(iterable_object)
    for index, item in enumerate(iterable_object):
        result_list.append(content_groups(item))
        print('Обработано {}% уникальных групп'.format(index * 100 // count_unique_groups))
    return result_list


def resolve_name(screen_name):
    method = 'utils.resolveScreenName'
    fields_param = dict(screen_name=screen_name)
    response = get_vk_request(REQUEST_URL, method, fields_in_param=fields_param)
    if not response:
        print('Пользователь, с таким никнеймом - не существует!')
        return 'error'
    elif response['type'] != 'user':
        print("Это не пользователь, а {}!".format(response['type']))
        return 'error'
    else:
        return response['object_id']


def detect_deactivated_user(client_id):
    method = 'users.get'
    fields_param = dict(user_id=client_id)
    response = get_vk_request(REQUEST_URL, method, fields_in_param=fields_param)[0]
    if 'deactivated' in response:
        print('Пользователь c id {}- деактивирован.'.format(response['id']))
        return True
    else:
        return False


if __name__ == '__main__':
    client_id = input("ВВедите исследуемый VK_ID: ")
    if not client_id.isdigit():
        client_id = resolve_name(client_id)
    if client_id is 'error':
        exit(3)

    if detect_deactivated_user(client_id):
        exit(4)

    list_friends = make_list_friends(client_id)
    friends_group_set = make_set_groups(list_friends)
    list_id = [client_id]
    user_group_set = make_set_groups(list_id)

    unique_groups = user_group_set - friends_group_set

    result_list = make_groups_describe_list(unique_groups)

    with open('groups.json', 'w', encoding='utf-8') as file:
            json.dump(result_list, file)

    with open('groups.json', 'r', encoding='utf-8') as file:
        print(json.load(file))
