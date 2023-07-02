from base import *
from tkinter import *
from tkinter import ttk
from model_combat import lineup



class CombatWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title('MTGLite Combat')
        self.geometry('1000x600')
        self.maxsize(1000, 600)
        self.config(bg='lightgrey')
        self.__create_widgets()

    def __create_widgets(self):
        pass

if __name__=='__main__':
    game_window=CombatWindow()
    game_window.mainloop()
