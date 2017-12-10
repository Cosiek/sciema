#!/usr/bin/env python
# encoding: utf-8


from random import randint

"""
Keyword arguments passed to settle function

kwargs = {
    world: self,
    player: player,
    curr_field: curr_field,
}
"""

# NOTE: keep all functions that should be used for move validation
# below this statement
imported = set(dir())


def do_nothing(*args, **kwargs):
    return kwargs['player'].position


# NOTE: keep all functions that should be used for move validation
# above this statement
_validator_names = set(dir()) - imported - set(('imported',))
_locals = locals()
SETTLE_ACTIONS = [_locals[vn] for vn in _validator_names]


def finish_off(*args, **kwargs):
    kwargs['world'].game.state = kwargs['world'].game.states.finished
    kwargs['player'].is_winner = True
    return do_nothing(*args, **kwargs)
