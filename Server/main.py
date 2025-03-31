from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

games = {}
@app.route('/',methods=['GET'])
def home():
    return jsonify({"hello": "hello"})

@app.route('/createGame', methods=['POST'])
def create_game():
    data = request.json
    player_id = data.get('player_id')
    player_ip = data.get('player_ip')
    player_port = data.get('player_port')
    if not player_id or not player_ip or not player_port:
        return jsonify({"error": "Missing data"}), 400

    game_code = str(uuid.uuid4())
    games[game_code] = (player_id, player_ip, player_port)
    return jsonify({"game_code": game_code}), 200

@app.route('/removeGame', methods=['POST'])
def remove_game():
    data = request.json
    game_code = data.get('game_code')
    if game_code in games:
        del games[game_code]
        return jsonify({"message": f"Game {game_code} removed"}), 200
    else:
        return jsonify({"error": "Game not found"}), 404

@app.route('/joinGame', methods=['POST'])
def join_game():
    data = request.json
    game_code = data.get('game_code')
    if game_code in games:
        player_id, player_ip, player_port = games[game_code]
        return jsonify({"player_ip": player_ip, "player_port": player_port}), 200
    else:
        return jsonify({"error": "Game not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)