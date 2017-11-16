#!/usr/bin/env python
# encoding: utf-8


class Player(object):

    def __init__(self, name, connection):
        self.name = name
        self.connection = connection
        self.connection.player_name = name
        self.connected = True

    def to_dct(self):
        return {'name': self.name, 'connected': self.connected}
