import time
import tkinter as tk
from tkinter import messagebox

from game.game_state import create_state
from game.game_logic import apply_move, is_game_over, final_scores, winner_text
from algorithms.minimax import choose_move_minimax
from algorithms.alpha_beta import choose_move_alpha_beta


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MI Spēle (akmeņi)")

        # Spēles stāvoklis
        self.state = None

        # UI mainīgie
        self.var_stones = tk.IntVar(value=60)
        self.var_algo = tk.StringVar(value="Minimax")
        self.var_starter = tk.StringVar(value="human")
        self.var_depth = tk.IntVar(value=6)

        # Augšējais bloks ar iestatījumiem
        frm = tk.Frame(root)
        frm.pack(padx=10, pady=10)

        tk.Label(frm, text="Sākuma akmeņi (50-70):").grid(row=0, column=0, sticky="w")
        tk.Spinbox(frm, from_=50, to=70, textvariable=self.var_stones, width=5).grid(row=0, column=1, sticky="w")

        tk.Label(frm, text="Kurš sāk:").grid(row=0, column=2, sticky="w", padx=(10, 0))
        tk.OptionMenu(frm, self.var_starter, "human", "computer").grid(row=0, column=3, sticky="w")

        tk.Label(frm, text="Algoritms:").grid(row=1, column=0, sticky="w")
        tk.OptionMenu(frm, self.var_algo, "Minimax", "AlphaBeta").grid(row=1, column=1, sticky="w")

        tk.Label(frm, text="Dziļums:").grid(row=1, column=2, sticky="w", padx=(10, 0))
        tk.Spinbox(frm, from_=1, to=12, textvariable=self.var_depth, width=5).grid(row=1, column=3, sticky="w")

        tk.Button(frm, text="Sākt spēli", command=self.start_game).grid(row=2, column=0, pady=(8, 0), sticky="we")
        tk.Button(frm, text="Restart", command=self.reset_game).grid(row=2, column=1, pady=(8, 0), sticky="we")

        # Informācijas lauks
        self.lbl_info = tk.Label(root, text="Nospied 'Sākt spēli'", justify="left")
        self.lbl_info.pack(padx=10, pady=10, anchor="w")

        # Pogas cilvēka gājieniem
        frm2 = tk.Frame(root)
        frm2.pack(padx=10, pady=10)

        self.btn_take2 = tk.Button(frm2, text="Paņemt 2", width=12, command=lambda: self.human_move(2))
        self.btn_take3 = tk.Button(frm2, text="Paņemt 3", width=12, command=lambda: self.human_move(3))
        self.btn_take2.grid(row=0, column=0, padx=5)
        self.btn_take3.grid(row=0, column=1, padx=5)

        # Sākumā pogas izslēgtas
        self.set_buttons_enabled(False)

    def set_buttons_enabled(self, enabled):
        if enabled:
            state = "normal"
        else:
            state = "disabled"

        self.btn_take2.config(state=state)
        self.btn_take3.config(state=state)

    def start_game(self):
        stones = int(self.var_stones.get())
        starter = self.var_starter.get()

        # Izveidojam sākuma spēles stāvokli
        self.state = create_state(stones, starter)

        # Ja lietotājs ievadīja nepareizu akmeņu skaitu
        if self.state is None:
            self.lbl_info.config(text="Kļūda: akmeņu skaitam jābūt no 50 līdz 70")
            self.set_buttons_enabled(False)
            messagebox.showerror("Kļūda", "Akmeņu skaitam jābūt no 50 līdz 70")
            return

        # Atjaunojam loga informāciju
        self.update_view()

        # Ja pirmais sāk dators, tad dators izdara pirmo gājienu
        if self.state["turn"] == "computer":
            self.root.after(200, self.computer_move)

    def reset_game(self):
        self.state = None
        self.lbl_info.config(text="Nospied 'Sākt spēli'")
        self.set_buttons_enabled(False)

    def update_view(self):
        if self.state is None:
            return

        h, c = final_scores(self.state)

        text = ""
        text += f"Uz galda: {self.state['stones_left']} akmeņi\n"
        text += f"Cilvēks: punkti={self.state['human_points']} paņemti={self.state['human_taken']} gala={h}\n"
        text += f"Dators: punkti={self.state['computer_points']} paņemti={self.state['computer_taken']} gala={c}\n"
        text += f"Gājiens: {self.state['turn']}\n"

        self.lbl_info.config(text=text)

        # Ja spēle ir beigusies
        if is_game_over(self.state):
            self.set_buttons_enabled(False)
            messagebox.showinfo("Spēle beigusies", winner_text(self.state))
            return

        # Ja gājiens ir cilvēkam
        if self.state["turn"] == "human":
            self.set_buttons_enabled(True)
        else:
            self.set_buttons_enabled(False)

    def human_move(self, take):
        if self.state is None:
            return

        if self.state["turn"] != "human":
            return

        # Cilvēks izdara gājienu
        self.state = apply_move(self.state, take)

        # Atjaunojam skatu
        self.update_view()

        # Ja tagad gājiens ir datoram, lai dators spēlē
        if self.state is not None and not is_game_over(self.state):
            if self.state["turn"] == "computer":
                self.root.after(200, self.computer_move)

    def computer_move(self):
        if self.state is None:
            return

        if self.state["turn"] != "computer":
            return

        depth = int(self.var_depth.get())
        algo = self.var_algo.get()

        start_time = time.time()

        # Izvēlamies algoritmu
        if algo == "Minimax":
            move, value, nodes = choose_move_minimax(self.state, depth)
        else:
            move, value, nodes = choose_move_alpha_beta(self.state, depth)

        end_time = time.time()
        ms = int((end_time - start_time) * 1000)

        # Ja nav iespējama gājiena
        if move is None:
            self.update_view()
            return

        # Dators izdara gājienu
        self.state = apply_move(self.state, move)

        messagebox.showinfo(
            "Datora gājiens",
            f"Dators paņēma: {move}\nNovērtējums: {value}\nVirsotnes: {nodes}\nLaiks: {ms} ms"
        )

        # Atjaunojam skatu
        self.update_view()


def start_gui():
    root = tk.Tk()
    app = App(root)
    root.mainloop()