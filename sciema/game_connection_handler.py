#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

import json

import tornado.websocket

from game import Game


GAMES = {}
CLIENTS = []


class GameConnectionHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = None
        self.player_name = None

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

    def on_close(self):
        CLIENTS.remove(self)
        if self.game:
            self.game.player_disconnected(self)
        print('Ucieczka!')

    def check_origin(self, origin):
        return True

    # data handling -------------------

    def basic_validate(self, message):
        errors = []
        # load json from message
        try:
            data = json.loads(message)
        except json.decoder.JSONDecodeError:
            self.err('JSON decode error')
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
                # validation error
                self.err('Game already exists. Choose another name')
            else:
                game = Game(data['game'], self)
                if game.add_player(self, data):
                    GAMES[data['game']] = game
                    self.snd(game.get_game_state())
        elif data['action'] == 'join_game':
            if data['game'] in GAMES:
                game = GAMES[data['game']]
                if game.add_player(self, data):
                    self.snd_a(game.get_game_state())
            else:
                # validation error
                self.err('Game does not exist')
        else:
            # pass this to game object
            if self.game is None:
                self.err('Inadequate action')
            else:
                self.snd_a(self.game.handle_action(data))

    # helpers -------------------------

    def err(self, message):
        self.snd({'errors': [message]})

    def snd(self, data_dict):
        self.write_message(json.dumps(data_dict))

    def snd_a(self, data_dict):
        if self.game:
            for client in self.game.players.values():
                client.snd(data_dict)
