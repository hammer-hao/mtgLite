class game:
    counter = 0
    def __init__(self):
        self.isActive=True
        self.id=game.counter
        game.counter+=1
        self.player0=player()
        self.player1=player()

class player:
    counter = 0
    def __init__(self):
        self.lifetotal=20
        self.id=player.counter
        player.counter+=1
        self.isalive=True
        self.library=library()
        self.hand=hand()
    def drawCard(self):
        self.library.drawTop()
        self.hand.addCard()

class library:
    def __init__(self):
        self.cardCount=60
    def drawTop(self):
        self.cardCount-=1

class hand:
    def __init__(self):
        self.cardCount=0
    def addCard(self):
        self.cardCount+=1

class Card:
    def __init__(self, name=str, art=str, color=str, isLegendary=bool):
        self.name=name
        self.art=art
        self.color=color
        self.isLegendary=isLegendary
