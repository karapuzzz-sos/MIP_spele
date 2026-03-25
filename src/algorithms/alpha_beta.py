from src.game.game_logic import possible_moves, apply_move, is_game_over
from src.algorithms.heuristic import heuristic

def alpha_beta_value(state, depth, alpha, beta):
    # Ja spēle beigusies vai dziļums 0
    if depth == 0 or is_game_over(state):
        return heuristic(state), 1
    evaluated = 0
    best = None
    # Ja gājiens ir datoram (maksimizējam)
    if state["turn"] == "computer":
        for m in possible_moves(state):
            child = apply_move(state, m)
            value, cnt = alpha_beta_value(child, depth - 1, alpha, beta)
            evaluated = evaluated + cnt
            # Ja pirmā vērtība vai labāka
            if best is None or value > best:
                best = value
            # Atjaunojam alpha
            if alpha is None or best > alpha:
                alpha = best
            # Alfa-beta nogriešana
            if beta is not None and alpha >= beta:
                break
    # Ja gājiens ir cilvēkam (minimizējam)
    else:
        for m in possible_moves(state):
            child = apply_move(state, m)
            value, cnt = alpha_beta_value(child, depth - 1, alpha, beta)
            evaluated = evaluated + cnt
            # Ja pirmā vērtība vai mazāka
            if best is None or value < best:
                best = value
            # Atjaunojam beta
            if beta is None or best < beta:
                beta = best
            # Alfa-beta nogriešana
            if alpha is not None and alpha >= beta:
                break
    return best, evaluated

def choose_move_alpha_beta(state, depth):
    moves = possible_moves(state)
    if len(moves) == 0:
        return None, 0, 0
    evaluated_total = 0
    alpha = None
    beta = None
    best_move = None
    best_value = None
    for m in moves:
        child = apply_move(state, m)
        value, cnt = alpha_beta_value(child, depth - 1, alpha, beta)
        evaluated_total = evaluated_total + cnt
        if best_value is None:
            best_value = value
            best_move = m
        else:
            if state["turn"] == "computer":
                if value > best_value:
                    best_value = value
                    best_move = m
                if alpha is None or best_value > alpha:
                    alpha = best_value
            else:
                if value < best_value:
                    best_value = value
                    best_move = m
                if beta is None or best_value < beta:
                    beta = best_value
    return best_move, best_value, evaluated_total