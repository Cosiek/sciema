#!/usr/bin/env python
# encoding: utf-8


from random import choice, randint

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
    return


def back_to_beginning(*args, **kwargs):
    kwargs['player'].set_position(kwargs['world'].get_start_position())


def sent_others_to_beginning(*args, **kwargs):
    world = kwargs['world']
    start = world.get_start_position()
    for player in world.players.values():
        if player.name != kwargs['player'].name:
            player.set_position(start)


def mix_map(*args, **kwargs):
    kwargs['world'].generate_random_map()


def change_move_validation_rules(*args, **kwargs):
    kwargs['world'].set_move_validation_rules()


def change_settle_actions(*args, **kwargs):
    kwargs['world'].set_settle_actions()


def swap_players_positions(*args, **kwargs):  # TODO - test with multiple players
    player1 = kwargs['player']
    player_names = list(kwargs['world'].players.keys())
    player_names.remove(player1.name)
    if not player_names:
        return
    player2 = kwargs['world'].players[choice(player_names)]
    pos2 = player2.position
    player2.set_position(player1.position)
    player1.set_position(pos2)


def hide_finish(*args, **kwargs):
    world = kwargs['world']
    # put something new where finish is
    middle_row_idx, _ = world.get_start_position()
    rfi = world.get_random_field_iterator()
    world.map[middle_row_idx][world.x_size - 1] = next(rfi)


def copy_finish(*args, **kwargs):
    world = kwargs['world']
    row = randint(1, world.x_size - 2)
    col = randint(1, world.y_size - 2)
    world.map[row][col] = 'finish'


def move_finish(*args, **kwargs):
    hide_finish(*args, **kwargs)
    copy_finish(*args, **kwargs)


def swap_start_and_finish(*args, **kwargs):
    world = kwargs['world']
    middle_row_idx, _ = world.get_start_position()
    world.map[middle_row_idx][0] = 'finish'
    world.map[middle_row_idx][world.x_size - 1] = 'start'


def go_back_in_time(*args, **kwargs):
    player = kwargs['player']
    player.set_position(player.history[0])


def total_random(*args, **kwargs):
    action = choice(SETTLE_ACTIONS)
    return action(*args, **kwargs)


def move_to_first_column(*args, **kwargs):
    player = kwargs['player']
    player.set_position([player.history[-1][0], 0])


def move_to_first_row(*args, **kwargs):
    player = kwargs['player']
    player.set_position([0, player.history[-1][1]])


def move_everyone_to_first_column(*args, **kwargs):
    for player in kwargs['world'].players.values():
        move_to_first_column(player=player)


def move_everyone_to_first_row(*args, **kwargs):
    for player in kwargs['world'].players.values():
        move_to_first_row(player=player)


# NOTE: keep all functions that should be used for move validation
# above this statement
_validator_names = set(dir()) - imported - set(('imported',))
_locals = locals()
SETTLE_ACTIONS = [_locals[vn] for vn in _validator_names]

for i in range(len(SETTLE_ACTIONS) * 4):
    SETTLE_ACTIONS.append(do_nothing)


def finish_off(*args, **kwargs):
    kwargs['world'].game.state = kwargs['world'].game.states.finished
    kwargs['player'].is_winner = True
    return do_nothing(*args, **kwargs)
