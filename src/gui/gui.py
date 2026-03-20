import time
import tkinter as tk

from game.game_state import create_state
from game.game_logic import apply_move, is_game_over, final_scores, winner_text
from algorithms.minimax import choose_move_minimax
from algorithms.alpha_beta import choose_move_alpha_beta
from algorithms.test.test_runer import run_algorithm_tests, format_test_results

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MI Spēle - Akmeņu spēle")
        self.root.geometry("1100x700")
        self.root.resizable(False, False)

        # Spēles stāvoklis
        self.state = None

        # Mainīgie interfeisam
        self.var_stones = tk.IntVar(value=60)
        self.var_algo = tk.StringVar(value="Minimax")
        self.var_starter = tk.StringVar(value="human")
        self.var_depth = tk.IntVar(value=6)
        self.var_take = tk.IntVar(value=2)

        # Datora informācija
        self.last_ai_info = "Dators vēl nav veicis gājienu"
        self.ai_move_count = 0

        # Virsraksts
        title_label = tk.Label(root, text="Akmeņu spēle", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # Galvenais rāmis
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Kreisā un labā kolonna
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side="left", fill="y", padx=(0, 10))

        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="left", fill="both", expand=True)


        settings_frame = tk.LabelFrame(left_frame, text="Spēles iestatījumi", padx=10, pady=10)
        settings_frame.pack(fill="x", pady=(0, 10))

        tk.Label(settings_frame, text="Sākuma akmeņi (50-70):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Spinbox(settings_frame, from_=50, to=70, textvariable=self.var_stones, width=8).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(settings_frame, text="Kurš sāk:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.OptionMenu(settings_frame, self.var_starter, "human", "computer").grid(row=1, column=1, padx=5, pady=5)

        tk.Label(settings_frame, text="Algoritms:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        tk.OptionMenu(settings_frame, self.var_algo, "Minimax", "AlphaBeta").grid(row=2, column=1, padx=5, pady=5)

        tk.Label(settings_frame, text="Dziļums:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        tk.Spinbox(settings_frame, from_=1, to=12, textvariable=self.var_depth, width=8).grid(row=3, column=1, padx=5, pady=5)

        tk.Button(settings_frame, text="Sākt spēli", width=15, command=self.start_game).grid(row=2, column=0, padx=5, pady=10)
        tk.Button(settings_frame, text="Restart", width=15, command=self.reset_game).grid(row=2, column=1, padx=5, pady=10)
        tk.Button(settings_frame, text="Testi", width=15, command=self.open_test_window).grid(row=2, column=2, padx=5, pady=10)

   
        move_frame = tk.LabelFrame(left_frame, text="Cilvēka gājiens", padx=10, pady=10)
        move_frame.pack(fill="x")

        tk.Label(move_frame, text="Izvēlies, cik akmeņus paņemt:").pack(anchor="w", pady=(0, 8))

        tk.Radiobutton(
            move_frame,
            text="Paņemt 2 akmeņus",
            variable=self.var_take,
            value=2,
            font=("Arial", 10)
        ).pack(anchor="w")

        tk.Radiobutton(
            move_frame,
            text="Paņemt 3 akmeņus",
            variable=self.var_take,
            value=3,
            font=("Arial", 10)
        ).pack(anchor="w")

        self.btn_make_move = tk.Button(
            move_frame,
            text="Izpildīt gājienu",
            width=18,
            command=self.make_human_move
        )
        self.btn_make_move.pack(pady=10)

    
        info_frame = tk.LabelFrame(right_frame, text="Spēles informācija", padx=10, pady=10)
        info_frame.pack(fill="x", pady=(0, 10))

        self.lbl_info = tk.Label(
            info_frame,
            text="Nospied 'Sākt spēli'",
            justify="left",
            anchor="nw",
            font=("Consolas", 11),
            width=55,
            height=12
        )
        self.lbl_info.pack(fill="x", padx=5, pady=5)

   
        ai_frame = tk.LabelFrame(right_frame, text="Datora pēdējā gājiena informācija", padx=10, pady=10)
        ai_frame.pack(fill="x", pady=(0, 10))

        self.lbl_ai_info = tk.Label(
            ai_frame,
            text=self.last_ai_info,
            justify="left",
            anchor="w",
            font=("Arial", 10),
            width=70
        )
        self.lbl_ai_info.pack(fill="x", padx=5, pady=5)

      
        history_frame = tk.LabelFrame(right_frame, text="Datora gājienu vēsture", padx=10, pady=10)
        history_frame.pack(fill="both", expand=True)

        self.history_listbox = tk.Listbox(
            history_frame,
            height=12,
            font=("Arial", 10)
        )
        self.history_listbox.pack(side="left", fill="both", expand=True)

        history_scrollbar = tk.Scrollbar(history_frame, orient="vertical")
        history_scrollbar.pack(side="right", fill="y")

        self.history_listbox.config(yscrollcommand=history_scrollbar.set)
        history_scrollbar.config(command=self.history_listbox.yview)

        # Sākumā poga izslēgta
        self.set_buttons_enabled(False)
    
    def set_buttons_enabled(self, enabled):
        state = "normal" if enabled else "disabled"
        self.btn_make_move.config(state=state)

    def start_game(self):
        stones = int(self.var_stones.get())
        starter = self.var_starter.get()

        self.state = create_state(stones, starter)

        if self.state is None:
            self.lbl_info.config(text="Kļūda: akmeņu skaitam jābūt no 50 līdz 70")
            self.lbl_ai_info.config(text="Spēle netika sākta")
            self.set_buttons_enabled(False)
            return

        self.last_ai_info = "Dators vēl nav veicis gājienu"
        self.lbl_ai_info.config(text=self.last_ai_info)

        self.history_listbox.delete(0, tk.END)
        self.ai_move_count = 0

        self.update_view()

        if self.state["turn"] == "computer":
            self.root.after(300, self.computer_move)

    def reset_game(self):
        self.state = None
        self.last_ai_info = "Dators vēl nav veicis gājienu"
        self.lbl_info.config(text="Nospied 'Sākt spēli'")
        self.lbl_ai_info.config(text=self.last_ai_info)
        self.history_listbox.delete(0, tk.END)
        self.ai_move_count = 0
        self.set_buttons_enabled(False)

    def update_view(self):
        if self.state is None:
            return

        h, c = final_scores(self.state)

        text = ""
        text += f"Uz galda: {self.state['stones_left']} akmeņi\n\n"
        text += f"Cilvēks:\n"
        text += f"  punkti = {self.state['human_points']}\n"
        text += f"  paņemtie akmeņi = {self.state['human_taken']}\n"
        text += f"  gala rezultāts = {h}\n\n"
        text += f"Dators:\n"
        text += f"  punkti = {self.state['computer_points']}\n"
        text += f"  paņemtie akmeņi = {self.state['computer_taken']}\n"
        text += f"  gala rezultāts = {c}\n\n"

        if is_game_over(self.state):
            result = winner_text(self.state)
            text += "Spēle ir beigusies\n"
            text += f"Uzvarētājs: {result}\n"
            text += "\nLai sāktu jaunu spēli, nospied pogu 'Restart'"
            self.set_buttons_enabled(False)
            self.lbl_ai_info.config(text=f"Spēles rezultāts: {result}")
        else:
            text += f"Tagad gājiens: {self.state['turn']}"
            if self.state["turn"] == "human":
                self.set_buttons_enabled(True)
            else:
                self.set_buttons_enabled(False)

        self.lbl_info.config(text=text)

    def make_human_move(self):
        take = self.var_take.get()
        self.human_move(take)

    def human_move(self, take):
        if self.state is None:
            return

        if self.state["turn"] != "human":
            return

        self.state = apply_move(self.state, take)

        self.last_ai_info = f"Cilvēks paņēma: {take}"
        self.lbl_ai_info.config(text=self.last_ai_info)

        self.update_view()

        if self.state is not None and not is_game_over(self.state):
            if self.state["turn"] == "computer":
                self.root.after(300, self.computer_move)
    
    def computer_move(self):
        if self.state is None:
            return

        if self.state["turn"] != "computer":
            return

        depth = int(self.var_depth.get())
        algo = self.var_algo.get()

        start_time = time.time()

        if algo == "Minimax":
            move, value, nodes = choose_move_minimax(self.state, depth)
        else:
            move, value, nodes = choose_move_alpha_beta(self.state, depth)

        end_time = time.time()
        ms = int((end_time - start_time) * 1000)

        if move is None:
            self.last_ai_info = "Dators nevar veikt gājienu"
            self.lbl_ai_info.config(text=self.last_ai_info)
            self.update_view()
            return

        self.state = apply_move(self.state, move)

        self.last_ai_info = (
            f"Dators paņēma: {move} | "
            f"Novērtējums: {value} | "
            f"Virsotnes: {nodes} | "
            f"Laiks: {ms} ms"
        )
        self.lbl_ai_info.config(text=self.last_ai_info)

        self.ai_move_count = self.ai_move_count + 1
        self.history_listbox.insert(
            tk.END,
            f"{self.ai_move_count}. gājiens -> paņēma {move}, vērtība {value}, virsotnes {nodes}, laiks {ms} ms"
        )
        self.history_listbox.see(tk.END)

        self.update_view()
    def open_test_window(self):
        # Izveidojam jaunu logu
        test_window = tk.Toplevel(self.root)
        test_window.title("Algoritmu testu rezultāti")
        test_window.geometry("900x700")

        # Teksta lauks rezultātiem
        text_widget = tk.Text(test_window, wrap="word", font=("Consolas", 10))
        text_widget.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(test_window, command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        text_widget.config(yscrollcommand=scrollbar.set)

        # Parādām, ka testi tiek veikti
        text_widget.insert(tk.END, "Notiek Minimax testu izpilde...\n")
        test_window.update()

        # Minimax testi
        minimax_results = run_algorithm_tests("Minimax")
        minimax_text = format_test_results(minimax_results, "Minimax")

        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, minimax_text)
        text_widget.insert(tk.END, "\n\n")

        text_widget.insert(tk.END, "Notiek Alpha-Beta testu izpilde...\n")
        test_window.update()

        # Alpha-Beta testi
        alphabeta_results = run_algorithm_tests("AlphaBeta")
        alphabeta_text = format_test_results(alphabeta_results, "Alpha-Beta")

        text_widget.insert(tk.END, alphabeta_text)    

def start_gui():
    root = tk.Tk()
    app = App(root)
    root.mainloop()