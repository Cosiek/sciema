#!/usr/bin/env python
# encoding: utf-8


from random import choice, randint, shuffle

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
    return u''


def back_to_beginning(*args, **kwargs):
    kwargs['player'].set_position(kwargs['world'].get_start_position())
    return u'{} wraca na start'.format(kwargs['player'].name)


def sent_others_to_beginning(*args, **kwargs):
    world = kwargs['world']
    start = world.get_start_position()
    for player in world.players.values():
        if player.name != kwargs['player'].name:
            player.set_position(start)
    return u'wszyscy oprócz {} wracają na start'.format(kwargs['player'].name)


def mix_map(*args, **kwargs):
    kwargs['world'].generate_random_map()
    return u'{} nadepnął na przetasowanie mapy'.format(kwargs['player'].name)


def change_move_validation_rules(*args, **kwargs):
    kwargs['world'].set_move_validation_rules()
    return u'{}: zmienił reguły przchodzenia'.format(kwargs['player'].name)


def change_settle_actions(*args, **kwargs):
    kwargs['world'].set_settle_actions()
    return u'{}: zmienił reguły obszarów'.format(kwargs['player'].name)


def swap_players_positions(*args, **kwargs):
    player1 = kwargs['player']
    player_names = list(kwargs['world'].players.keys())
    player_names.remove(player1.name)
    if not player_names:
        return u'nic się nie stało'
    player2 = kwargs['world'].players[choice(player_names)]
    pos2 = player2.position
    player2.set_position(player1.position)
    player1.set_position(pos2)
    return u'{} zamienił się pozycjami z {}'.format(player1.name, player2.name)


def shuffle_positions(*args, **kwargs):
    players = kwargs['world'].players
    positions = [p.position for p in players.values()]
    shuffle(positions)
    for player in players.values():
        player.set_position(positions.pop())
    return u'{} przetasował pozycje graczy'.format(kwargs['player'].name)


def hide_finish(*args, **kwargs):
    world = kwargs['world']
    # put something new where finish is
    if not world.finishes:
        return u'{} nic nie zrobił!'.format(kwargs['player'].name)
    finish_position = world.finishes.pop()
    rfi = world.get_random_field_iterator()
    world.map[finish_position[0]][finish_position[1]] = next(rfi)
    return u'{} zniknął metę!'.format(kwargs['player'].name)


def copy_finish(*args, **kwargs):
    world = kwargs['world']
    row = randint(1, world.x_size - 2)
    col = randint(1, world.y_size - 2)
    world.map[row][col] = chr(127937)
    world.finishes.append([row, col])
    return u'{} zrobił kolejną metę'.format(kwargs['player'].name)


def move_finish(*args, **kwargs):
    hide_finish(*args, **kwargs)
    copy_finish(*args, **kwargs)
    return u'{} przeniósł metę'.format(kwargs['player'].name)


def swap_start_and_finish(*args, **kwargs):
    world = kwargs['world']
    if not (world.starts and world.finishes):
        return u'{} nie zamienił niczego z niczym'.format(kwargs['player'].name)
    start = world.starts.pop()
    finish = world.finishes.pop()
    world.starts.append(finish)
    world.finishes.append(start)
    world.map[start[0]][start[1]] = chr(127937)  # finish
    world.map[finish[0]][finish[1]] = chr(127987)  # start
    return u'{} zamienił start z metą'.format(kwargs['player'].name)


def go_back_in_time(*args, **kwargs):
    player = kwargs['player']
    player.set_position(player.history[0])
    return u'{} cofnął się w czasie'.format(kwargs['player'].name)


def total_random(*args, **kwargs):
    action = choice(SETTLE_ACTIONS)
    return u'Wyszło, że ' + action(*args, **kwargs)


def move_to_first_column(*args, **kwargs):
    player = kwargs['player']
    player.set_position([player.history[-1][0], 0])
    return u'{} leci do pierwszej kolumny'.format(kwargs['player'].name)


def move_to_first_row(*args, **kwargs):
    player = kwargs['player']
    player.set_position([0, player.history[-1][1]])
    return u'{} leci do pierwszego wiersza'.format(kwargs['player'].name)


def move_everyone_to_first_column(*args, **kwargs):
    for player in kwargs['world'].players.values():
        move_to_first_column(player=player)
    return u'{} wysyła wszystkich do pierwszej kolumny'.format(kwargs['player'].name)


def move_everyone_to_first_row(*args, **kwargs):
    for player in kwargs['world'].players.values():
        move_to_first_row(player=player)
    return u'{} wysyła wszystkich do pierwszego rzędu'.format(kwargs['player'].name)


def step_on_someone(*args, **kwargs):
    this_player = kwargs['player']
    for player in kwargs['world'].players.values():
        if (player.name != this_player.name and
                player.position == this_player.position):
            player.set_position(kwargs['world'].get_start_position())
    return u'{} nie chce towarzystwa w tym miejscu.'.format(this_player.name)

# NOTE: keep all functions that should be used for move validation
# above this statement
_validator_names = set(dir()) - imported - set(('imported',))
_locals = locals()
SETTLE_ACTIONS = [_locals[vn] for vn in _validator_names]

def finish_off(*args, **kwargs):
    kwargs['world'].game.state = kwargs['world'].game.states.finished
    kwargs['player'].is_winner = True
    return u'{} wygrywa'.format(kwargs['player'].name)
