import socket
import threading
class TCPController:
    
    def set_tcp_socket(self, socket):
        self.tcpSocket = socket

    def tcp_socket_listen(self):
        self.tcpSocket.listen()
        print("Socket listen")

    def tcp_socket_accept(self,stop_broadcast_socket, change_user_text,set_possible_all_buttons_active):                
        self.connect, self.addr = self.tcpSocket.accept()
        print("Accepted incomming connect")
        stop_broadcast_socket()
        print(self.connect)

        change_user_text("Gegner Gefunden")
        set_possible_all_buttons_active()

    def socketTcpJoinGame(self, ip, port):
        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("create Socket")
        self.tcpSocket.connect((ip,int(port)))
        self.connect = self.tcpSocket
        print(f"Connect to {ip}:{int(port)}")
        

    def playmove(self, row, col):
        move_tuple = (row, col)
        move_str = str(move_tuple) 
        move_bytes = move_str.encode('utf-8') 
        self.connect.send(move_bytes)

    def recvmove(self, change_button_function):
        try:
            data = self.connect.recv(4096)
            move_tuple = eval(data.decode('utf-8'))
            if isinstance(move_tuple, tuple) and len(move_tuple) == 2:
                row, col = move_tuple
                change_button_function(row, col)
            else:
                print("Invalid data format.")
        except Exception as e:
            print(f"Error receiving or processing data: {e}")

    def close_tcp_socket(self):
        self.tcpSocket.close()
        self.connect.close()
