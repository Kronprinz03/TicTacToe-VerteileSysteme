import socket
import netifaces
import threading
import time 

class FindGamesHandler:
    def __init__(self):
        self.udpPortSend = 1234
        self.updPortRecv = 4321

    def setDynamicTextFuction(self, dynamicTextFunktion):
        self.dynamicTextFuction = dynamicTextFunktion
    
    def setAllButtonsPossibleActive(self, allButtonsPossibleActive):
        self.allButtonsPossibleActive = allButtonsPossibleActive

    def setChangeButtonFunction(self, changeButtonFunction):
        self.changeButtonFunction = changeButtonFunction

    def broadcastingGame(self):  
        self.isGameRunning = True
        self.isPlayerSearching = True

        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Create Socket")
        local_ip = get_local_ip()
        self.tcpSocket.bind((local_ip,0))    
        port = self.tcpSocket.getsockname()[1]
        print(f"Bind Socket {local_ip}:{port}")

        self.tcpThread = threading.Thread(target=self.socketTcpCreateGame)
        self.tcpThread.start() 


        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        self.broadcast_message = f'{local_ip}:{port}'
        print(f'Starting to broadcast: {self.broadcast_message}')
        self.thread = threading.Thread(target=self.broadcastingMessage)
        self.thread.start()
        self.dynamicTextFuction("Suche Gegner")

    def findActiveGame(self, listen_duration=1):
        listener_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listener_socket.bind(("", self.updPortRecv))
        listener_socket.settimeout(1)

        start_time = time.time()
        active_games = []

        print('Searching for active games...')
        try:
            while time.time() - start_time < listen_duration:
                try:
                    data, addr = listener_socket.recvfrom(1024)
                    game_info = data.decode()
                    print(f'Found game: {game_info} from {addr}')
                    if game_info not in active_games:
                        active_games.append(game_info)
                except socket.timeout:
                    continue
        finally:
            listener_socket.close()

        return_active_games = []
        for active_game in active_games:
            return_active_games.append(active_game.split(':', 1))
        
        listener_socket.close()
        return return_active_games

    def broadcastingMessage(self):
        try:    
            while self.isPlayerSearching:
                self.broadcast_socket.sendto(self.broadcast_message.encode(), ('<broadcast>', self.updPortRecv))
                print(f"Broadcasted message: {self.broadcast_message}")
                time.sleep(1)
        except Exception as e:
            print(f"Error in broadcasting: {e}")
        finally:
            self.broadcast_socket.close()
        print(f"Closed Socket")

    def stopBroadCastSocket(self):
        self.isPlayerSearching = False

    def socketTcpCreateGame(self):
        self.tcpSocket.listen()
        self.connect, self.addr = self.tcpSocket.accept()
        print("Accepted incomming connect")
        self.stopBroadCastSocket()
        print(self.connect)

        self.dynamicTextFuction("Gegner Gefunden")
        self.allButtonsPossibleActive()

    def socketTcpJoinGame(self, ip, port):
        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("create Socket")
        self.tcpSocket.connect((ip,int(port)))
        self.connect = self.tcpSocket
        print(f"Connect to {ip}:{int(port)}")
        self.tcpThread = threading.Thread(target=self.recvmove)
        self.tcpThread.start() 

    def playmove(self, row, col):
        print(self.connect)
        move_tuple = (row, col)
        move_str = str(move_tuple) 
        move_bytes = move_str.encode('utf-8') 
        self.connect.send(move_bytes)
        print("send data")
        self.dynamicTextFuction("Enemys Turn")
        self.tcpThread = threading.Thread(target=self.recvmove)
        self.tcpThread.start() 

    def recvmove(self):
        try:
            data = self.connect.recv(4096)
            move_tuple = eval(data.decode('utf-8'))
            if isinstance(move_tuple, tuple) and len(move_tuple) == 2:
                row, col = move_tuple
                self.changeButtonFunction(row, col)
                self.isEnemyTurn = False
            else:
                print("Invalid data format.")
        except Exception as e:
            print(f"Error receiving or processing data: {e}")

    def close_tcp_socket(self):
        self.tcpSocket.close()
        self.connect.close()


def get_local_ip():
    for interface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(interface)
        ipv4_info = addresses.get(netifaces.AF_INET)

        if ipv4_info:
            for link in ipv4_info:
                ip = link.get('addr')
                if ip and not ip.startswith('127.'):
                    return ip
    return 'localhost' 