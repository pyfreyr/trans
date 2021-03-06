import json
from json.decoder import JSONDecodeError
from urllib.parse import urlencode

from tornado.httpclient import HTTPRequest

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,de;q=0.5',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'fanyi.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
}

LANGS = {
    'zh': 'zh-CHS',
    'en': 'en'
}

URL = 'https://fanyi.sogou.com/reventondc/translateV1'


def parse(response, **kwargs):
    if response['status'] == 0:
        try:
            data = json.loads(response.pop('data'))
            target = data['data']['translate']['dit']
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
