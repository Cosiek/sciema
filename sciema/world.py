#!/usr/bin/env python
# encoding: utf-8


from random import shuffle


FIELD_TYPES = {
    'start': {'color': (255, 255, 255), 'possible': 0},
    'grass': {'color': (0, 255, 50), 'possible': 5},
    'water': {'color': (0, 50, 252), 'possible': 5},
    'lava': {'color': (255, 50, 50), 'possible': 1},
    'rock': {'color': (200, 150, 150), 'possible': 1},
    'finish': {'color': (0, 0, 0), 'possible': 0},
}


class World(object):

    def __init__(self, players, size=(25, 25)):
        self.x_size, self.y_size = size

        self.map = []
        self.generate_random_map()

        self.players = players
        start_position = self.get_start_position()
        for p in players.values():
            p.set_position(start_position)

    def generate_random_map(self):
        map_ = []
        rfi = self.get_random_field_iterator()
        for y in range(self.y_size):
            row = []
            for x in range(self.x_size):
                row.append(next(rfi))
            map_.append(row)
        # add start and finish fields
        middle_row_idx, _ = self.get_start_position()
        map_[middle_row_idx][0] = 'start'
        map_[middle_row_idx][self.x_size - 1] = 'finish'
        # set map
        self.map = map_

    def get_start_position(self):
        return [int((self.y_size + 1) / 2), 0]

    @staticmethod
    def get_random_field_iterator():
        # generate poll with right number of fields of each type
        poll = []
        for key, val in FIELD_TYPES.items():
            if val.get('possible'):
                poll.extend([key] * val.get('possible'))
        while True:
            shuffle(poll)
            for field_name in poll:
                yield field_name

    def to_dct(self):
        return {
            'size': (self.x_size, self.y_size),
            'field_types': FIELD_TYPES,
            'map': self.map,
        }
