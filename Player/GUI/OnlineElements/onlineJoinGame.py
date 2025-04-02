import tkinter as tk
import requests

class OnlineJoinGame:
    def __init__(self, internet_controller, playboard, server_interface):
        self.internet_controller = internet_controller
        self.playboard = playboard
        self.server_interface = server_interface

    def draw(self, master, goBackCallback):
        self.master = master
        self.goBackCallback = goBackCallback

        # Top Button Frame
        self.top_frame = tk.Frame(master)
        self.top_frame.pack(fill="x", pady=5)

        # Back Button
        self.back_button = tk.Button(self.top_frame, text="⬅ Back", command=self.on_back)
        self.back_button.pack(side="left", padx=10)

        # Game ID Input Frame
        self.game_id_frame = tk.Frame(master)
        self.game_id_frame.pack(fill="x", pady=5)

        # Game ID Label
        self.game_id_label = tk.Label(self.game_id_frame, text="Game ID:")
        self.game_id_label.pack(side="left", padx=5)

        # Game ID Entry
        self.game_id_entry = tk.Entry(self.game_id_frame)
        self.game_id_entry.pack(side="left", padx=5)

        # Join Game Button
        self.join_button = tk.Button(self.game_id_frame, text="Join Game", command=self.load_game)
        self.join_button.pack(side="left", padx=5)

        # Error Message Label
        self.error_label = tk.Label(master, text="", fg="red")
        self.error_label.pack(pady=5)

    def on_back(self):
        self.top_frame.pack_forget()
        self.game_id_frame.pack_forget()
        self.error_label.pack_forget()
        self.goBackCallback()

    def backFunction(self):
        self.draw(self.master, self.goBackCallback)

    def load_game(self):
        game_code = self.game_id_entry.get()

        if not game_code:
            self.error_label.config(text="Please enter a Game ID.")
            return
        
        if(self.internet_controller.join_game(game_code)):
           self.error_label.config(text="An Error occured while connecting to the game. Pls Check if the game is active and the code is correct.")
           return

        self.top_frame.pack_forget()
        self.game_id_frame.pack_forget()
        self.error_label.pack_forget()
        self.playboard.draw(self.master,self.backFunction, "Enemys Turn") 