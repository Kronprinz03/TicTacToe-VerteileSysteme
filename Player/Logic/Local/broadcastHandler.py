import time 
import socket 
import threading

class BroadcastController:
    def __init__(self):
        self.udpPortSend = 1234
        self.updPortRecv = 4321
    
    def broadcastingGame(self, local_ip, port, change_user_text):
        self.isPlayerSearching = True

        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        self.broadcast_message = f'{local_ip}:{port}'
        print(f'Starting to broadcast: {self.broadcast_message}')
        self.thread = threading.Thread(target=self.broadcastingMessage)
        self.thread.start()
        change_user_text("Suche Gegner")
    
    def findActiveGame(self, listen_duration):
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
            self.broadcast_socket.close()
        except Exception as e:
            print(f"Error in broadcasting: {e}")
        finally:
            self.broadcast_socket.close()
        print(f"Closed Socket")
    
    def stop_broadcast_socket(self):
        self.isPlayerSearching = False

