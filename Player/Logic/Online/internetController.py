import threading
import socket
from pyngrok import ngrok

class InternetNetworkInterface:
    def __init__(self, tcp_controller, broadcastController, server_interface, get_local_ip):
        self.tcp = tcp_controller
        self.udp = broadcastController
        self.server_interface = server_interface
        self.get_local_ip = get_local_ip
        self.game_id = None 

    def get_needed_functions(self,dynamic_text_funktion, set_all_possible_buttons_active, change_button_function):
        self.dynamic_text_fuction = dynamic_text_funktion
        self.set_all_possible_buttons_active = set_all_possible_buttons_active
        self.change_button_function = change_button_function

    def createGame(self):
        tcpSocket, local_ip, port = create_tcp_socket(self.get_local_ip)
        self.tcp.set_tcp_socket(tcpSocket)
        self.tcp.tcp_socket_listen()
        server_ip, server_port, ngrok_tunnel = create_server(port)
        game_id = self.server_interface.send_new_game("123",server_ip, server_port)

        self.tunnel = ngrok_tunnel
        self.game_id = game_id

        self.tcpThread = threading.Thread(target=self.tcp.tcp_socket_accept,
                                          args=(self.stop_broadcast_socket,self.change_user_text,self.set_all_possible_buttons_active))
        self.tcpThread.start()
        
        print(game_id)
        self.change_user_text(f"Game ID : {game_id}")

    def playmove(self, row, col):
        self.tcp.playmove(row,col)
        self.change_user_text("Enemys Turn")
        self.tcpThread = threading.Thread(target=self.tcp.recvmove, args=(self.change_button_function,))
        self.tcpThread.start() 
    
    def join_game(self, game_id):
        response = self.server_interface.get_game_with_code(game_id)
        print(response)
        ip = response.get('player_ip')
        port = response.get('player_port')
        print(f"IP: {ip}, Port: {port}")
        self.tcp.socketTcpJoinGame(ip=ip, port=port)
        self.tcpThread = threading.Thread(target=self.tcp.recvmove, args=(self.change_button_function,))
        self.tcpThread.start() 

    def stop_broadcast_socket(self):
        pass
    
    def change_user_text(self,text):
        self.dynamic_text_fuction(text)
    
    def close_tcp_socket(self):
        self.tcp.close_tcp_socket()
        if (self.game_id != None):
            self.server_interface.delete_game(self.game_id)
            ngrok.disconnect(self.tunnel.public_url)
            self.game_id = None

def create_server(socket_port):
    server_port = socket_port
    ngrok_tunnel = ngrok.connect(server_port, "tcp")
    server_url = ngrok_tunnel.public_url
    server_ip, server_port = server_url.replace('tcp://', '').split(':')

    print(f"Game ready: Player 1's server is accessible at {server_ip}:{server_port}")
    return server_ip, server_port, ngrok_tunnel


def create_tcp_socket(get_local_ip):
    local_ip = get_local_ip()
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Create Socket")
    tcpSocket.bind(("0.0.0.0",0))    
    port = tcpSocket.getsockname()[1]
    print(f"Bind Socket {local_ip}:{port}")
    return tcpSocket, local_ip, port