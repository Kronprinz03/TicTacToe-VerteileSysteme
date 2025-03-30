class ButtonHandler:
    def check(self, playButtons):
        # Assume playButtons is already a 3x3 2D array
        winning_buttons = []
        winner = None

        for i in range(3):
            # Check rows
            if playButtons[i][0]["text"] == playButtons[i][1]["text"] == playButtons[i][2]["text"] and playButtons[i][0]["text"] != "":
                winning_buttons = [[i,0], [i,1], [i,2]]
                winner = playButtons[i][0]["text"]
                return winning_buttons, True, winner

            # Check columns
            if playButtons[0][i]["text"] == playButtons[1][i]["text"] == playButtons[2][i]["text"] and playButtons[0][i]["text"] != "":
                winning_buttons = [[0,i], [1,i], [2,i]]
                winner = playButtons[0][i]["text"]
                return winning_buttons, True, winner

        # Check diagonals
        if playButtons[0][0]["text"] == playButtons[1][1]["text"] == playButtons[2][2]["text"] and playButtons[0][0]["text"] != "":
            winning_buttons = [[0,0], [1,1], [2,2]]
            winner = playButtons[0][0]["text"]
            return winning_buttons, True, winner

        if playButtons[0][2]["text"] == playButtons[1][1]["text"] == playButtons[2][0]["text"] and playButtons[0][2]["text"] != "":
            winning_buttons = [[0,2], [1,1], [2,0]]
            winner = playButtons[0][2]["text"]
            return winning_buttons, True, winner

        isDraw = checkDraw(playButtons)
        return None, isDraw, None

def checkDraw(playButtons):
    # Check if all buttons are filled
    return all(button["text"] != "" for row in playButtons for button in row)