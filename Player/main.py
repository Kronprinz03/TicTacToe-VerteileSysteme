from GUI.playBoard import PlayboardGUI
from GUI.modeSelectionGUI import ModeSelectionGUI
from GUI.connectionGUI import ConnectionGUI
from GUI.joinGame import JoinGame
from Logic.Local.localNetworkHandler import FindGamesHandler
from Logic.Game.buttonHandler import ButtonHandler
from tkinter import Tk



def main():
    root = Tk()
    root.geometry("1200x710")
    root.title('Tic Tac Toe')
    findGamesHandler = FindGamesHandler()
    buttonHandler = ButtonHandler()
    playBoardGUI = PlayboardGUI(findGamesHandler, buttonHandler)
    joinGameGUI = JoinGame(findGamesHandler, playBoardGUI)

    
    connectionGUI = ConnectionGUI(playBoardGUI, joinGameGUI)
    modeSelectionGUI = ModeSelectionGUI(root, connectionGUI) 
    modeSelectionGUI.draw()
    root.mainloop()

if __name__ == "__main__":
    main()