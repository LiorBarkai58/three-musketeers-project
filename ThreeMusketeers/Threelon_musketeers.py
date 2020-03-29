from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen

from ThreeMusketeers.Board import Board, GraphicBoard


board = Board()
graphicGrid = GraphicBoard(board, "M")
graphicGrid.initialize_board()

Builder.load_string(""" 
<Menu>: 
    BoxLayout: 
        Button: 
            text: "Play" 
            background_color : 0, 0, 1, 1 
            on_press: 
                # You can define the duration of the change 
                # and the direction of the slide 
                root.manager.transition.direction = 'left' 
                root.manager.transition.duration = 1 
                root.manager.current = 'Game'
        Button: 
            text: "Rules" 
            background_color : 0, 0, 1, 1 
            on_press: 
                # You can define the duration of the change 
                # and the direction of the slide 
                root.manager.transition.direction = 'left' 
                root.manager.transition.duration = 1 
                root.manager.current = 'rules' 

<rules>: 
    GridLayout: 
        Button:
            text: "Back to menu"
            center_x: 50
            center_y: 50
            size: 100, 100
            id: rtrn
            on_press:
                root.manager.transition.direction = 'right'
                app.root.current = 'Menu'
            Image:
                source: "Pics\\guard.png"
                center_x: 50
                center_y: 50
                size: 100, 100

<Game>: 
    BoxLayout: 
        Button: 
            text: "Go to Screen 4" 
            background_color : 1, 0, 1, 1 
            on_press: 
                root.manager.transition.direction = 'left' 
                root.manager.transition.duration = 1 
                root.manager.current = 'Menu' 
""")

class Game(Screen):

    pass
class rules(Screen):
    pass
class Menu(Screen):
    pass

# Menu = Screen(name='Menu')
# Game = Screen(name='Game')
# rules = Screen(name='rules')

sm = ScreenManager()
menu = Menu(name="Menu")
rules = rules(name="rules")
sm.add_widget(menu)
sm.add_widget(Game(name="Game"))
sm.add_widget(rules)







class TestApp(App):
    def build(self):
        self.title = 'ThreeMusketeers'
        return sm


TestApp().run()


while not board.game_over:
    board.print_board()
    board.move_musk(input())
    board.print_board()
    board.move_guard(input())

print("The winning piece was ", board.winning_piece)
