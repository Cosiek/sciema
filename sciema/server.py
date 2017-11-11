#!/usr/bin/env python
# encoding: utf-8

import json
import os
import socket

import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options, parse_command_line


CURRENT_DIR = os.path.dirname(__file__)
define('port', default=8888, help=u'Port na którym serwer ma działać', type=int)

GAMES = {'A': [], 'B': []}
CLIENTS = []


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("home.html", games=GAMES)


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def __init__(self):
        super()
        self.game = None

    # connections handling ------------

    def open(self, *args):
        print('Nowy klient')
        self.stream.set_nodelay(True)
        CLIENTS.append(self)

    def on_message(self, message):
        print('Nowa wiadomość: ', message)
        # validate input data
        is_valid, data, errors = self.basic_validate(message)
        if not is_valid:
            self.snd(errors)

        action = data.get('action')
        if action == 'new_game':
            if data['game'] in GAMES:
                # validation error
                pass
            else:
                GAMES[data['game']] = [data['player'],]
        else:
            GAMES[data['game']].append(data['player'])

        self.game = GAMES[data['game']]
        self.write_message(json.dumps(GAMES))

    def on_close(self):
        print('Ucieczka!')

    def check_origin(self, origin):
        return True

    def snd(self, data_dict):
        self.write_message(json.dumps(data_dict))

    # data handling -------------------

    @staticmethod
    def basic_validate(message):
        errors = []
        # load json from message
        try:
            data = json.loads(message)
        except json.decoder.JSONDecodeError:
            errors.append('JSON decode error')
            return False, {'errors': errors}, None

        for key in ['action', 'game']:
            if not data.get(key):
                errors.append('Missing parameter {}'.format(key))

        return bool(errors), {'errors': errors}, data



STATIC_ROOT = os.path.join(CURRENT_DIR, "static")


app = tornado.web.Application(
    [
        (r'/', IndexHandler),
        (r'/websocket', WebSocketHandler),
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
