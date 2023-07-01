import numpy as np

class lineup():
    def __init__(self, attacking:bool, lineup_list):
        self.attacking=attacking
        lineup=[]
        for creature in lineup_list:
        #print(i[-1])
            if creature[-1]>0:
                lineup+=creature
            else:
                print('something wrong! creature have 0 toughness!')
        for i in range(7-len(lineup_list)):
            lineup+=[0,0]
        array=np.array(lineup).reshape(7,2)
        self.members=array
    def compute_size(self):
        size = lambda power, toughness: power**0.5+toughness**0.5
        sizes=np.zeros(7)
        for idx, member in enumerate(self.members):
            sizes[idx]=size(member[0], member[1])
        self.sizes=sizes
    def sort(self):
        self.compute_size()
        ranks=self.sizes.argsort().argsort()
        sorted=np.zeros(14).reshape(7,2)
        for idx, rank in enumerate(ranks):
            sorted[rank] = self.members[idx]
        self.members=sorted

def gen_decision(attackinglineup:lineup, blockinglineup:lineup, idlelineup:lineup, weights, noise):
    #generates blocking decision using softmax function which converts closeness of agresiveness to sizes into a probability density function
    attackinglineup.sort()
    #sort ascending
    sizes=attackinglineup.sizes
    adjusted_sizes=sizes*(1/sizes.max())
    for idx, agent in enumerate(blockinglineup.members):
        agressiveness_parameter=weights[idx]
        closeness=(1-np.abs(agressiveness_parameter-adjusted_sizes))
        pi=(np.exp(closeness)/np.exp(closeness).sum())
        choice=np.random.choice(np.arange(1,8), p=pi)
        print(choice)
        
        
        
        
        
    

test_list=[[1,1], [2,2], [2,5], [1,2], [2,3], [3,3], [3,2]]
test_lineup = lineup(True, test_list)
test_lineup.sort()

test_weights=np.array([0.1,0.2,0.3,0.4,0.5,0.6,0.7])

gen_decision(test_lineup, test_lineup, test_lineup, test_weights, 0)