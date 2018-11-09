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
    'Host': 'fanyi.baidu.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
}

LANGS = {
    'zh': 'zh',
    'en': 'en'
}

URL = 'https://fanyi.baidu.com/transapi'


def parse(response, **kwargs):
    if response['status'] == 0:
        try:
            data = json.loads(response.pop('data'))
            targets = [t['dst'] for t in data]
        except (JSONDecodeError, KeyError, AttributeError) as e:
            response.update(status=1, error=e)
        else:
            response.update(target='\n'.join(targets))
    response.update(**kwargs)
    return response


def make_request(body, **kwargs):
    params = {}
    params['from'] = LANGS[body['from']]
    params['to'] = LANGS[body['to']]
    params['query'] = body['query']
    params['source'] = 'txt'

    return HTTPRequest(url=URL, method='POST', headers=HEADERS,
                       body=urlencode(params), **kwargs)
