import numpy as np

class Creature():
    def __init__(self, power:int, toughness:int):
        self.power=power
        self.toughness=toughness
        self.blockedby=None

class lineup():
    def __init__(self, attacking:bool, *creatures:Creature):
        self.attacking=attacking
        #populate creatures
        self.members=[]
        for creature in creatures:
            if creature.toughness>0:
                self.members.append(creature)
            else:
                print('something wrong! creature have 0 toughness!')
        for i in range(7-len(creatures)):
            print(i)
            self.members+=Creature(0,0)

    def compute_size(self):
        size = lambda power, toughness: power**0.5+toughness**0.5
        sizes=np.zeros(7)
        for idx, member in enumerate(self.members):
            sizes[idx]=size(member.power, member.toughness)
        self.sizes=sizes

    def sort(self):
        self.compute_size()
        ranks=self.sizes.argsort().argsort()
        sorted=[i for i in range(7)]
        for idx, rank in enumerate(ranks):
            sorted[rank] = self.members[idx]
        self.members=sorted

def gen_decision(attackinglineup:lineup, blockinglineup:lineup, idlelineup:lineup, weights, temperature):
    #generates blocking decision using softmax function which converts closeness of agresiveness to sizes into a probability density function
    attackinglineup.sort()
    #sort ascending
    sizes=attackinglineup.sizes
    adjusted_sizes=sizes*(1/sizes.max())
    adjusted_sizes=np.insert(adjusted_sizes, 0, 0)
    blocking_decision=[]
    for idx, agent in enumerate(blockinglineup.members):
        agressiveness_parameter=weights[idx]
        closeness=(1-np.abs(agressiveness_parameter-adjusted_sizes))
        pi=(np.exp(closeness/temperature)/np.exp(closeness/temperature).sum())
        choice=np.random.choice(np.arange(0,8), p=pi)
        blocking_decision.append(choice)
    print('decision:')
    print(np.array(blocking_decision))
    print('temperature: '+str(temperature))
    print(' pdf: '+str(pi))
    return np.array(blocking_decision)

def resolve_damage(attackinglineup:lineup, defendinglineup:lineup, blocking_choice):
    for attacker in attackinglineup.members:
        
    pass
        
test_list=[[1,1], [2,2], [2,5], [1,2], [2,3], [3,3], [3,2]]
test_lineup = lineup(True, Creature(1,1), Creature(2,2), Creature(2,5), Creature(1,2), Creature(2,3), Creature(3,3), Creature(3,2))
test_lineup.sort()

test_weights=np.array([0.1,0.2,0.3,0.4,0.5,0.6,0.7])

rand_choice = gen_decision(test_lineup, test_lineup, test_lineup, test_weights, 0.2)
resolve_damage(test_lineup.members, test_lineup.members, rand_choice)