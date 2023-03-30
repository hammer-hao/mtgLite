import numpy as np
import random
from tqdm import tqdm
import pandas as pd
from model_combat import creatures_list

creatures_pool=[[1,1], [2,2], [2,1], [1,2], [2,3], [3,3], [3,2], [3,1], [2,4], [4,4], [4,2], [3,5], [5,5]]

def lineup_to_array(lineup_list):
    lineup=[]
    empty=[0,0]
    for i in lineup_list:
        #print(i[-1])
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
    #print('decision is'+str(maxed_list))
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
    #print('attacking:'+str(attackers))
    #print('blocking:'+str(defenders))
    #print('blocking formation:'+str(blocking_arr))
    totaldamage=0
    for idx, row in enumerate(attackers):
        if idx in blocking_arr:
            defenders_ids=np.where(blocking_arr==idx)[0].tolist()
            #print('blocker(s) of attacker ' + str(idx) + ' is:' + str(defenders_ids))
            blocker_size=np.zeros(2)
            for blocker_id in defenders_ids:
                blocker_size=blocker_size+defenders[blocker_id]
            if (row[0]>=blocker_size[1])&(blocker_size[0]>=row[1]):
                pass
                #all creatures die
                #print('all creature dies')
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
            #print('attacker ' + str(idx) + ' is not blocked')
            surviving_attacker[surviving_attackercount,:]=row
            surviving_attackercount+=1
            totaldamage+=row[0]
    return surviving_attacker, surviving_blocker, totaldamage

def process_turn(player0attacking:bool, playerlife:np.array, player0Lineup, player1Lineup):
    if player0attacking==True:
        attackers=player0Lineup
        blockers=player1Lineup
    else:
        attackers=player1Lineup
        blockers=player0Lineup
    #each player recieves a random creature
    if len(attackers)<7:
        attackers.append(random.choice(creatures_list))
    if len(blockers)<7:
        blockers.append(random.choice(creatures_list))
    numattacking=random.randint(0, len(attackers))
    #random attack
    attacking_creatures=random.sample(attackers, numattacking)
    attacking_decision=[(creature in attacking_creatures) for creature in attackers]
    #record the decision to attack
    attack_state_action=record_state_action(life=playerlife, playerbool=player0attacking, attack_lineup=attackers, block_lineup=blockers, deciding_player=(1-player0attacking), attacking_decision=attacking_decision)
    attacking_lineup=lineup_to_array(attacking_creatures)
    blocking_lineup=lineup_to_array(blockers)
    if (len(attacking_creatures)>=1) & (len(blockers)>=1):
        #at least one attacker and one blocker
        defending_matrix=gen_random_decision(int(len(blockers)), int(len(attacking_creatures)))
        block_state_action=record_state_action(life=playerlife, playerbool=not(player0attacking), attack_lineup=attackers, block_lineup=blockers, deciding_player=player0attacking, attacking_creatures=attacking_creatures, blocking_matrix= defending_matrix)
        surviving_attacker, surviving_blocker, totaldamage = resolve_damage(attacking_lineup, blocking_lineup, defending_matrix)
        playerlife[player0attacking]-=totaldamage
        for creature in attacking_creatures:
            attackers.remove(creature)
        attackers_left=attackers+surviving_attacker[surviving_attacker!=0].reshape(-1,2).tolist()
        blockers_left=surviving_blocker[surviving_blocker!=0].reshape(-1,2).tolist()
    elif (len(attacking_creatures)>=1) & (len(blockers)<1):
        block_state_action=record_state_action(life=playerlife, playerbool=not(player0attacking), attack_lineup=attackers, block_lineup=blockers, deciding_player=player0attacking, attacking_creatures=attacking_creatures)
        #no blockers available
        totaldamage=0
        #all creatures deal damage
        for creature in attacking_creatures:
            totaldamage+=creature[0]
        playerlife[player0attacking]-=totaldamage
        attackers_left=attackers
        blockers_left=blockers
    elif (len(attacking_creatures)<1) & (len(blockers)>=1):
        block_state_action=record_state_action(life=playerlife, playerbool=not(player0attacking), attack_lineup=attackers, block_lineup=blockers, deciding_player=player0attacking, attacking_creatures=attacking_creatures)
        #no attackers, yes blockers
        totaldamage=0
        playerlife[player0attacking]-=totaldamage
        attackers_left=attackers
        blockers_left=blockers
    else:
        block_state_action=record_state_action(life=playerlife, playerbool=not(player0attacking), attack_lineup=attackers, block_lineup=blockers, deciding_player=player0attacking, attacking_creatures=attacking_creatures)
        #no blockers but did not attack either
        totaldamage=0
        playerlife[player0attacking]-=totaldamage
        attackers_left=attackers
        blockers_left=blockers
    s_a=pd.concat([attack_state_action, block_state_action])
    return playerlife, attackers_left, blockers_left, s_a

def game():
    life=np.array([20,20])
    player0=[]
    player1=[]
    P0attacking=random.randint(0,1)
    log=pd.DataFrame()
    while np.all(life>0):
        life, attackerleft, blockerleft, s_a = process_turn(player0attacking=P0attacking, playerlife=life, player0Lineup=player0, player1Lineup=player1)
        if P0attacking==1:
            player0=attackerleft
            player1=blockerleft
        else:
            player0=blockerleft
            player1=attackerleft
        P0attacking=1-P0attacking
        log=pd.concat([log, s_a])
        #print('life: '+str(life))
    if life[0]>0.5:
        log.iloc[:,-1]=1-log.iloc[:,-1]
    return log

def record_state_action(life, playerbool, attack_lineup, block_lineup, deciding_player, attacking_creatures=None, attacking_decision=None, blocking_matrix=None):
    attack=lineup_to_array(attack_lineup)
    block=lineup_to_array(block_lineup)
    if playerbool==False:
        life=np.flip(life)
        controllingplayer=np.array([1])
    else:
        controllingplayer=np.array([0])
    if attacking_decision is None:
        attacking_decision=np.zeros(7)
    try:
        attackcr=lineup_to_array(attacking_creatures)
    except TypeError:
        attackcr=np.zeros(14)
    try:
        blockformation=blocking_matrix.flatten()
    except AttributeError:
        blockformation=np.zeros(49)
    df=pd.DataFrame(np.hstack([life, attack, block, np.pad(np.array(attacking_decision), (0, int(7-len(attacking_decision))), 'constant'), np.array(deciding_player), attackcr, blockformation, controllingplayer])).T
    return df