import requests
import os
import random
from dotenv import load_dotenv

VK_API_URL = 'https://api.vk.com/method/'
VK_API_VERSION = '5.131'


def get_random_comic():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    max_num = response.json()['num']
    download_num = random.randint(1, max_num)
    url = 'https://xkcd.com/{}/info.0.json'.format(str(download_num))
    response = requests.get(url)
    response.raise_for_status()
    response_comic = response.json()
    img_link = response_comic['img']
    filename = img_link.split('/')[-1]
    img_comic = requests.get(img_link)
    with open(filename, 'wb') as file:
        file.write(img_comic.content)
    caption = response_comic['alt']
    return filename, caption


def check_vk_response(response):
    if 'error' in response:
        raise requests.HTTPError(response['error']['error_msg'])


def upload_photo_to_server_vk(token, filename):
    method = 'photos.getWallUploadServer'
    url = f'https://api.vk.com/method/{method}'
    payload = {'access_token': token,
               'v': VK_API_VERSION}
    response = requests.get(url, params=payload).json()
    check_vk_response(response)
    upload_url = response['response']['upload_url']
    with open(filename, 'rb') as image_file_descriptor:
        upload_response = requests.post(upload_url, files={'photo': image_file_descriptor}).json()
        server = upload_response['server']
        photo = upload_response['photo']
        hash_value = upload_response['hash']
        return server, photo, hash_value


def save_photo_on_server(token, server, photo, hash_value):
    method = 'photos.saveWallPhoto'
    url = f'https://api.vk.com/method/{method}'
    payload = {'access_token': token,
               'v': VK_API_VERSION,
               'server': server,
               'photo': photo,
               'hash': hash_value}
    response = requests.post(url, params=payload).json()
    check_vk_response(response)
    return response['response'][0]['id']


def on_wall_post(token, group_id, message, attachments):
    method = 'wall.post'
    url = f'https://api.vk.com/method/{method}'
    payload = {'access_token': token,
               'v': VK_API_VERSION,
               'owner_id': f'-{group_id}',
               'from_group': group_id,
               'message': message,
               'attachments': attachments}
    response = requests.post(url, params=payload).json()
    check_vk_response(response)


def main():
    load_dotenv()
    token = os.environ['VK_TOKEN']
    group_id = os.environ['GROUP_ID']
    filename, caption = get_random_comic()
    try:
        server, photo, hash_value = upload_photo_to_server_vk(token, filename)
    finally:
        os.remove(filename)
    attachments = 'photo2094408_{}'.format(save_photo_on_server(token, server, photo, hash_value))
    on_wall_post(token, group_id, caption, attachments)


if __name__ == '__main__':
    main()
