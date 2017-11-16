#!/usr/bin/env python
# encoding: utf-8

from collections import deque

class Player(object):

    def __init__(self, name, connection):
        self.name = name
        self.connection = connection
        self.connection.player_name = name
        self.connected = True

        self.history = deque(maxlen=5)

    def set_position(self, position):
        self.history.append(position)

    @property
    def position(self):
        return self.history[-1] if self.history else None

    def to_dct(self):
        return {'name': self.name, 'connected': self.connected,
                'position': self.position}
