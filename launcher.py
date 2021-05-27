import pygame
import pygame_menu
from pygame_menu import Theme
from game import Game
from settings.screen import Screen

pygame.init()
pygame.display.set_caption("Q-LEARNING")
screen = pygame.display.set_mode((300, 500))

def start_the_game():
    pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))
    app = Game(Screen.MATRIX_ROW,Screen.MATRIX_COLUMN)
    app.mainLoop()
    pygame.display.set_mode((300, 500))

def setRow(value):
    Screen.MATRIX_ROW = value
def setColumn(value):
    Screen.MATRIX_COLUMN= value

theme = Theme(  background_color=(40, 40, 40),
                title_background_color=(60, 60, 60),
                widget_padding=15,
                selection_color=(106, 126, 250),
                title_font_color=(106, 126, 250),
                title_font_size=50,
                title_offset= (50,10),
                title_font = pygame_menu.font.FONT_MUNRO,
                widget_font = pygame_menu.font.FONT_MUNRO,
                title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
                )

MenuScreen = pygame_menu.menu.Menu("Q-LEARNING", 300, 500, theme=theme)

MenuScreen.add.text_input('MATRIX X : ', default='10', input_type=pygame_menu.locals.INPUT_INT, onchange=setRow)
MenuScreen.add.text_input('MATRIX Y : ', default='10', input_type=pygame_menu.locals.INPUT_INT, onchange=setColumn)
MenuScreen.add.button('BASLAT', start_the_game)
MenuScreen.add.button('CIKIS', pygame_menu.events.EXIT)
MenuScreen.mainloop(screen)
