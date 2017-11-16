#!/usr/bin/env python
# encoding: utf-8

from player import Player
from world import World


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
        self.world = None

    def add_player(self, connection, data):
        # validate data
        if self.state != self.states.waiting:
            connection.err("The game is already on - it's to late to join")
            return False
        if not data.get('player'):
            connection.err('Invalid data: missing player name')
            return False
        if data['player'] in self.players:
            connection.err('Player name already taken')
            return False
        # set data
        self.players[data['player']] = Player(data['player'], connection)
        connection.game = self
        return True

    def player_disconnected(self, connection):
        # TODO
        pass

    def handle_action(self, data, connection):
        print(data)
        if data['action'] == 'run_game':
            if not connection is self.owner:
                connection.err("Only the owner can run a game")
                return False
            self.state = self.states.game_on
            self.world = World()
            response = self.get_game_state()
            response['world'] = self.world.to_dct()
            return response
        elif data['action'] == 'end-game':
            if not connection is self.owner:
                connection.err("Only the owner can finish a game")
                return False
            self.state = self.states.finished
            state = self.get_game_state()
            state['winner'] = connection.player_name
            return state

    def get_game_state(self):
        return {
            'name': self.name,
            'owner': self.owner.player_name,
            'players': [p.to_dct() for p in self.players.values()],
            'state': self.state,
        }
