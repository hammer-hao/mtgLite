from base import *
import decklist, cardlibrary
import random
from tkinter import *
from tkinter import ttk

class HandFrame(Frame):
    def __init__(self, Master):
        super().__init__()
        self.config(height=300, width=200, highlightbackground='grey', highlightthickness=1)
        self.grid_propagate(0)
    def add_card(self, card:Card, id:int):
        thisframe=Frame(self, width=190, height=30, padx=5, pady=5, highlightbackground='lightblue', highlightthickness=1)
        thisframe.pack_propagate(0)
        thisframe.grid(row=id, column=0)
        thiscard=Label(thisframe, text=card.name)
        thiscard.pack(side='top', fill='both', expand=True)


class StackFrame(Frame):
    def __init__(self, Master):
        super().__init__()
        self.config(height=300, width=200, highlightbackground='grey', highlightthickness=1)
        self.grid_propagate(0)

class LandFrame(Frame):
    def __init__(self, Master):
        super().__init__()
        self.config(height=150, width=600, highlightbackground='grey', highlightthickness=1)

class MiscFrame(Frame):
    def __init__(self, Master):
        super().__init__()
        self.config(height=150, width=200, highlightbackground='grey', highlightthickness=1)

class GameWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title('MTGLite')
        self.geometry('1000x600')
        self.maxsize(1000, 600)
        self.config(bg='lightgrey')
        self.__create_widgets()

    def __create_widgets(self):
        global deck_top
        deck_top = HandFrame(self)
        deck_top.grid(row=0, column=0, rowspan=2, padx=0, pady=0)
        for idx, card in enumerate(game.Player0.hand.cardList):
            deck_top.add_card(card, idx)

        deck_bottom = HandFrame(self)
        deck_bottom.grid(row=2, column=0, rowspan=2, padx=0, pady=0)

        hand_top = LandFrame(self)
        hand_top.grid(row=0, column=1,padx=0, pady=0)

        battlefield_top = LandFrame(self)
        battlefield_top.grid(row=1, column=1,padx=0, pady=0)

        battlefield_bottom = LandFrame(self)
        battlefield_bottom.grid(row=2, column=1,padx=0, pady=0)

        hand_bottom = LandFrame(self)
        hand_bottom.grid(row=3, column=1, padx=0, pady=0)

        misc_top = MiscFrame(self)
        misc_top.grid(row=0, column=2, padx=0, pady=0)

        stack_frame = StackFrame(self)
        stack_frame.grid(row=1, column=2, rowspan=2, padx=0, pady=0)

        misc_bottom = MiscFrame(self)
        misc_bottom.grid(row=3, column=2, padx=0, pady=0)
        
        global lifetotal
        lifetotal=Label(misc_top, text=0, font=('Arial', 35, 'bold'))
        lifetotal.place(x=10, y=10)

        draw=Button(misc_bottom, text='draw', command=onDrawClick).grid(row=0, column=0)
        pass0=Button(misc_bottom, text='pass', command=player0pass).grid(row=1, column=0)
        pass1=Button(misc_top, text='pass', command=player1pass).grid(row=0, column=0)

deck0=decklist.deck1

class Game:
    global lifetotal
    def __init__(self):
        pass
    def start_game(self, decklist0:dict, decklist1:dict):
        deck0=Library()
        for cardname, count in decklist0.items():
            card=cardlibrary.library[cardname]
            if card['card-type']=='land':
                thiscard=LandCard(cardname, card['card-art'], card['card-color'], card['isLegendary'])
            else:
                thiscard=NonLandCard(cardname, card['card-art'], card['card-color'], card['isLegendary'], spelleffect=None)
            for i in range(count):
                deck0.populate(thiscard)
            deck0.shuffle()
        deck1=Library()
        for cardname, count in decklist1.items():
            card=cardlibrary.library[cardname]
            if card['card-type']=='land':
                thiscard=LandCard(cardname, card['card-art'], card['card-color'], card['isLegendary'])
            else:
                thiscard=NonLandCard(cardname, card['card-art'], card['card-color'], card['isLegendary'], spelleffect=None)
            for i in range(count):
                deck1.populate(thiscard)
            deck1.shuffle()
        self.Player0=Player(self, deck0)
        self.Player0.drawCard(1)
        self.Player1=Player(self, deck1)
        self.Player1.drawCard(1)

        x = random.randint(0, 1)
        if x==0:
            self.playingPlayer=self.Player0
            self.reactorPlayer=self.Player1
        else:
            self.playingPlayer=self.Player1
            self.reactorPlayer=self.Player0
        self.current_phase=Main()
        lifetotal.config(text=self.Player0.lifetotal)

    def skip(self):
        if (self.playingPlayer.prioritypassed==True) & (self.reactorPlayer.prioritypassed==True):
            self.current_phase=self.current_phase.next_phase()
            self.playingPlayer.prioritypassed=False
            self.reactorPlayer.prioritypassed=False
        elif (self.playingPlayer.prioritypassed==True) & (self.reactorPlayer.prioritypassed==False):
            print('playingPlayer has passed priority')
        elif (self.playingPlayer.prioritypassed==False) & (self.reactorPlayer.prioritypassed==True):
            print('Cannot pass priority')
            self.reactorPlayer.prioritypassed=False
        else:
            pass

class Player:
    counter = 0
    def __init__(self, game:Game, library:Library):
        self.game=game
        self.lifetotal=20
        self.id=Player.counter
        Player.counter+=1
        self.isalive=True
        self.library=library
        self.hand=hand()
        self.prioritypassed=False
    def drawCard(self, numbertodraw:int):
        self.hand.draw(num=numbertodraw, library=self.library)
    def pass_priority(self):
        self.prioritypassed=True
        self.game.skip()

game=Game()
game.start_game(deck0, deck0)

def player0pass(event=None):
    game.Player0.pass_priority()

def player1pass(event=None):
    game.Player1.pass_priority()

def onDrawClick(event=None):
    game.Player0.drawCard(1)
    deck_top.add_card(game.Player0.hand.cardList[-1], (len(game.Player0.hand.cardList)-1))

if __name__=='__main__':
    game_window=GameWindow()
    game_window.mainloop()
