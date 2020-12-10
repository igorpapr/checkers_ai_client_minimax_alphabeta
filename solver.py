from copy import deepcopy

from checkers.game import Game


def next_move(game: Game, depth, maximizing_player, test):
    optimal_move = None
    a = float('-inf')
    for move in game.get_possible_moves():
        new_game = deepcopy(game)
        new_game.move(move)
        b = -_minimax(new_game, depth - 1, new_game.whose_turn(), maximizing_player, float('-inf'), float('+inf'), test)
        if a < b:
            a = b
            optimal_move = move
    return optimal_move


def _minimax(game: Game, depth, player_num, maximizing_player, alpha, beta, test):
    if depth == 0 or game.is_over():
        return heuristic(game, maximizing_player, test)

    if player_num == maximizing_player:
        value = float('-inf')
        for move in game.get_possible_moves():
            new_game = deepcopy(game)
            new_game.move(move)
            value = max(value,
                        _minimax(new_game, depth - 1, new_game.whose_turn(), maximizing_player, alpha, beta, test))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('+inf')
        for move in game.get_possible_moves():
            new_game = deepcopy(game)
            new_game.move(move)
            value = min(value,
                        _minimax(new_game, depth - 1, new_game.whose_turn(), maximizing_player, alpha, beta, test))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value


def heuristic(game: Game, player_num, test):
    our_pieces = game.board.searcher.get_pieces_by_player(player_num)
    enemy_pieces = game.board.searcher.get_pieces_by_player(1 if player_num == 2 else 2)
    kings = filter(lambda p: p.king, our_pieces)
    middle_box = filter(lambda p: p.player == player_num and p.position in [14, 15, 18, 19], our_pieces)
    middle_rows = filter(lambda p: p.player == player_num and p.position in [13, 16, 17, 20], our_pieces)

    if player_num == 1:
        back_row = filter(lambda p: p.position in [1, 2, 3, 4], our_pieces)
    else:
        back_row = filter(lambda p: p.position in [29, 30, 31, 32], our_pieces)

    our_pieces = len(our_pieces)
    enemy_pieces = len(enemy_pieces)
    kings = len(list(kings))
    back_row = len(list(back_row))
    middle_box = len(list(middle_box))
    middle_rows = len(list(middle_rows))

    res = -(5 * our_pieces
            - 1 * enemy_pieces
            + 7.75 * kings
            + 4 * back_row
            + 2.5 * middle_box
            + 0.5 * middle_rows)
    if test:
        return our_pieces
    else:
        return res
