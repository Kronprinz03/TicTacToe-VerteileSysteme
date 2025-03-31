import threading
import socket

class LocalNetworkInterface:
    def __init__(self, tcp_controller, broadcastController, get_local_ip):
        self.tcp = tcp_controller
        self.udp = broadcastController
        self.get_local_ip = get_local_ip

    def get_needed_functions(self,dynamic_text_funktion, set_all_possible_buttons_active, change_button_function):
        self.dynamic_text_fuction = dynamic_text_funktion
        self.set_all_possible_buttons_active = set_all_possible_buttons_active
        self.change_button_function = change_button_function

    def createGame(self):
        tcpSocket, local_ip, port = create_tcp_socket(self.get_local_ip)
        self.tcp.set_tcp_socket(tcpSocket)
        self.udp.broadcastingGame(local_ip, port, self.change_user_text)
        self.tcpThread = threading.Thread(target=self.tcp.tcp_socket_listen,
                                          args=(self.stop_broadcast_socket,self.change_user_text,self.set_all_possible_buttons_active))
        self.tcpThread.start()

    def playmove(self, row, col):
        self.tcp.playmove(row,col)
        self.change_user_text("Enemys Turn")
        self.tcpThread = threading.Thread(target=self.tcp.recvmove, args=(self.change_button_function,))
        self.tcpThread.start() 

    def find_active_games(self, sek = 1):
        return self.udp.findActiveGame(sek)
    
    def join_game(self, ip, port):
        self.tcp.socketTcpJoinGame(ip=ip, port=port)
        self.tcpThread = threading.Thread(target=self.tcp.recvmove, args=(self.change_button_function,))
        self.tcpThread.start() 

    def stop_broadcast_socket(self):
        self.udp.stop_broadcast_socket()
    
    def change_user_text(self,text):
        self.dynamic_text_fuction(text)
    
    def close_tcp_socket(self):
        self.tcp.close_tcp_socket()


def create_tcp_socket(get_local_ip):
    local_ip = get_local_ip()
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Create Socket")
    tcpSocket.bind((local_ip,0))    
    port = tcpSocket.getsockname()[1]
    print(f"Bind Socket {local_ip}:{port}")
    return tcpSocket, local_ip, port