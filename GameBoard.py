import sys

from Player import Player
from AI import AI
import random


# Game board that can place, twist, and check if a winner is found.
class GameBoard:
    def __init__(self):
        self.output_file = open('Output.txt', 'w')
        self.boards = []
        name = input('Please enter your name: ')
        if name == '':
            print('Name cannot be empty.')
            name = input('Please enter your name: ')
        self.output_file.write("Your name: " + name + '\n')
        token = input('Please pick your token (b/w): ').lower()
        while token != 'b' and token != 'w':
            print('Invalid token.')
            token = input('Please pick your token (b/w): ').lower()
        self.output_file.write("Your token: " + token + '\n')
        self.human = Player(name, token)
        if self.human.token == 'b':
            self.ai = AI('w')
        else:
            self.ai = AI('b')
        self.output("AI's token: " + self.ai.token)

        for i in range(4):
            block = []
            for j in range(9):
                block.append('.')
            self.boards.append(block)

    def start(self):
        if random.choice([1, 2]) == 1:
            self.output('You make the first move.')
            self.human_turn()
        else:
            self.output('AI makes the first move.')
            self.ai.max = True
            self.ai_turn()

    def human_turn(self):
        move = input("Enter your move: ")
        self.output_file.write("Your move: " + move + '\n')
        self.place(self.human.token, int(move[0:1]), int(move[2:3]))
        self.twist(int(move[4:5]), move[5:6].lower())
        self.ai_turn()

    def ai_turn(self):
        print("AI's turn...")
        move = self.ai.play(self.boards)
        self.output(
            "AI's move: {}/{} {}{}".format(move.place_board, move.position, move.twist_board, move.direction.upper()))
        self.place(self.ai.token, move.place_board, move.position)
        self.twist(move.twist_board, move.direction)
        self.human_turn()

    def output(self, message: str):
        print(message)
        self.output_file.write(message + '\n')
        self.output_file.flush()

    def display(self):
        self.output("+-------+-------+")
        for i in range(3):
            self.output('| {} {} {} | {} {} {} |'.format(self.boards[0][0 + 3 * i],
                                                         self.boards[0][1 + 3 * i],
                                                         self.boards[0][2 + 3 * i],
                                                         self.boards[1][0 + 3 * i],
                                                         self.boards[1][1 + 3 * i],
                                                         self.boards[1][2 + 3 * i]))
        self.output("+-------+-------+")
        for i in range(3):
            self.output('| {} {} {} | {} {} {} |'.format(self.boards[2][0 + 3 * i],
                                                         self.boards[2][1 + 3 * i],
                                                         self.boards[2][2 + 3 * i],
                                                         self.boards[3][0 + 3 * i],
                                                         self.boards[3][1 + 3 * i],
                                                         self.boards[3][2 + 3 * i]))
        self.output("+-------+-------+")

    # Board: 1-4
    # Position: 1-9
    def place(self, the_piece: str, the_board: int, the_position: int):
        if the_board < 1 or the_board > 4 or the_position < 1 or the_position > 9 or \
                self.boards[the_board - 1][the_position - 1] != '.':
            self.output('Invalid move')
            self.human_turn()
        else:
            self.boards[the_board - 1][the_position - 1] = the_piece
            self.output('Place')
            self.display()
            self.victory_check()

    def twist(self, the_board: int, the_direction: str):
        if the_board < 1 or the_board > 4 or the_direction.lower() != 'l' and the_direction.lower() != 'r':
            self.output('Invalid twist')
            self.human_turn()
        else:
            board = self.boards[the_board - 1]
            new_board = ['.'] * 9
            new_board[4] = board[4]
            if the_direction.lower() == 'l':
                new_board[0] = board[1]
                new_board[1] = board[2]
                new_board[2] = board[5]
                new_board[5] = board[8]
                new_board[8] = board[7]
                new_board[7] = board[6]
                new_board[6] = board[3]
                new_board[3] = board[0]
            else:
                new_board[0] = board[3]
                new_board[1] = board[0]
                new_board[2] = board[1]
                new_board[5] = board[2]
                new_board[8] = board[5]
                new_board[7] = board[8]
                new_board[6] = board[7]
                new_board[3] = board[6]
            self.boards[the_board - 1] = new_board
            self.output('Twist')
            self.display()
            self.victory_check()

    def victory_check(self):
        # Check rows
        for i in range(0, 3, 2):
            for j in range(3):
                if self.boards[i][1 + 3 * j] != '.':
                    if self.boards[i][0 + 3 * j] == self.boards[i][1 + 3 * j] == self.boards[i][2 + 3 * j] == \
                            self.boards[i + 1][0 + 3 * j] == self.boards[i + 1][1 + 3 * j] \
                            or self.boards[i][1 + 3 * j] == self.boards[i][2 + 3 * j] == self.boards[i + 1][
                            0 + 3 * j] == self.boards[i + 1][1 + 3 * j] == self.boards[i + 1][2 + 3 * j]:
                        if self.boards[i][1 + 3 * j] == self.human.token:
                            self.human.victory = True
                        else:
                            self.ai.victory = True

        # Check columns
        for i in range(2):
            for j in range(3):
                if self.boards[i][j + 3] != '.':
                    if self.boards[i][j] == self.boards[i][j + 3] == self.boards[i][j + 6] == \
                            self.boards[i + 2][j] == self.boards[i + 2][j + 3] \
                            or self.boards[i][j + 3] == self.boards[i][j + 6] == self.boards[i + 2][j] == \
                            self.boards[i + 2][j + 3] == self.boards[i + 2][j + 6]:
                        if self.boards[i][j + 3] == self.human.token:
                            self.human.victory = True
                        else:
                            self.ai.victory = True

        # Check diagonals
        if self.boards[0][8] != '.':
            if self.boards[0][0] == self.boards[0][4] == self.boards[0][8] == self.boards[3][0] == self.boards[3][4] or \
                    self.boards[0][4] == self.boards[0][8] == self.boards[3][0] == self.boards[3][4] == self.boards[3][
                8] or self.boards[1][1] == self.boards[1][3] == self.boards[0][8] == self.boards[2][1] == \
                    self.boards[2][3]:
                if self.boards[0][8] == self.human.token:
                    self.human.victory = True
                else:
                    self.ai.victory = True

        if self.boards[1][6] != '.':
            if self.boards[1][2] == self.boards[1][4] == self.boards[1][6] == self.boards[2][2] == self.boards[2][4] or \
                    self.boards[1][4] == self.boards[1][6] == self.boards[2][2] == self.boards[2][4] == self.boards[2][
                6] or self.boards[0][1] == self.boards[0][5] == self.boards[1][6] == self.boards[3][1] == \
                    self.boards[3][5]:
                if self.boards[1][6] == self.human.token:
                    self.human.victory = True
                else:
                    self.ai.victory = True

        if self.boards[3][0] != '.':
            if self.boards[1][5] == self.boards[1][7] == self.boards[3][0] == self.boards[2][5] == self.boards[2][7]:
                if self.boards[3][0] == self.human.token:
                    self.human.victory = True
                else:
                    self.ai.victory = True

        if self.boards[2][2] != '.':
            if self.boards[0][3] == self.boards[0][7] == self.boards[2][2] == self.boards[3][4] == self.boards[3][7]:
                if self.boards[2][2] == self.human.token:
                    self.human.victory = True
                else:
                    self.ai.victory = True

        if self.human.victory and self.ai.victory:
            self.output('We have a tie!')
            self.output_file.close()
            sys.exit()
        elif self.human.victory:
            self.output('You won!')
            self.output_file.close()
            sys.exit()
        elif self.ai.victory:
            self.output('You lost.')
            self.output_file.close()
            sys.exit()
