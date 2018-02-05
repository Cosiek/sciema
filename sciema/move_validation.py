#!/usr/bin/env python
# encoding: utf-8

from copy import deepcopy
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

# NOTE: keep all functions that should be used for move validation
# below this statement
imported = set(dir())


def always_true(*args, **kwargs):
    return True, kwargs['requested_pos']


def always_false(*args, **kwargs):
    return False, kwargs['player'].position


def fifty_fifty(*args, **kwargs):
    return (always_true(*args, **kwargs) if randint(0, 1)
            else always_false(*args, **kwargs))


def three_to_one(*args, **kwargs):
    return (always_true(*args, **kwargs) if randint(0, 3)
            else always_false(*args, **kwargs))


def skip_over(*args, **kwargs):
    requested_pos = deepcopy(kwargs['requested_pos'])
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
    if _is_outside_map(requested_pos, world):
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


def _is_outside_map(position, world):
    return (position[0] < 0 or world.x_size <= position[0] or
            position[1] < 0 or world.y_size <= position[1])


def only_vertical(*args, **kwargs):
    if kwargs['direction'] in ('up', 'down'):
        return always_true(*args, **kwargs)
    return always_false(*args, **kwargs)


def only_horizontal(*args, **kwargs):
    if kwargs['direction'] in ('up', 'down'):
        return always_false(*args, **kwargs)
    return always_true(*args, **kwargs)


def keep_off_the_grass(*args, **kwargs):
    if kwargs['next_field'] == u'☘':
        return always_false(*args, **kwargs)
    return always_true(*args, **kwargs)


def no_swimming(*args, **kwargs):
    if kwargs['next_field'] == u'〰':
        return always_false(*args, **kwargs)
    return always_true(*args, **kwargs)

# NOTE: keep all functions that should be used for move validation
# above this statement
_validator_names = set(dir()) - imported - set(('imported',))
_locals = locals()
VALIDATORS = [_locals[vn] for vn in _validator_names if not vn.startswith('_')]

APPROVE = [always_true, fifty_fifty, three_to_one]
DISAPPROVE = [always_false, bounce_back, skip_over]
MOVE = [always_true, three_to_one, skip_over, bounce_back]
