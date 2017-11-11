#!/usr/bin/env python
# encoding: utf-8

import json

import tornado.websocket


GAMES = {}
CLIENTS = []


class GameConnectionHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
            return

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
        CLIENTS.remove(self)
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

        return not bool(errors), data, {'errors': errors}
