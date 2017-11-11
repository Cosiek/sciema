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
        data = self.basic_validate(message)
        if data is None:
            return

        self.dispatch(data)

        self.write_message(json.dumps(GAMES))

    def on_close(self):
        CLIENTS.remove(self)
        print('Ucieczka!')

    def check_origin(self, origin):
        return True

    def snd(self, data_dict):
        self.write_message(json.dumps(data_dict))

    # data handling -------------------

    def basic_validate(self, message):
        errors = []
        # load json from message
        try:
            data = json.loads(message)
        except json.decoder.JSONDecodeError:
            errors.append('JSON decode error')
            self.snd({'errors': errors})
            return None

        for key in ['action', 'game']:
            if not data.get(key):
                errors.append('Missing parameter {}'.format(key))

        if errors:
            self.snd({'errors': errors})
            return None
        return data

    def dispatch(self, data):
        if data['action'] == 'new_game':
            if data['game'] in GAMES:
                if data['game'] in GAMES:
                    # validation error
                    self.snd(
                        {'errors': ['Game already exists. Choose another name']}
                    )
                else:
                    GAMES[data['game']] = [data['player'],]
        elif data['action'] == 'join_game':
            if data['game'] in GAMES:
                self.game = GAMES[data['game']]
            else:
                # validation error
                self.snd({'errors': ['Game does not exist']})
        else:
            # pass this to game object
            if self.game is None:
                self.snd({'errors': ['Unadeqate action']})
                return
            #self.game.handle_action(data)
