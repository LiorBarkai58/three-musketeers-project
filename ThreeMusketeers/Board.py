import kivy
from kivy.config import Config
from kivy.core.text import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image

Config.set("graphics", "width", 800)
Config.set("graphics", "height", 800)

types_dictionary = {"musketeer": "M", "guard": "G", "empty": "-"}
pictures_dictionary = {"M": "pics/5head.png", "G": "pics/kekw.png", "-": "pics/kappa.png"}


class GraphicBoard(GridLayout):
    def __init__(self, board, **kwargs):
        GridLayout.__init__(self, **kwargs)
        self.board = board
        self.cols = 5
        self.rows = 5
        self.turn_counter = 1
        self.graphic_representation = []
        self.possible_moves = []
        self.moving = False
        self.moveable_to = []
        self.clicked_button = None
        self.game_over_text = None

    def initialize_board(self):
        for row in range(5):
            current_list = []
            for column in range(5):
                button = Tile(row, column, self)
                current_list.append(button)
                self.add_widget(button)
            self.graphic_representation.append(current_list)

    def end_game_text(self):
        self.game_over_text = Button(text="Game over")
        self.game_over_text.size = [600, 100]
        self.game_over_text.x = 100
        self.game_over_text.y = 350
        self.game_over_text.font_size = 70
        self.game_over_text.color = (1, 125, 250, 1)
        self.add_widget(self.game_over_text)

    def general_win_check(self):
        self.board.guard_win_check()
        self.board.musketeer_win_check()


class Tile(ButtonBehavior, Image):
    def __init__(self, line, column, graphic_board, **kwargs):
        self.clicked = False
        self.graphic_board = graphic_board
        ButtonBehavior.__init__(self, **kwargs)
        self.line = line
        self.column = column
        self.type = types_dictionary["empty"]
        Image.__init__(self, **kwargs)
        self.type = self.graphic_board.board.grid[self.line][self.column]
        self.source = pictures_dictionary[self.type]

    def get_type(self):
        return self.type
    def highlight_movement_options(self):
        for direction in ([1, 0], [-1, 0], [0, 1], [0, -1]):
            if 0 <= self.line + direction[0] < 5 and 0 <= self.column + direction[1] < 5:
                button_direction = self.graphic_board.graphic_representation[self.line + direction[0]][
                    self.column + direction[1]]
                if (button_direction.type == types_dictionary["guard"] and self.type == types_dictionary["musketeer"]) \
                        or (
                        button_direction.type == types_dictionary["empty"] and self.type == types_dictionary["guard"]):
                    button_direction.color = (50, 120, 10, 5)
                    self.graphic_board.moveable_to.append(button_direction)

    def dehighlight_movement_options(self):
        for button in self.graphic_board.moveable_to:
            button.color = (1, 1, 1, 1)

    def on_press(self):
        self.graphic_board.board.guard_win_check()
        self.graphic_board.board.musketeer_win_check()
        if self.graphic_board.board.game_over:
            self.graphic_board.end_game_text()
        elif self.graphic_board.moving and self in self.graphic_board.moveable_to:
            self.clicked = not self.clicked
            self.source = self.graphic_board.clicked_button.source
            self.type = self.graphic_board.clicked_button.type
            if None != self.graphic_board.clicked_button:
                self.graphic_board.clicked_button.source = "pics/kappa.png"
                self.graphic_board.clicked_button.type = types_dictionary["empty"]
            for button in self.graphic_board.moveable_to:
                button.color = (1, 1, 1, 1)
            self.graphic_board.moveable_to = []
            current_button = self.graphic_board.clicked_button
            if self.graphic_board.board.turn_counter % 2 != 0:
                self.graphic_board.board.grid[current_button.line][current_button.column] = "-"
                self.graphic_board.board.grid[self.line][self.column] = "M"
                self.graphic_board.board.turn_counter += 1
                self.graphic_board.board.guard_win_check()
                self.graphic_board.board.musketeer_win_check()
                self.graphic_board.board.print_board()
                self.graphic_board.clicked_button.clicked = False
            else:
                self.graphic_board.board.grid[current_button.line][current_button.column] = "-"
                self.graphic_board.board.grid[self.line][self.column] = "G"
                self.graphic_board.board.turn_counter += 1
                self.graphic_board.board.guard_win_check()
                self.graphic_board.board.musketeer_win_check()
                self.graphic_board.board.print_board()
                self.graphic_board.clicked_button.clicked = False


            self.graphic_board.clicked_button = None
            self.graphic_board.moving = False


        elif not self.graphic_board.moving and not self.type == types_dictionary["empty"]:
            if (self.graphic_board.board.turn_counter % 2 == 0 and self.type == types_dictionary["guard"]) \
                    or (1 == self.graphic_board.board.turn_counter % 2 and self.type == types_dictionary["musketeer"]):
                self.clicked = not self.clicked

                if self.clicked:
                    self.graphic_board.clicked_button = self
                    for direction in ([1, 0], [-1, 0], [0, 1], [0, -1]):
                        if 0 <= self.line + direction[0] < 5 and 0 <= self.column + direction[1] < 5:
                            button_direction = self.graphic_board.graphic_representation[self.line + direction[0]][
                                self.column + direction[1]]
                            if (button_direction.type == types_dictionary["guard"] and self.type == types_dictionary["musketeer"]) \
                                    or (button_direction.type == types_dictionary["empty"] and self.type == types_dictionary["guard"]):
                                button_direction.color = (50, 120, 10, 5)
                                self.graphic_board.moveable_to.append(button_direction)

                    self.graphic_board.moving = True
                else:
                    for direction in ([1, 0], [-1, 0], [0, 1], [0, -1]):
                        if 0 <= self.line + direction[0] < 5 and 0 <= self.column + direction[1] < 5:
                            self.graphic_board.graphic_representation[self.line + direction[0]][
                                self.column + direction[1]].color = (
                                1, 1, 1, 1)


position_dictionary = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}
letter_dictionary = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}


class Board(object):
    grid = [["G", "G", "G", "G", "M"],
            ["G", "G", "G", "G", "G"],
            ["G", "G", "M", "G", "G"],
            ["G", "G", "G", "G", "G"],
            ["M", "G", "G", "G", "G"]]

    game_over = False

    winning_piece = "-"

    missing_piece = "-"

    turn_counter = 1

    def print_board(self):
        counter = 0
        print("    1  2  3  4  5")
        for rows in self.grid:
            print(letter_dictionary[counter] + "| ", end=" ")
            for cols in rows:
                print(cols + " ", end=" ")
            counter += 1
            print(" \t")

    def move_musk(self, piece):
        position_of_piece = [position_dictionary[piece[0]], eval(piece[1]) - 1]
        piece = piece.lower()
        if self.grid[position_of_piece[0]][position_of_piece[1]] == "M":
            if "u" in piece and "p" in piece:
                if position_of_piece[0] != 0 and self.grid[position_of_piece[0] - 1][position_of_piece[1]] == "G":
                    self.grid[position_of_piece[0]][position_of_piece[1]] = self.missing_piece
                    self.grid[position_of_piece[0] - 1][position_of_piece[1]] = "M"
                else:
                    print
                    "invalid move"
                    self.move_musk(input())
                    return
            if "d" in piece and "o" in piece and "w" in piece and "n" in piece:
                if position_of_piece[0] != 4 and self.grid[position_of_piece[0] + 1][position_of_piece[1]] == "G":
                    self.grid[position_of_piece[0]][position_of_piece[1]] = self.missing_piece
                    self.grid[position_of_piece[0] + 1][position_of_piece[1]] = "M"
                else:
                    print("invalid move")
                    self.move_musk(input())
                    return
            if "l" in piece and "e" in piece and "f" in piece and "t" in piece:
                if position_of_piece[1] != 0 and self.grid[position_of_piece[0]][position_of_piece[1] - 1] == "G":
                    self.grid[position_of_piece[0]][position_of_piece[1]] = self.missing_piece
                    self.grid[position_of_piece[0]][position_of_piece[1] - 1] = "M"
                else:
                    print("invalid move")
                    self.move_musk(input())
                    return
            if "r" in piece and "i" in piece and "g" in piece and "h" in piece and "t" in piece:
                if position_of_piece[1] != 4 and self.grid[position_of_piece[0]][position_of_piece[1] + 1] == "G":
                    self.grid[position_of_piece[0]][position_of_piece[1]] = self.missing_piece
                    self.grid[position_of_piece[0]][position_of_piece[1] + 1] = "M"
                else:
                    print("invalid move")
                    self.move_musk(input())
                    return
        else:
            print("invalid move")
            self.move_musk(input())

    def move_guard(self, piece):
        position_of_piece = [position_dictionary[piece[0]], eval(piece[1]) - 1]
        if self.grid[position_of_piece[0]][position_of_piece[1]] == "G":
            if "u" in piece and "p" in piece:
                if position_of_piece[0] != 0 and self.grid[position_of_piece[0] - 1][position_of_piece[1]] == "-":
                    self.grid[position_of_piece[0]][position_of_piece[1]] = self.missing_piece
                    self.grid[position_of_piece[0] - 1][position_of_piece[1]] = "G"
                else:
                    print("invalid move")
                    self.move_guard(input())
                    return
            if "d" in piece and "o" in piece and "w" in piece and "n" in piece:
                if position_of_piece[0] != 4 and self.grid[position_of_piece[0] + 1][position_of_piece[1]] == "-":
                    self.grid[position_of_piece[0]][position_of_piece[1]] = self.missing_piece
                    self.grid[position_of_piece[0] + 1][position_of_piece[1]] = "G"
                else:
                    print("invalid move")
                    self.move_guard(input())
                    return
            if "l" in piece and "e" in piece and "f" in piece and "t" in piece:
                if position_of_piece[1] != 0 and self.grid[position_of_piece[0]][position_of_piece[1] - 1] == "-":
                    self.grid[position_of_piece[0]][position_of_piece[1]] = self.missing_piece
                    self.grid[position_of_piece[0]][position_of_piece[1] - 1] = "G"
                else:
                    print("invalid move")
                    self.move_guard(input())
                    return
            if "r" in piece and "i" in piece and "g" in piece and "h" in piece and "t" in piece:
                if position_of_piece[1] != 4 and self.grid[position_of_piece[0]][position_of_piece[1] + 1] == "-":
                    self.grid[position_of_piece[0]][position_of_piece[1]] = self.missing_piece
                    self.grid[position_of_piece[0]][position_of_piece[1] + 1] = "G"
                else:
                    print("invalid move")
                    self.move_guard(input())
                    return
        else:
            print("invalid move")
            self.move_guard(input())

    def check_adjacent(self, row, col, direction):
        if direction == "left":
            if col == 0:
                return "-"
            else:
                return self.grid[row][col - 1]

        if direction == "right":
            if col == len(self.grid[row]) - 1:
                return "-"
            else:
                return self.grid[row][col + 1]
        if direction == "up":
            if row == 0:
                return "-"
            else:
                return self.grid[row - 1][col]
        if direction == "down":
            if row == len(self.grid) - 1:
                return "-"
            else:
                return self.grid[row + 1][col]

    def has_legal_moves(self, piece_row, piece_col):
        piece = self.grid[piece_row][piece_col]
        if piece == "M":
            desired_game_piece = 'G'
        else:
            desired_game_piece = '-'
        return any(self.check_adjacent(piece_row, piece_col, direction) == desired_game_piece for direction in
                   ("up", "down", "left", "right"))

    def musketeer_win_check(self):
        free_counter = 0
        for rows in range(len(self.grid)):
            for cols in range(len(self.grid[rows])):
                if self.grid[rows][cols] == "M":
                    if not self.has_legal_moves(rows, cols):
                        free_counter += 1
        if free_counter == 3:
            self.game_over = True
            self.winning_piece = "M"

    def guard_win_check(self):
        musketeers = []
        if not self.game_over:
            for rows in range(len(self.grid)):
                for cols in range(len(self.grid[rows])):
                    if self.grid[rows][cols] == "M":
                        musketeers.append([rows, cols])
            if (musketeers[0][1] == musketeers[1][1] == musketeers[2][1]) or (musketeers[0][0] == musketeers[1][0] == musketeers[2][0]):
                self.game_over = True
                self.winning_piece = "G"
