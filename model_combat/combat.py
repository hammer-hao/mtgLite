import numpy as np
import random

def lineup_to_array(lineup_list):
    lineup=[]
    empty=[0,0]
    for i in lineup_list:
        print(i[-1])
        if i[-1]>0:
            lineup+=i
        else:
            print('something wrong! creature have 0 toughness!')
    for i in range(7-len(lineup_list)):
        lineup+=empty
    array=np.array(lineup)
    return array

def softmax_n(array):
        probs=(np.exp(array)/np.sum(np.exp(array)))
        newarray=np.zeros(len(array))
        id=np.argmax(probs)
        newarray[id]=1
        return newarray

def gen_random_decision(n_attackers, n_blockers):
    decision=np.random.random((n_blockers, n_attackers+1))
    maxed_list=[softmax_n(row) for row in decision]
    this_decision=np.vstack(maxed_list)
    if (n_attackers!=7) and (n_blockers!=7):
        decision_matrix_active=np.pad(this_decision[:,:-1], ((0,(7-n_blockers)),(0,(7-n_attackers))), mode='constant', constant_values=0)
    elif (n_attackers!=7):
        decision_matrix_active=np.pad(this_decision[:,:-1], ((0,0),(0,(7-n_attackers))), mode='constant', constant_values=0)
    elif (n_blockers!=7):
        decision_matrix_active=np.pad(this_decision[:,:-1], ((0,(7-n_blockers)),(0,0)), mode='constant', constant_values=0)
    else:
        decision_matrix_active=this_decision
    return decision_matrix_active


def resolve_damage(attackingarray, defendingarray, defendingdecision):
    attackers=attackingarray.reshape(7, 2).tolist()
    defenders=defendingarray.reshape(7, 2).tolist()
    defend_matrix=defendingdecision.tolist()
    blocking_list=[]
    surviving_attacker=np.zeros(shape=(7,2))
    surviving_blocker=np.zeros(shape=(7,2))
    surviving_blockercount=0
    surviving_attackercount=0
    for idx, row in enumerate(defend_matrix):
        if defenders[idx][-1]<0.5:
            continue
        elif np.max(row)<0.5:
            blocking=8
            surviving_blocker[surviving_blockercount,:]=defenders[idx]
            surviving_blockercount+=1
        else:
            blocking= np.argmax(row)
        blocking_list.append(blocking)
    blocking_arr=np.array(blocking_list)
    print('attacking:'+str(attackers))
    print('blocking:'+str(defenders))
    print('blocking formation:'+str(blocking_arr))
    totaldamage=0
    for idx, row in enumerate(attackers):
        if idx in blocking_arr:
            defenders_ids=np.where(blocking_arr==idx)[0].tolist()
            print('blocker(s) of attacker ' + str(idx) + ' is:' + str(defenders_ids))
            blocker_size=np.zeros(2)
            for blocker_id in defenders_ids:
                blocker_size=blocker_size+defenders[blocker_id]
            if (row[0]>=blocker_size[1])&(blocker_size[0]>=row[1]):
                #all creatures die
                print('all creature dies')
            elif (row[0]>=blocker_size[1])&(blocker_size[0]<row[1]):
                #all blockers die, attacker survives
                surviving_attacker[surviving_attackercount,:]=row
                surviving_attackercount+=1
            elif (row[0]<blocker_size[1])&(blocker_size[0]>=row[1]):
                #at least one blocker survives, attacker dies
                if sum(np.array([defenders[defender_id][1] for defender_id in defenders_ids])>row[0])==len(np.array([defenders[defender_id][1] for defender_id in defenders_ids])):
                    #both blockers survive
                    for survivor in defenders_ids:
                        surviving_blocker[surviving_blockercount,:]=defenders[survivor]
                        surviving_blockercount+=1
                elif sum(np.array([defenders[defender_id][1] for defender_id in defenders_ids])>row[0])<len(np.array([defenders[defender_id][1] for defender_id in defenders_ids])):
                    #not all blockers survive, prioritize those with greater toughness
                    blockers_list=[defenders[defender_id] for defender_id in defenders_ids]
                    surviving_defender=sorted(blockers_list, key= lambda x: (x[1], x[0]), reverse=False)
                    excessdamage=row[0]
                    survivors=surviving_defender
                    for blocker in surviving_defender:
                        excessdamage-=blocker[1]
                        if excessdamage>=0:
                            survivors.remove(blocker)
                    for survivor in survivors:
                        surviving_blocker[surviving_blockercount,:]=survivor
                        surviving_blockercount+=1
            elif (row[0]<blocker_size[1])&(blocker_size[0]>=row[1]):
                #at least one blocker survives, attacker survives
                if sum(np.array([defenders[defender_id] for defender_id in defenders_ids])>row[0])==len(np.array([defenders[defender_id] for defender_id in defenders_ids])>row[0]):
                    #both blockers survive
                    for survivor in defenders_ids:
                        surviving_blocker[surviving_blockercount,:]=survivor
                        surviving_blockercount+=1
                elif sum(np.array([defenders[defender_id] for defender_id in defenders_ids])>row[0])<len(np.array([defenders[defender_id] for defender_id in defenders_ids])>row[0]):
                    #not all blockers survive, prioritize those with greater toughness
                    blockers_list=[defenders[defender_id] for defender_id in defenders_ids]
                    surviving_defender=sorted(blockers_list, key= lambda x: (x[2], x[1]), reverse=False)
                    excessdamage=row[0]
                    survivors=surviving_defender
                    for blocker in surviving_defender:
                        excessdamage-=blocker[1]
                        if excessdamage>=0:
                            survivors.remove(blocker)
                    for survivor in survivors:
                        surviving_blocker[surviving_blockercount,:]=defenders[survivor]
                        surviving_blockercount+=1
                surviving_attacker[surviving_attackercount,:]=row
                surviving_attackercount+=1
        else:
            #not blocked
            print('attacker ' + str(idx) + ' is not blocked')
            surviving_attacker[surviving_attackercount,:]=row
            surviving_attackercount+=1
            totaldamage+=row[0]
    return surviving_attacker, surviving_blocker, totaldamage

creature_pool=[[1,1], [2,2], [2,1], [1,2], [2,3], [3,3], [3,2], [3,1], [2,4], [4,4], [4,2], [3,5], [5,5]]

def process_turn(player0attacking:bool, playerlife:np.array, player0Lineup, player1Lineup):
    if player0attacking==True:
        attackers=player0Lineup
        blockers=player1Lineup
    else:
        attackers=player1Lineup
        blockers=player0Lineup
    #each player recieves a random creature
    if len(attackers)<7:
        attackers.append(random.choice(creature_pool))
    if len(blockers)<7:
        blockers.append(random.choice(creature_pool))
    numattacking=random.randint(0, len(attackers))
    #random attack
    attacking_creatures=random.sample(attackers, numattacking)
    attacking_lineup=lineup_to_array(attacking_creatures)
    blocking_lineup=lineup_to_array(blockers)
    defending_matrix=gen_random_decision(int(len(blockers)), int(len(attacking_creatures)))
    surviving_attacker, surviving_blocker, totaldamage = resolve_damage(attacking_lineup, blocking_lineup, defending_matrix)
    playerlife[player0attacking]-=totaldamage
    for creature in attacking_creatures:
        attackers.remove(creature)
    attackers_left=attackers+surviving_attacker[surviving_attacker!=0].tolist()
    blockers_left=surviving_blocker[surviving_blocker!=0].tolist()
    return playerlife, attackers_left, blockers_left

def game():
    life=np.array([20,20])
    player0=[]
    player1=[]
    P0attacking=random.randint(0,1)
    while np.any(life>=0):
        life, attackerleft, blockerleft = process_turn(player0attacking=P0attacking, playerlife=life, player0Lineup=player0, player1Lineup=player1)
        if P0attacking==1:
            player0=attackerleft
            player1=blockerleft
        else:
            player0=blockerleft
            player1=attackerleft
        P0attacking=1-P0attacking
        print('life: '+str(life))
        

def gen_stateaction_pair(attacking_lineup, blocking_lineup, state:bool, attacking_creatures=None, blocking_matrix=None):
    pass
