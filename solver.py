import logging
from copy import deepcopy

from checkers.game import Game


def next_move(game: Game, depth):
    optimal_move = None
    a = float('-inf')
    for move in game.get_possible_moves():
        new_game = deepcopy(game)
        new_game.move(move)
        b = -minimax(new_game, depth - 1, new_game.whose_turn())  # TODO: multiple moves by single player
        if a < b:
            a = b
            optimal_move = move
    return optimal_move


def minimax(game: Game, depth, player_num) -> float:
    if depth == 0 or game.is_over():
        return heuristic(game, player_num)
    a = float('-inf')
    for move in game.get_possible_moves():
        new_game = deepcopy(game)
        new_game.move(move)
        b = -minimax(new_game, depth - 1, new_game.whose_turn())
        a = max(a, b)
    return a


def heuristic(game: Game, player_num=1):
    return len(game.board.searcher.get_pieces_by_player(player_num))
