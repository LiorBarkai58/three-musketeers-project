from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

from ThreeMusketeers.Board import Board, GraphicBoard

# Python AI for the game "Three musketeers"
# Note that this code runs on python 3.7 contrary to the default one at our school's labs
#
#
#
#
#
#

#
# Builds the first board that the player is controlling the musketeers and the AI is controlling the guardsmen
#
board = Board()
graphicGridGAI = GraphicBoard(board, "G")
graphicGridGAI.initialize_board()

#
# Builds the first board that the player is controlling the guardsmen and the AI is controlling the musketeers
#
board2 = Board()
graphicGridMAI = GraphicBoard(board2, "M")
graphicGridMAI.initialize_board()


#
# This is the initialization of the screen manager
#
Builder.load_string("""
<Menu>:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            Button:
                text: "Play as musketeers"
                font_size: 25
                background_color : 0, 0, 15, 15
                on_press:
                    # You can define the duration of the change
                    # and the direction of the slide
                    root.manager.current = 'GameGAI'
            Button:
                text: "Play as guardsmen"
                font_size: 25
                background_color : 0, 0, 15, 15
                on_press:
                    # You can define the duration of the change
                    # and the direction of the slide
                    root.manager.current = 'GameMAI'
        Button:
            text: "Rules"
            font_size: 40
            background_color : 0, 0, 15, 15
            on_press:
                # You can define the duration of the change
                # and the direction of the slide
                root.manager.current = 'rules'

<rules>:
    BoxLayout:
        Button:
            text: "Back to menu"
            center_x: 50
            center_y: 50
            size: 100, 100
            id: rtrn
            on_press:
                app.root.current = 'Menu'
        Button:
            text: "Winning Conditions"
            center_x: 750
            center_y: 50
            size: 100, 100
            on_press:
                app.root.current = 'winning'
<winning>:
    BoxLayout:
        Button:
            text: "Back to menu"
            center_x: 50
            center_y: 50
            size: 100, 100
            id: rtrn
            on_press:
                app.root.current = 'Menu'


""")

class Game(Screen):
    pass
class rules(Screen):
    pass
class Menu(Screen):
    pass
class winning(Screen):
    pass


sm = ScreenManager(transition=NoTransition())
menu = Menu(name="Menu")
rules = rules(name="rules")
rules.add_widget(Image(source="Pics\\rules.png"))

winning = winning(name="winning")
winning.add_widget(Image(source="Pics\\winningcon.png"))

gameGAI = Game(name="GameGAI")
gameGAI.add_widget(graphicGridGAI)

gameMAI = Game(name="GameMAI")
gameMAI.add_widget(graphicGridMAI)


sm.add_widget(menu)
sm.add_widget(gameGAI)
sm.add_widget(gameMAI)
sm.add_widget(rules)
sm.add_widget(winning)







class TestApp(App):
    def build(self):
        self.title = 'ThreeMusketeers'
        return sm


TestApp().run()

