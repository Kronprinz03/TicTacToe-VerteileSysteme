from tkinter import *
from tkinter import messagebox

class PlayboardGUI():
    def __init__(self, network_interface, gameLogic):
        self.network_interface = network_interface
        self.gameLogic = gameLogic
        self.network_interface.get_needed_functions(self.changeDynamicText, 
                                                          self.activateAllPossibleButtons, 
                                                          self.changeButton) 

    def draw(self, master, goBackCallback, userInfoText,):
        self.goBackCallback = goBackCallback

        self.back_button_frame = Frame(master)
        self.back_button_frame.pack( fill='x', pady=5)

        self.back_button = Button(self.back_button_frame, text="⬅ Back", command=self.on_back)
        self.back_button.pack(side="left", padx=10)

        self.playBoard_frame = Frame(master)
        self.playBoard_frame.pack(expand=True, fill=BOTH)

        title_label = Label(self.playBoard_frame, text="Tic Tac Toe", font=('Arial', 36))
        title_label.pack(pady=10, anchor=N)

        self.button_frame = Frame(self.playBoard_frame)
        self.button_frame.pack(expand=True)

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                button = Button(self.button_frame, text='', font=('Arial', 24), width=5, height=2,
                command=lambda row=i, col=j: self.on_button_click(row, col),state='disabled')
                button.grid(row=i, column=j, padx=2, pady=2) 
                self.buttons[i][j] = button
        for i in range(3):
            self.button_frame.grid_rowconfigure(i, weight=1)
            self.button_frame.grid_columnconfigure(i, weight=1)

        self.status_label = Label(
        self.playBoard_frame, text=userInfoText, font=('Arial', 24))
        self.status_label.pack(pady=10, anchor=N)
        self.isGameRunning = True
 
    def waitForEnemy(self):
        self.network_interface.createGame()
    
    def activateAllPossibleButtons(self):
        if(self.isGameRunning == True):
            for row in self.buttons: 
                for button in row: 
                    if button.cget("text") == "":
                        button.config(state='active')
            self.changeDynamicText("Your Turn")
        

    def changeDynamicText(self, text):
        self.status_label.config(text=text)

    def changeButton(self, row, col):
        clickedButton = self.buttons[row][col]
        clickedButton.config(text="O")
        self.handleGameLogic()
        self.activateAllPossibleButtons()
        

    def on_back(self):
        print("return")
        self.network_interface.stop_broadcast_socket()
        self.playBoard_frame.pack_forget()
        self.back_button_frame.pack_forget()
        self.goBackCallback()
        
    def on_button_click(self, row, col):
        for button_row in self.buttons:
            for button in button_row:
                button.config(state='disabled')
        clickedButton = self.buttons[row][col]
        clickedButton.config(text='X')
        self.network_interface.playmove(row,col)
        self.changeDynamicText("Enemys Turn")
        self.handleGameLogic()
        

    def change_winnning_buttons(self, cords, color):
        for cord in cords:
            button = self.buttons[cord[0]][cord[1]]
            button.config(bg='lightblue', fg='white')
            
    def handleGameLogic(self):
        winning_buttons_cords, isfinished, winner = self.gameLogic.check(self.buttons)
        if(isfinished == False):
           return
        if(winner == 'X'):
            self.change_winnning_buttons(winning_buttons_cords, 'green')
            self.changeDynamicText("You won")
        elif(winner == 'O'):
            self.change_winnning_buttons(winning_buttons_cords, 'red') 
            self.changeDynamicText("You lost")       
        else:
            self.changeDynamicText("Draw")
        self.isGameRunning = False
        self.network_interface.close_tcp_socket()