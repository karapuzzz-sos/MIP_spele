# Šeit ir spēles noteikumi
def possible_moves(state):
    # Izveidojam sarakstu ar iespējamiem gājieniem
    moves = []
    # Ja var paņemt 2 akmeņus
    if state["stones_left"] >= 2:
        moves.append(2)
    # Ja var paņemt 3 akmeņus
    if state["stones_left"] >= 3:
        moves.append(3)
    # Atgriežam iespējamos gājienus
    return moves

def is_game_over(state):
    # Spēle beidzas, ja uz galda vairs nav pietiekami akmeņu gājienam
    if state["stones_left"] <= 1:
        return True
    return False

def apply_move(state, take):
    # Pārbaudām, vai drīkst paņemt tikai 2 vai 3
    if take != 2 and take != 3:
        print("Kļūda: drīkst paņemt tikai 2 vai 3 akmeņus")
        return state
    # Pārbaudām, vai uz galda ir pietiekami daudz akmeņu
    if take > state["stones_left"]:
        print("Kļūda: uz galda nav tik daudz akmeņu")
        return state
    # Izveidojam jaunu stāvokli
    new_state = {}
    # Nokopējam visus iepriekšējos datus
    new_state["stones_left"] = state["stones_left"]
    new_state["human_taken"] = state["human_taken"]
    new_state["computer_taken"] = state["computer_taken"]
    new_state["human_points"] = state["human_points"]
    new_state["computer_points"] = state["computer_points"]
    new_state["turn"] = state["turn"]
    # Saglabājam, kurš spēlētājs tagad veic gājienu
    current_player = state["turn"]
    # Nosakām pretinieku
    if current_player == "human":
        other_player = "computer"
    else:
        other_player = "human"
    # Noņemam paņemtos akmeņus no galda
    new_state["stones_left"] = new_state["stones_left"] - take
    # Pieskaitām paņemtos akmeņus attiecīgajam spēlētājam
    if current_player == "human":
        new_state["human_taken"] = new_state["human_taken"] + take
    else:
        new_state["computer_taken"] = new_state["computer_taken"] + take
    # Ja pēc gājiena uz galda paliek pāra skaits akmeņu
    if new_state["stones_left"] % 2 == 0:
        # Tad 2 punktus saņem pretinieks
        if other_player == "human":
            new_state["human_points"] = new_state["human_points"] + 2
        else:
            new_state["computer_points"] = new_state["computer_points"] + 2
    # Ja pēc gājiena uz galda paliek nepāra skaits akmeņu
    else:
        # Tad 2 punktus saņem pats spēlētājs
        if current_player == "human":
            new_state["human_points"] = new_state["human_points"] + 2
        else:
            new_state["computer_points"] = new_state["computer_points"] + 2
    # Pārslēdzam gājienu uz pretinieku
    new_state["turn"] = other_player
    # Atgriežam jauno stāvokli
    return new_state

def final_scores(state):
    # Gala rezultāts ir punkti + paņemtie akmeņi
    human_score = state["human_points"] + state["human_taken"]
    computer_score = state["computer_points"] + state["computer_taken"]
    # Atgriežam abus rezultātus
    return human_score, computer_score

def winner_text(state):
    # Aprēķinām gala punktus
    h, c = final_scores(state)
    # Nosakām uzvarētāju
    if h > c:
        return "Uzvar cilvēks"
    if c > h:
        return "Uzvar dators"
    return "Neizšķirts"