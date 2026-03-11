# Funkcija izveido sākuma spēles stāvokli
def create_state(stones, starting_player):

    # Pārbaudām vai akmeņu skaits ir diapazonā 50–70
    if stones < 50 or stones > 70:
        print("Kļūda: akmeņu skaitam jābūt no 50 līdz 70")
        return None

    # Izveidojam spēles stāvokļa vārdnīcu
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

    # Kurš sāk spēli
    state["turn"] = starting_player

    # Atgriežam izveidoto stāvokli
    return state