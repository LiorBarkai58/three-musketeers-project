from kivy.app import App

from ThreeMusketeers.Board import Board

board = Board()

class TestApp(App):
    def build(self):
        self.title = 'ThreeMusketeers'
        return board.graphicGrid


TestApp().run()


while not board.game_over:
    board.print_board()
    board.move_musk(input())
    board.print_board()
    board.move_guard(input())

print("The winning piece was ", board.winning_piece)
