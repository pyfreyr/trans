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
    'Host': 'fy.iciba.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
}

LANGS = {
    'zh': 'zh-CN',
    'en': 'en-US'
}

URL = 'http://fy.iciba.com/ajax.php'


def parse(response, **kwargs):
    if response['status'] == 0:
        try:
            data = json.loads(response.pop('data'))
            target = data['content']['out']
        except (JSONDecodeError, KeyError, AttributeError) as e:
            response.update(status=1, error=e)
        else:
            response.update(target=target)
    response.update(**kwargs)
    return response


def make_request(body, **kwargs):
    params = {}
    params['f'] = LANGS[body['from']]
    params['t'] = LANGS[body['to']]
    params['w'] = body['query']
    params['a'] = 'fy'
    url = '{}?{}'.format(URL, urlencode(params))

    return HTTPRequest(url=url, method='GET', headers=HEADERS, **kwargs)
