import copy
import math


# This class is used to store a move.
class Move:
    def __init__(self, the_place_board: int, the_position: int, the_twist_board: int, the_direction: str):
        self.place_board = the_place_board
        self.position = the_position
        self.twist_board = the_twist_board
        self.direction = the_direction


# This class is used to build the AI's game tree.
class Node:
    def __init__(self, the_boards: list, depth: int, token, move: Move, is_max, alpha, beta):
        self.children = []
        self.boards = copy.deepcopy(the_boards)
        self.depth = depth
        self.token = token
        self.move = move
        self.is_max = is_max
        self.best_node = None
        self.utility_value = math.inf
        if self.is_max:
            self.utility_value = -math.inf
        self.alpha = alpha
        self.beta = beta


# This class simulates a twist. It is used to generate the possible moves.
def simulate_twist(the_current_boards, the_board: int, the_direction: str):
    board = the_current_boards[the_board]
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
    the_current_boards[the_board] = new_board


# This class can generate the game tree and assign utility values to the game states using the Minimax algorithm.
class AI:
    def __init__(self, the_token: str):
        self.name = 'AI'
        self.token = the_token
        self.victory = False
        self.is_max = False
        self.root = None
        self.max_depth = 3
        self.nodes_total = 0

    # Generates the game tree. It is call recursively until max depth is reached.
    def generate_tree(self, current_node: Node):
        if current_node.depth < self.max_depth:
            new_token = 'b'
            if current_node.token == new_token:
                new_token = 'w'
            seen_moves = []
            possible_moves = []
            for i in range(4):
                for j in range(9):
                    if current_node.boards[i][j] == '.':
                        possible_moves.append([i, j])
            exit_signal = False
            for move in possible_moves:
                boards = copy.deepcopy(current_node.boards)
                boards[move[0]][move[1]] = current_node.token
                for board in range(4):
                    for direction in ['l', 'r']:
                        simulate_twist(boards, board, direction)
                        if boards not in seen_moves:
                            seen_moves.append(copy.deepcopy(boards))
                            node = Node(boards, current_node.depth + 1, new_token,
                                        Move(move[0] + 1, move[1] + 1, board + 1, direction),
                                        not current_node.is_max, current_node.alpha, current_node.beta)
                            current_node.children.append(node)
                            self.generate_tree(node)
                            if current_node.is_max:
                                if current_node.alpha < node.utility_value:
                                    current_node.alpha = node.utility_value
                                if current_node.utility_value < node.utility_value:
                                    current_node.utility_value = node.utility_value
                                    current_node.best_node = node

                            else:
                                if current_node.beta > node.utility_value:
                                    current_node.beta = node.utility_value
                                if current_node.utility_value > node.utility_value:
                                    current_node.utility_value = node.utility_value
                                    current_node.best_node = node
                            if current_node.alpha > current_node.beta or current_node.alpha == current_node.beta:
                                exit_signal = True
                                break
                    if exit_signal:
                        break

                if exit_signal:
                    break

        else:
            current_node.utility_value = self.utility(current_node.boards)

    def play(self, the_current_board: list):
        self.root = Node(the_current_board, 0, self.token, None, self.is_max, -math.inf, math.inf)
        self.generate_tree(self.root)
        return self.root.best_node.move

    def utility(self, the_boards: list):
        value = 0
        modifier = -1
        if self.is_max:
            modifier = 1
        # Calculate columns
        for i in range(2):
            for j in range(3):
                ai_tally = 0
                human_tally = 0
                if the_boards[i][j] == self.token:
                    ai_tally += 1
                elif the_boards[i][j] != '.':
                    human_tally += 1

                if the_boards[i][j + 3] == self.token:
                    ai_tally += 1
                elif the_boards[i][j + 3] != '.':
                    human_tally += 1

                if the_boards[i][j + 6] == self.token:
                    ai_tally += 1
                elif the_boards[i][j + 6] != '.':
                    human_tally += 1

                if the_boards[i + 2][j] == self.token:
                    ai_tally += 1
                elif the_boards[i + 2][j] != '.':
                    human_tally += 1

                if the_boards[i + 2][j + 3] == self.token:
                    ai_tally += 1
                elif the_boards[i + 2][j + 3] != '.':
                    human_tally += 1

                if the_boards[i + 2][j + 6] == self.token:
                    ai_tally += 1
                elif the_boards[i + 2][j + 6] != '.':
                    human_tally += 1

                if ai_tally > 1:
                    value += modifier * ai_tally
                if human_tally > 1:
                    value -= modifier * human_tally

        # Calculate rows
        for i in range(0, 3, 2):
            for j in range(0, 9, 3):
                ai_tally = 0
                human_tally = 0
                if the_boards[i][j] == self.token:
                    ai_tally += 1
                elif the_boards[i][j] != '.':
                    human_tally += 1

                if the_boards[i][j + 1] == self.token:
                    ai_tally += 1
                elif the_boards[i][j + 1] != '.':
                    human_tally += 1

                if the_boards[i][j + 2] == self.token:
                    ai_tally += 1
                elif the_boards[i][j + 2] != '.':
                    human_tally += 1

                if the_boards[i + 1][j] == self.token:
                    ai_tally += 1
                elif the_boards[i + 1][j] != '.':
                    human_tally += 1

                if the_boards[i + 1][j + 1] == self.token:
                    ai_tally += 1
                elif the_boards[i + 1][j + 1] != '.':
                    human_tally += 1

                if the_boards[i + 1][j + 2] == self.token:
                    ai_tally += 1
                elif the_boards[i + 1][j + 2] != '.':
                    human_tally += 1

                if ai_tally > 1:
                    value += modifier * ai_tally
                if human_tally > 1:
                    value -= modifier * human_tally
        return value
