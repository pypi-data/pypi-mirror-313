import requests
import pyzbar.pyzbar as pyzbar
import os

def image_to_string(image_path, action_type):
    with open(image_path, 'rb') as file:
        data = {'type': action_type}
        files = {'image': (os.path.basename(image_path), file)}
        user_agent = {'User-agent': 'Mozilla/5.0'}
        proxies = {'http': '127.0.0.1:7890'}
        response = requests.post("http://39.103.59.220/ocr/orc_receive_img/", files=files, data=data, headers=user_agent, proxies=proxies)
    return response.json()