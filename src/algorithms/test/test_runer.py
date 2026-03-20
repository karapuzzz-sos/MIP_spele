import time

from src.game.game_state import create_state
from src.game.game_logic import apply_move, is_game_over, winner_text
from src.algorithms.minimax import choose_move_minimax
from src.algorithms.alpha_beta import choose_move_alpha_beta


# Funkcija, kas izvēlas algoritmu
def choose_algorithm_move(state, depth, algorithm_name):
    if algorithm_name == "Minimax":
        return choose_move_minimax(state, depth)
    else:
        return choose_move_alpha_beta(state, depth)


# Funkcija, kas izspēlē vienu pilnu automātisko testu
def run_one_test(stones, starter, depth, algorithm_name):
    # Izveido sākuma stāvokli
    state = create_state(stones, starter)

    # Ja nevar izveidot stāvokli
    if state is None:
        return None

    # Statistika
    total_nodes = 0
    move_count = 0
    total_time = 0

    # Kamēr spēle nav beigusies
    while not is_game_over(state):
        start_time = time.time()

        move, value, nodes = choose_algorithm_move(state, depth, algorithm_name)

        end_time = time.time()

        # Ja algoritms nevar izvēlēties gājienu
        if move is None:
            break

        # Izpildām gājienu
        state = apply_move(state, move)

        # Pieskaitām statistiku
        total_nodes = total_nodes + nodes
        move_count = move_count + 1
        total_time = total_time + (end_time - start_time)

    # Nosakām uzvarētāju
    result = winner_text(state)

    # Ja bija vismaz viens gājiens
    if move_count > 0:
        avg_time = total_time / move_count
    else:
        avg_time = 0

    return {
        "starter": starter,
        "stones": stones,
        "depth": depth,
        "winner": result,
        "nodes": total_nodes,
        "avg_time": avg_time
    }


# Funkcija, kas palaiž vairākus testus vienam algoritmam
def run_algorithm_tests(algorithm_name):
    results = []

    # Dažādi sākuma akmeņu skaiti
    stones_list = [50, 52, 55, 58, 60, 50, 52, 55, 58, 60,]

    # Dažādi dziļumi
    depth_list = [2, 3, 4, 5, 6, 2, 4, 3, 5, 6]

    # Kurš sāk
    starter_list = [
        "human", "human", "human", "human", "human",
        "computer", "computer", "computer", "computer", "computer"
    ]

    # Veicam 10 testus
    for i in range(10):
        stones = stones_list[i]
        depth = depth_list[i]
        starter = starter_list[i]

        result = run_one_test(stones, starter, depth, algorithm_name)

        if result is not None:
            results.append(result)

    return results


# Funkcija, kas sagatavo teksta atskaiti
def format_test_results(results, algorithm_name):
    text = ""
    text += f"{algorithm_name} testi\n"
    text += "=" * 70 + "\n\n"

    computer_wins = 0
    human_wins = 0
    draws = 0

    total_nodes = 0
    total_avg_time = 0

    for i, r in enumerate(results, start=1):
        text += f"{i}. tests\n"
        text += f"  Kurš sāk: {r['starter']}\n"
        text += f"  Akmeņu skaits: {r['stones']}\n"
        text += f"  Dziļums: {r['depth']}\n"
        text += f"  Uzvarētājs: {r['winner']}\n"
        text += f"  Virsotnes: {r['nodes']}\n"
        text += f"  Vidējais laiks: {r['avg_time']:.6f} s\n"
        text += "\n"

        total_nodes = total_nodes + r["nodes"]
        total_avg_time = total_avg_time + r["avg_time"]

        if r["winner"] == "Uzvar dators":
            computer_wins = computer_wins + 1
        elif r["winner"] == "Uzvar cilvēks":
            human_wins = human_wins + 1
        else:
            draws = draws + 1

    if len(results) > 0:
        avg_nodes = total_nodes / len(results)
        avg_time = total_avg_time / len(results)
    else:
        avg_nodes = 0
        avg_time = 0

    text += "=" * 70 + "\n"
    text += "Kopsavilkums\n"
    text += f"Datora uzvaras: {computer_wins}\n"
    text += f"Cilvēka uzvaras: {human_wins}\n"
    text += f"Neizšķirti: {draws}\n"
    text += f"Vidējais virsotņu skaits: {avg_nodes:.2f}\n"
    text += f"Vidējais laiks uz testu: {avg_time:.6f} s\n"

    return text