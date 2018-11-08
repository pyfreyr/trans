import json
from json.decoder import JSONDecodeError

import tornado.ioloop
from tornado.options import define, options
from tornado.web import RequestHandler, Application

from api import API_VENDORS
from trans_client import get_content

define('port', default='8888', type=int)


class TransHandler(tornado.web.RequestHandler):
    async def post(self, *args, **kwargs):
        try:
            params = json.loads(self.request.body)
            vendor = params['vendor']
        except (JSONDecodeError, KeyError):
            self.set_status(400)
        else:
            trans_handler = API_VENDORS[vendor]
            request = trans_handler.make_request(params)
            response = await get_content(request)
            res = trans_handler.parse(response, **params)

            self.write(json.dumps(res, ensure_ascii=False, indent=4))


def make_app():
    return Application(
        handlers=[
            (r'/v1/trans', TransHandler),
        ],
        # debug=True
    )


if __name__ == '__main__':
    options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
    # try:
    #     tornado.ioloop.IOLoop.current().start()
    # except KeyboardInterrupt:
    #     tornado.ioloop.IOLoop.current().stop()
