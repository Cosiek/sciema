#!/usr/bin/env python
# encoding: utf-8

import os
import socket

import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options, parse_command_line


CURRENT_DIR = os.path.dirname(__file__)


define('port', default=8888, help=u'Port na którym serwer ma działać', type=int)


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("home.html")


STATIC_ROOT = os.path.join(CURRENT_DIR, "static")


app = tornado.web.Application(
    [
        (r'/', IndexHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': STATIC_ROOT}),
    ],
    template_path=os.path.join(CURRENT_DIR, "templates"),
)


if __name__ == '__main__':
    # check current ip:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets

    parse_command_line()
    print(u'Zaczynam pracę na {}:{}'.format(s.getsockname()[0], options.port))
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
