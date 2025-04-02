from tkinter import Tk, Button, Label, Frame, LEFT, BOTH, N

class LocalConnectionGUI:
    def __init__(self, playBoard, joinGame):
        self.playBoard = playBoard
        self.joinGame = joinGame

    def draw(self, master, goBackCallback):
        self.goBackCallback = goBackCallback
        self.master = master
        button_width = 10 

        self.connection_frame = Frame(self.master)
        self.connection_frame.pack(expand=True, fill=BOTH)

        title_label = Label(self.connection_frame, text="Choose Game", font=('Arial', 36))
        title_label.pack(pady=10, anchor=N)

        self.button_frame = Frame(self.connection_frame)
        self.button_frame.pack(anchor='center') 

        self.join_button = Button(self.button_frame, text="Join", font=('Arial', 24), width=button_width, command=self.join_game)
        self.join_button.pack(side='left', padx=10, pady=10)

        self.create_button = Button(self.button_frame, text="Create", font=('Arial', 24), width=button_width, command=self.create_game)
        self.create_button.pack(side='left', padx=10, pady=10) 

        self.back_button = Button(self.button_frame, text="Back", font=('Arial', 24), width=button_width, command=self.go_back)
        self.back_button.pack(side='left', padx=10, pady=10)
    
    def join_game(self):
        print("Join game selected")
        self.connection_frame.pack_forget()
        self.joinGame.draw(self.master, self.backFunction)

    def create_game(self):
        print("Create game selected")
        self.connection_frame.pack_forget()
        self.playBoard.draw(self.master, self.backFunction, "Suche Gegner")
        self.playBoard.waitForEnemy()

    def backFunction(self):
        self.draw(self.master, self.goBackCallback)

    def go_back(self):
        print("Returning to mode selection")
        self.connection_frame.pack_forget()
        self.goBackCallback()

        