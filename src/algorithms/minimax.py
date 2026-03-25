from src.game.game_logic import possible_moves, apply_move, is_game_over
from src.algorithms.heuristic import heuristic


def minimax_value(state, depth):
    # Ja spēle beigusies vai sasniegts dziļums
    if depth == 0 or is_game_over(state):
        return heuristic(state), 1
    # Skaitām novērtētās virsotnes
    evaluated = 0
    # Labākā vērtība sākumā nav zināma
    best = None
    # Ja gājiens ir datoram
    if state["turn"] == "computer":
        for m in possible_moves(state):
            child = apply_move(state, m)
            value, cnt = minimax_value(child, depth - 1)
            evaluated = evaluated + cnt
            # Ja pirmā vērtība vai labāka
            if best is None or value > best:
                best = value
    # Ja gājiens ir cilvēkam
    else:
        for m in possible_moves(state):
            child = apply_move(state, m)
            value, cnt = minimax_value(child, depth - 1)
            evaluated = evaluated + cnt
            # Ja pirmā vērtība vai mazāka
            if best is None or value < best:
                best = value
    return best, evaluated

def choose_move_minimax(state, depth):
    moves = possible_moves(state)
    if len(moves) == 0:
        return None, 0, 0
    evaluated_total = 0
    best_move = None
    best_value = None
    for m in moves:
        child = apply_move(state, m)
        value, cnt = minimax_value(child, depth - 1)
        evaluated_total = evaluated_total + cnt
        # Ja pirmais gājiens
        if best_value is None:
            best_value = value
            best_move = m
        else:
            # Ja dators ir gājienā → maksimizē
            if state["turn"] == "computer":
                if value > best_value:
                    best_value = value
                    best_move = m
            # Ja cilvēks → minimizē
            else:
                if value < best_value:
                    best_value = value
                    best_move = m
    return best_move, best_value, evaluated_total