import requests

class ServerInterface:
    def __init__(self):
        self.route_get_game = "http://87.106.224.118:3000/joinGame"
        self.route_new_game =  "http://87.106.224.118:3000/createGame"
        self.route_delete_game = "http://87.106.224.118:3000/removeGame"

    def send_new_game(self, player_id, player_ip, player_port):
        payload = {
        "player_id": player_id,
        "player_ip": player_ip,
        "player_port": player_port
        }
        response = requests.post(self.route_new_game, json=payload)
        if response.status_code == 200:
            return response.json().get("game_code")
        else:
            return response.json().get("error")

    def get_game_with_code(self, game_code):
        payload = {
            "game_code": game_code
        }
        response = requests.post(self.route_get_game, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return response.json().get("error")

    def delete_game(self, game_code):
        payload = {
            "game_code": game_code
        }
        response = requests.post(self.route_delete_game, json=payload)
        if response.status_code == 200:
            return response.json().get("message")
        else:
            return response.json().get("error")