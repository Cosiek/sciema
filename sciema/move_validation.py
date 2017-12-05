#!/usr/bin/env python
# encoding: utf-8


from random import randint

"""
Keyword arguments passed to move validation function

kwargs = {
    'world': self,
    'player': player,
    'curr_field': curr_field,
    'next_field': next_field,
    'requested_pos': requested_pos,
    'direction': direction
}
"""


def always_true(*args, **kwargs):
    return True, kwargs['requested_pos']


def always_false(*args, **kwargs):
    return False, kwargs['player'].position


def fifty_fifty(*args, **kwargs):
    return (always_true(*args, **kwargs) if randint(0, 1)
            else always_false(*args, **kwargs))


def skip_over(*args, **kwargs):
    requested_pos = kwargs['requested_pos'].copy()
    direction = kwargs['direction']
    world = kwargs['world']
    if direction == 'up':
        requested_pos[0] -= 1
    elif direction == 'down':
        requested_pos[0] += 1
    elif direction == 'left':
        requested_pos[1] -= 1
    elif direction == 'right':
        requested_pos[1] += 1
    # check walking outside of world
    if (requested_pos[0] < 0 or world.x_size <= requested_pos[0] or
            requested_pos[1] < 0 or world.y_size <= requested_pos[1]):
        return always_true(*args, **kwargs)
    return True, requested_pos


def bounce_back(*args, **kwargs):
    opposite_directions = {
        'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'
    }
    kwargs['direction'] = opposite_directions[kwargs['direction']]
    _, req_pos = skip_over(*args, **kwargs)
    kwargs['requested_pos'] = req_pos
    return skip_over(*args, **kwargs)


def only_vertical(*args, **kwargs):
    if kwargs['direction'] in ('up', 'down'):
        return always_true(*args, **kwargs)
    return always_false(*args, **kwargs)


def only_horizontal(*args, **kwargs):
    if kwargs['direction'] in ('up', 'down'):
        return always_false(*args, **kwargs)
    return always_true(*args, **kwargs)


def keep_off_the_grass(*args, **kwargs):
    if kwargs['next_field'] == 'grass':
        return always_false(*args, **kwargs)
    return always_true(*args, **kwargs)
