import json
import requests


def get_img():
    url = 'https://www.wudada.online/Api/SjTx'
    response = requests.get(url)
    res = json.loads(response.text)
    img_data = res['data']
    return img_data