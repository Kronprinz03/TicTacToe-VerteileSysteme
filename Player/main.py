from GUI.playBoard import PlayboardGUI
from GUI.modeSelectionGUI import ModeSelectionGUI
from GUI.connectionGUI import ConnectionGUI
from GUI.joinGame import JoinGame
from Logic.Game.buttonHandler import ButtonHandler
from Logic.utility import get_local_ip
from Logic.Local.localNetworkInterface import LocalNetworkInterface
from Logic.Local.broadcastHandler import BroadcastController
from Logic.Local.localNetworkHandler import TCPController
from tkinter import Tk



def main():
    root = Tk()
    root.geometry("1200x710")
    root.title('Tic Tac Toe')
    tcp_controller = TCPController()
    broadcast_controller = BroadcastController()
    buttonHandler = ButtonHandler()
    local_network_interface = LocalNetworkInterface(tcp_controller,broadcast_controller, get_local_ip)
    playBoardGUI = PlayboardGUI(local_network_interface, buttonHandler)
    joinGameGUI = JoinGame(local_network_interface, playBoardGUI)

    
    connectionGUI = ConnectionGUI(playBoardGUI, joinGameGUI)
    modeSelectionGUI = ModeSelectionGUI(root, connectionGUI) 
    modeSelectionGUI.draw()
    root.mainloop()

if __name__ == "__main__":
    main()