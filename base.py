import numpy as np
import decklist
from abc import ABC, abstractclassmethod, ABCMeta
from random import shuffle

class Card:
    __metaclass__=ABCMeta
    def __init__(self, name:str, art:str, color:str, isLegendary:bool):
        self.name=name
        self.art=art
        self.color=color
        self.isLegendary=isLegendary
        
class Library:
    def __init__(self):
        self.cardList=[]
        self.cardCount=len(self.cardList)
    def populate(self, card:Card):
        self.cardList.append(card)
    def shuffle(self):
        self.cardlist=shuffle(self.cardList)
    def drawTop(self):
        returncard = self.cardList[-1]
        self.cardList=self.cardList[:-1]
        return returncard

class hand:
    def __init__(self):
        self.cardList=[]
    def addCard(self, card:Card):
        self.cardList.append(card)
        self.cardCount=len(self.cardList)
    def play_card(self, index:int):
        card_to_play=self.cardList[index]
        self.cardList=self.cardList.remove(card_to_play)
        card_to_play.play()
    def draw(self, num:int, library:Library):
        for i in range(num):
            drawncard=library.drawTop()
            self.addCard(card=drawncard)

class Permanent:
    counter=0
    def __init__(self, name:str, color:str, isLegendary:bool, entersTapped:bool):
        self.id=Permanent.counter
        Permanent.counter+=1
        self.name=name
        self.color=color
        self.isLegendary=isLegendary
        self.tapped=entersTapped
        self.inBattleField=True
    def tap(self):
            self.tapped=True
    def untap(self):
            self.tapped=False
    def leaveBattlefeild(self):
        self.inBattleField=False

class Creature(Permanent):
    def __init__(self, name:str, color:str, isLegendary:bool, entersTapped:bool, size:np.array, creaturetype:str):
        super().__init__(name, color, isLegendary, entersTapped)
        self.size=size
        self.type=creaturetype
        self.isAlive=True
        self.summoningSickness=True
    def dealCombatDamage(self, target):
        if hasattr(target, 'recieveDamage'):
            target.recieveDamage(self.size[0])
        else:
            print('no arribute')
    def recieveDamage(self, damage):
        self.size[1]-=damage
        self.checkAlive()
    def checkAlive(self):
        if self.size[1]<=0:
            self.isAlive=False
        else:
            self.isAlive=True

class Land(Permanent):
    def __init__(self, name:str, color:str, isLegendary:bool, entersTapped:bool):
        super().__init__(name, color, isLegendary, entersTapped)

    @abstractclassmethod
    def play(self):
        #play the card
        return

class Effect(ABC):
    @abstractclassmethod
    def execute():
        pass

class summonCreature(Effect):
    def __init__(self, creature_to_summon:Creature):
        self.creature_to_summon=creature_to_summon
    def execute(self):
        Battlefield.addpermanent(self.creature_to_summon)

class LandCard(Card):
    def __init__(self, name:str, art:str, color:str, isLegendary:bool):
        super().__init__(name, art, color, isLegendary)
    def play(self):
        thisland=Land(self.name, self.color, self.isLegendary, False)
        Battlefield.addpermanent(thisland) 

class NonLandCard(Card):
    def __init__(self, name:str, art:str, color:str, isLegendary:bool, spelleffect:Effect):
        super().__init__(name, art, color, isLegendary)
        self.spell=Spell
    def play(self):
        stack.addspell(self.spell)

class Battlefield:
    def __init__(self):
        self.noLands=0
        self.noCreatures=0
        self.noArtifacts=0
        self.noEnchantments=0
        self.noPermanents=(self.noLands+self.noCreatures+self.noArtifacts+self.noEnchantments)
        self.permanents=[]
    def addpermanent(self, permanent:Permanent):
        self.permanents.append(permanent)
        self.noPermanents+=1

class Spell:
    def __init__(self, color:str, manacost:str, effect):
        self.color=color
        self.manacost=manacost
        self.effect=effect
    def resolve(self):
        self.effect.execute()

class stack:
    def __init__(self):
        self.spellList=[]
    def addspell(self, spell=Spell):
        self.spellList.append(spell)
    def resolvenext(self):
        self.spellList[-1].resolve()
        self.spellList=self.spellList[:-1]

class Phase(ABC):
    def __init__(self):
        self.thisphase='thisphase'
        self.next_phase=Phase
        print('current phase is ' + self.thisphase)
    @abstractclassmethod
    def next_phase(self):
        pass

class Upkeep(Phase):
    def __init__(self):
        self.thisphase='Upkeep'
        print('current phase is ' + self.thisphase)
    def next_phase(self):
        print('exiting'+self.thisphase)
        self.nextphase=Main()
        return self.nextphase

class Main(Phase):
    def __init__(self):
        self.thisphase='Main'
        print('current phase is ' + self.thisphase)
    def next_phase(self):
        print('exiting'+self.thisphase)
        self.nextphase=BeginCombat()
        return self.nextphase

class BeginCombat(Phase):
    def __init__(self):
        self.thisphase='BeginCombat'
        print('current phase is ' + self.thisphase)
    def next_phase(self):
        print('exiting'+self.thisphase)
        self.nextphase=EndCombat()
        return self.nextphase

class EndCombat(Phase):
    def __init__(self):
        self.thisphase='EndCombat'
        print('current phase is ' + self.thisphase)
    def next_phase(self):
        print('exiting'+self.thisphase)
        self.nextphase=SecondMain()
        return self.nextphase

class SecondMain(Phase):
    def __init__(self):
        self.thisphase='SecondMain'
        print('current phase is ' + self.thisphase)
    def next_phase(self):
        print('exiting'+self.thisphase)
        self.nextphase=EndStep()
        return self.nextphase

class EndStep(Phase):
    def __init__(self):
        self.thisphase='EndStep'
        print('current phase is ' + self.thisphase)
    def next_phase(self):
        print('exiting'+self.thisphase)
        self.nextphase=Upkeep()
        return self.nextphase