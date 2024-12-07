# -*- coding: UTF-8 -*-
import time
from random import randint
from aitool import pip_install


def mouse_move():
    try:
        import pyautogui as pg
    except ModuleNotFoundError:
        pip_install('PyAutoGUI==0.9.20')
        import pyautogui as pg

    while True:
        pg.moveTo(randint(0, 20), randint(0, 20), 2)
        time.sleep(10)


if __name__ == '__main__':
    mouse_move()
