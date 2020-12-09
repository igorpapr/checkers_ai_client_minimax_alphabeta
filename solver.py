from copy import deepcopy

from checkers.game import Game


def next_move(game: Game, depth, maximizing_player):
    optimal_move = None
    a = float('-inf')
    for move in game.get_possible_moves():
        new_game = deepcopy(game)
        new_game.move(move)
        b = -_minimax(new_game, depth - 1, new_game.whose_turn(), maximizing_player, float('-inf'), float('+inf'))
        if a < b:
            a = b
            optimal_move = move
    return optimal_move


def _minimax(game: Game, depth, player_num, maximizing_player, alpha, beta):
    if depth == 0 or game.is_over():
        return heuristic(game, player_num)

    if player_num == maximizing_player:
        value = float('-inf')
        for move in game.get_possible_moves():
            new_game = deepcopy(game)
            new_game.move(move)
            value = max(value, _minimax(new_game, depth - 1, new_game.whose_turn(), maximizing_player, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('+inf')
        for move in game.get_possible_moves():
            new_game = deepcopy(game)
            new_game.move(move)
            value = min(value, _minimax(new_game, depth - 1, new_game.whose_turn(), maximizing_player, alpha, beta))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value


def heuristic(game: Game, player_num):
    return len(game.board.searcher.get_pieces_by_player(player_num))
