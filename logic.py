
# Business logic functions
# Can be used across use cases, maybe in other games

import random
import csv
from datetime import datetime

class Board:
    def __init__(self):
        self._rows = [[None, None, None] for _ in range(3)]

    def get(self, x, y):
        return self._rows[y][x]

    def set(self, x, y, value):
        if self._rows[y][x] is None:
            self._rows[y][x] = value
        else:
            raise ValueError("The cell is already occupied.")

    def available_moves(self):
        return [(x, y) for y in range(3) for x in range(3) if self.get(x, y) is None]

    def is_winner(self, player):
        lines = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]
        for line in lines:
            if all(self.get(x, y) == player.marker for x, y in line):
                return True
        return False

    def is_draw(self):
        return all(self.get(x, y) is not None for y in range(3) for x in range(3))

    def display(self):
        symbols = {None: ' ', 'X': 'X', 'O': 'O'}
        for row in self._rows:
            print("|".join(symbols[cell] for cell in row))
            print("-" * 5)
        print("*********************")

class Player:
    def __init__(self, marker):
        self.marker = marker

    def get_move(self, board):
        while True:
            try:
                x, y = map(int, input(f"Player {self.marker}, enter your move (x y): ").split())
                if (x, y) in board.available_moves():
                    return x, y
                else:
                    print("That spot is already taken or invalid.")
            except ValueError:
                print("Please enter the coordinates as x y, with x and y being numbers from 0 to 2.")

class Bot(Player):
    def get_move(self, board):
        return random.choice(board.available_moves())

class Game:
    def __init__(self, player1, player2):
        self.board = Board()
        self.players = [player1, player2]
        self.current_player = 0  # Player 1 starts

    def switch_player(self):
        self.current_player = 1 - self.current_player

    def log_winner(self, winner):
        with open('logs/game_log.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), winner])

    def play(self):
        while True:
            self.board.display()
            player = self.players[self.current_player]
            x, y = player.get_move(self.board)
            self.board.set(x, y, player.marker)
            
            if self.board.is_winner(player):
                self.board.display()
                winner = f"Player {player.marker}"
                print(f"Player {player.marker} wins!")
                self.log_winner(winner)
                break
            elif self.board.is_draw():
                self.board.display()
                print("It's a draw!")
                self.log_winner('Draw')
                break
            
            self.switch_player()


def evaluate_game_state(board):
    if board.is_winner(Player('X')):
        return 'X wins'
    elif board.is_winner(Player('O')):
        return 'O wins'
    elif board.is_draw():
        return 'Draw'
    else:
        return 'Game ongoing'