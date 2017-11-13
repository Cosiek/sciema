#!/usr/bin/env python
# encoding: utf-8


class Game(object):

    class states:
        waiting = 'waiting'
        game_on = 'game_on'
        finished = 'finished'

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.players = {}

        self.state = self.states.waiting

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

    def player_disconnected(self, connection):
        pass

    def handle_action(self, data):
        pass

    def get_game_state(self):
        return {
            'name': self.name,
            'owner': self.owner.player_name,
            'players': list(self.players.keys()),
            'state': self.state,
        }
