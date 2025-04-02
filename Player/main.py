from GUI.playBoard import PlayboardGUI
from GUI.modeSelectionGUI import ModeSelectionGUI

from GUI.LocalElements.localConnectionGUI import LocalConnectionGUI
from GUI.OnlineElements.onlineConnectionGUI import OnlineConnectionGUI

from GUI.LocalElements.localJoinGame import LocalJoinGame
from GUI.OnlineElements.onlineJoinGame import OnlineJoinGame

from Logic.Local.localNetworkInterface import LocalNetworkInterface
from Logic.Online.internetController import InternetNetworkInterface

from Logic.Game.buttonHandler import ButtonHandler
from Logic.Online.serverInterface import ServerInterface
from Logic.utility import get_local_ip

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
    server_interface = ServerInterface()    

    local_network_interface = LocalNetworkInterface(tcp_controller, broadcast_controller, get_local_ip)
    internetController = InternetNetworkInterface(tcp_controller, broadcast_controller, server_interface, get_local_ip)
    
    

    local_playBoardGUI = PlayboardGUI(local_network_interface, buttonHandler)
    localJoinGameGUI = LocalJoinGame(local_network_interface, local_playBoardGUI)
    localConnectionGUI = LocalConnectionGUI(local_playBoardGUI, localJoinGameGUI)

    online_playBoardGUI = PlayboardGUI(internetController,buttonHandler)
    onlineJoinGame = OnlineJoinGame(internetController, online_playBoardGUI, server_interface)
    onlineConnectionGUI = OnlineConnectionGUI(playBoard=online_playBoardGUI, joinGame=onlineJoinGame)
    
    modeSelectionGUI = ModeSelectionGUI(root, localConnectionGUI, onlineConnectionGUI) 
    modeSelectionGUI.draw()
    root.mainloop()

if __name__ == "__main__":
    main()