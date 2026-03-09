# Heiristika: jo lielāka vērtība, jo labāk datoram

def heuristic(state):
    # Datora pašreizējais rezultāts
    computer_now = state["computer_points"] + state["computer_taken"]

    # Cilvēka pašreizējais rezultāts
    human_now = state["human_points"] + state["human_taken"]

    # Starpība (dators - cilvēks)
    return computer_now - human_now