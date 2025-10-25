from src.game_engine import *
from menu import Menu
from l1 import Level1
from l2 import Level2
from l3 import Level3

menu = Menu()
menu.run()
if menu.quit_after_return:
    print('quitting...')
    exit()
level1 = Level1()
level1.run()
level2 = Level2()
level2.run()
