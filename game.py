from base import *
import decklist, game, cardlibrary

def startgame(decklist0:dict, decklist1:dict):
    deck0=Library()
    for cardname, count in decklist0.items():
        card=cardlibrary.library[cardname]
        if card['card-type']=='land':
            thiscard=LandCard(card['name'], card['art'], card['isLegendary'])
        else:
            thiscard=NonLandCard(card['name'], card['art'], card['isLegendary'], spelleffect=None)
        for i in count:
            deck0.populate(thiscard)
        deck0.shuffle()
    deck1=Library()
    for cardname, count in decklist1.items():
        card=cardlibrary.library[cardname]
        if card['card-type']=='land':
            thiscard=LandCard(card['name'], card['art'], card['isLegendary'])
        else:
            thiscard=NonLandCard(card['name'], card['art'], card['isLegendary'], spelleffect=None)
        for i in count:
            deck1.populate(thiscard)
        deck1.shuffle()
    Player0=Player(deck0)
    Player1=Player(deck1)
startgame(decklist0=decklist.deck1, decklist1=decklist.deck1)