from tkinter import Tk, Button, Label, Frame, LEFT, BOTH, N

class ModeSelectionGUI:
    def __init__(self, master, local_connectionGUI, online_connectionGUI):
        self.local_connectionGUI = local_connectionGUI
        self.online_connectionGUI = online_connectionGUI
        self.master = master


    def draw(self): 
        self.mode_frame = Frame(self.master)
        self.mode_frame.pack(expand=True, fill=BOTH)

        title_label = Label(self.mode_frame, text="Choose Mode", font=('Arial', 36))
        title_label.pack(pady=10, anchor=N)

        self.button_frame = Frame(self.mode_frame)
        self.button_frame.pack(anchor='center', pady=20)

        button_width = 10

        online_button = Button(self.button_frame, text="Online", font=('Arial', 24), width=button_width, command=self.select_online)
        online_button.pack(side=LEFT, padx=10, pady=10)

        local_button = Button(self.button_frame, text="Local", font=('Arial', 24), width=button_width, command=self.select_local)
        local_button.pack(side=LEFT, padx=10, pady=10)

    def select_online(self):
        print("Online mode selected")
        self.mode_frame.pack_forget()
        self.online_connectionGUI.draw(self.master, self.draw) 

    def select_local(self):
        print("Local mode selected")
        self.mode_frame.pack_forget()
        self.local_connectionGUI.draw(self.master, self.draw)
    