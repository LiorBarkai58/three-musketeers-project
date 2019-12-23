from kivy.app import App

from Board import Board, GraphicBoard

board = Board()

class TestApp(App):
    def build(self):
        self.title = 'ThreeMusketeers'
        return board.graphicGrid


TestApp().run()


while not board.game_over:
    board.print_board()
    board.move_musk(raw_input())
    board.print_board()
    board.move_guard(raw_input())

print("The winning piece was ", board.winning_piece)
