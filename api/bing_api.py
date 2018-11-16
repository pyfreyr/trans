import json
from json.decoder import JSONDecodeError
from urllib.parse import urlencode

from tornado.httpclient import HTTPRequest

HEADERS = {
    'Accept': '*/*',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,de;q=0.5',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://cn.bing.com',
    'referer': 'https://cn.bing.com/translator/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
}

LANGS = {
    'zh': 'zh-CHS',
    'en': 'en'
}

URL = 'https://cn.bing.com/ttranslate'


def parse(response, **kwargs):
    if response['status'] == 0:
        try:
            data = json.loads(response.pop('data'))
            target = data['translationResponse']
        except (JSONDecodeError, KeyError) as e:
            response.update(status=1, error=str(e))
        else:
            response.update(target=target)
            response.update(**kwargs)
    return response


def make_request(body, **kwargs):
    params = {}
    params['from'] = LANGS[body['from']]
    params['to'] = LANGS[body['to']]
    params['text'] = body['query']

    return HTTPRequest(url=URL, method='POST', headers=HEADERS,
                       body=urlencode(params), **kwargs)
