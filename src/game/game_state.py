# Funkcija izveido jaunu spēles stāvokli 
def create_state(stones, starting_player):
    # Izveidojam tukšu vārdnīcu
    state = {}

    # Akmeņu skaits uz galda
    state["stones_left"] = stones

    # Cilvēka paņemtie akmeņi
    state["human_taken"] = 0

    # Datora paņemtie akmeņi
    state["computer_taken"] = 0

    # Cilvēka punkti
    state["human_points"] = 0

    # Datora punkti
    state["computer_points"] = 0

    # Kurš ir gājienā: "human" vai "computer"
    state["turn"] = starting_player

    # Atgriežam stāvokli
    return state