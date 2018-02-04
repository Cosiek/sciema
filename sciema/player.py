#!/usr/bin/env python
# encoding: utf-8

from collections import deque
from random import randint


class Player(object):

    def __init__(self, name, connection):
        self.name = name
        self.connection = connection
        self.connection.player_name = name
        self.connected = True

        self.requested_position = None  # indicates if player is on the move
        self.invalid_tries = 0
        self.history = deque(maxlen=5)
        self.is_winner = False

        self.look = self.get_new_look()

    def request_position(self, position):
        self.requested_position = position
        self.invalid_tries = 0

    def invalid_move(self):
        self.requested_position = None
        self.invalid_tries += 1
        return self.invalid_tries

    def settle(self):
        self.set_position(self.requested_position)
        self.requested_position = None

    def set_position(self, position):
        if position is not None:
            self.history.append(position)

    @property
    def is_moving(self):
        return self.requested_position is not None

    @property
    def position(self):
        return self.history[-1] if self.history else None

    def to_dct(self):
        return {'name': self.name, 'connected': self.connected,
                'position': self.position, 'is_winner': self.is_winner,
                'look': self.look}

    def get_new_look(self):
        return {
            'color': (randint(0, 255), randint(0, 255), randint(0, 255)),
            'icon': chr(randint(8192, 11263)),
        }
