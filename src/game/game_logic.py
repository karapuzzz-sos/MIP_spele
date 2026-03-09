# Šeit ir spēles noteikumi 

def possible_moves(state):
    # Izveidojam sarakstu ar iespējamiem gājieniem
    moves = []

    # Ja uz galda ir vismaz 2 akmeņi, var paņemt 2
    if state["stones_left"] >= 2:
        moves.append(2)

    # Ja uz galda ir vismaz 3 akmeņi, var paņemt 3
    if state["stones_left"] >= 3:
        moves.append(3)

    # Atgriežam gājienus
    return moves


def is_game_over(state):
    # Spēle beidzas, ja uz galda ir 0 vai 1 akmens
    # (jo 1 akmeni nevar paņemt, ja atļauts tikai 2 vai 3)
    if state["stones_left"] <= 1:
        return True
    return False


def apply_move(state, take):
    # Pārbaudām, vai gājiens ir 2 vai 3
    if take != 2 and take != 3:
        print("Kļūda: drīkst paņemt tikai 2 vai 3 akmeņus")
        return state

    # Pārbaudām, vai uz galda pietiek akmeņu
    if take > state["stones_left"]:
        print("Kļūda: uz galda nav tik daudz akmeņu")
        return state

    # Izveidojam jaunu stāvokli (lai nebojātu veco)
    new_state = {}

    # Nokopējam visus laukus
    new_state["stones_left"] = state["stones_left"]
    new_state["human_taken"] = state["human_taken"]
    new_state["computer_taken"] = state["computer_taken"]
    new_state["human_points"] = state["human_points"]
    new_state["computer_points"] = state["computer_points"]
    new_state["turn"] = state["turn"]

    # Noņemam akmeņus no galda
    new_state["stones_left"] = new_state["stones_left"] - take

    # Kurš paņēma akmeņus
    if new_state["turn"] == "human":
        new_state["human_taken"] = new_state["human_taken"] + take
    else:
        new_state["computer_taken"] = new_state["computer_taken"] + take

    # Punktu piešķiršana pēc atlikušā akmeņu skaita paritātes
    if new_state["stones_left"] % 2 == 0:
        # Ja pāra skaits, tad +2 punktus saņem pretinieks
        if new_state["turn"] == "human":
            new_state["computer_points"] = new_state["computer_points"] + 2
        else:
            new_state["human_points"] = new_state["human_points"] + 2
    else:
        # Ja nepāra skaits, tad +2 punktus saņem pats spēlētājs
        if new_state["turn"] == "human":
            new_state["human_points"] = new_state["human_points"] + 2
        else:
            new_state["computer_points"] = new_state["computer_points"] + 2

    # Pārslēdzam gājienu
    if new_state["turn"] == "human":
        new_state["turn"] = "computer"
    else:
        new_state["turn"] = "human"

    # Atgriežam jauno stāvokli
    return new_state


def final_scores(state):
    # Gala punkti = punkti + paņemtie akmeņi
    human_score = state["human_points"] + state["human_taken"]
    computer_score = state["computer_points"] + state["computer_taken"]
    return human_score, computer_score


def winner_text(state):
    # Aprēķinām gala punktus
    h, c = final_scores(state)

    # Nosakām rezultātu
    if h > c:
        return "Uzvar cilvēks"
    if c > h:
        return "Uzvar dators"
    return "Neizšķirts"