#!/usr/bin/env python
# encoding: utf-8


class Game(object):

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.players = {}

    def add_player(self, connection, data):
        # validate data
        if not data.get('player'):
            connection.err('Invalid data: missing player name')
            return False
        if data['player'] in self.players:
            connection.err('Player name already taken')
            return False
        # set data
        connection.player_name = data['player']
        self.players[data['player']] = connection
        connection.game = self
        return True

    def handle_action(self, data):
        pass
