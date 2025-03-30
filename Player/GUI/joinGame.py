
import threading
import tkinter as tk
from tkinter import messagebox

class JoinGame:
    def __init__(self, localNetworkHandler, playboard):
        self.localNetworkHandler = localNetworkHandler
        self.playboard = playboard

    def refresh_game_thread(self): 
        thread = threading.Thread(target=self.refresh_games)
        thread.start()
        self.refresh_button.config(state='disabled')

    def refresh_games(self):
        self.active_games = self.localNetworkHandler.findActiveGame(2)
        self.draw_game_buttons()

    def draw(self, master, goBackCallback):
        self.master = master
        self.goBackCallback = goBackCallback  # Function to call when "Back" is clicked

        # Top Button Frame
        self.top_frame = tk.Frame(master)
        self.top_frame.pack(fill="x", pady=5)

        # Back Button
        self.back_button = tk.Button(self.top_frame, text="⬅ Back", command=self.on_back)
        self.back_button.pack(side="left", padx=10)

        # Refresh Button
        self.refresh_button = tk.Button(self.top_frame, text="🔄 Refresh", command=self.refresh_game_thread)
        self.refresh_button.pack(side="left", padx=10)

        # Frame to hold game buttons
        self.game_list_frame = tk.Frame(master)
        self.game_list_frame.pack(fill="both", expand=True)

        self.active_games = []  # Stores discovered games
        self.refresh_game_thread()

    def on_back(self):
        self.game_list_frame.pack_forget()
        self.top_frame.pack_forget()
        self.goBackCallback()

    def backFunction(self):
        self.draw(self.master, self.goBackCallback)

    def join_game(self, ip, port):
        self.localNetworkHandler.socketTcpJoinGame(ip,port)
        self.top_frame.pack_forget()
        self.game_list_frame.pack_forget()
        self.playboard.draw(self.master,self.backFunction, "Enemys Turn")

    def draw_game_buttons(self):
        for widget in self.game_list_frame.winfo_children():
            widget.destroy()

        self.refresh_button.config(state='active')
        if not self.active_games:
            tk.Label(self.game_list_frame, text="No active games found.", fg="red").pack(pady=20)
            return

        for game_ip, game_port in self.active_games:
            btn = tk.Button(
                self.game_list_frame,
                text=f"Join {game_ip}:{game_port}",
                command=lambda ip=game_ip, port=game_port: self.join_game(ip, port),
                width=30,
                height=2,
                bg="#4CAF50",
                fg="white"
            )
            btn.pack(pady=5)
        