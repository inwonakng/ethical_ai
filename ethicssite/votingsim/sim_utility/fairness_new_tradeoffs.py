import numpy as np
from time import time
# from matplotlib import pyplot as plt
from .satisfaction_calc import *
from .fairness_SW_tradeoff import gaussian_ballots_gen, PL_ballots_gen

np.set_printoptions(precision=6)
#Functions needed
#Condorcet_efficiency - if Condorcet winner exists, do we choose them
#Fairness_efficiency - count of positive cases? or expectation of fairness?
#Consistency - how many pairs are consistent

#Voting rules
#Borda
#maximin
#alpha-fairBorda (min UF while SW >= alp'[kha*maxSW)

#vary over n1/n2 and alpha

def borda_utility(votes):
    """
    Description:
        Return Borda utility for each candidate
    """
    n, m = votes.shape
    utilities = np.zeros(m)
    for vote in votes:
        for j in range(m):
            utilities[vote[j]] += m-j-1 
    return utilities/n

def util_uf(votes1, votes2):
    """
    Computes utility and unfairness for ranked utility
    
    Parameters
    ----------
    votes1 : preference profile of group 1
    votes2 : preference profile of group 2

    Returns
    -------
    average social welfare and unfairness for all alternatives
    """
    util1 = borda_utility(votes1)
    util2 = borda_utility(votes2)
    util = borda_utility(np.concatenate((votes1,votes2)))
    
    m = len(util)
    uf = np.zeros(m)
    for j in range(m):
        if(util[j]==0):
            uf[j] = np.nan
        else:
            uf[j] = np.abs(util1[j] - util2[j]) / util[j]
    return util, np.array(uf)

def fair_borda(votes, n1, n2, threshold):
    # minimize unfairness for SW > threshold*maxSW
    # SW computed for ranked utility 
    """
    votes is complete preference profile
    first n1 agents in group1
    next n2 agents in group2
    """
    util, uf = util_uf(votes[:n1], votes[n1:n1+n2])
    m = len(util)
    min_uf = np.inf
    w = m+1
    for j,u in enumerate(util):
        if(u < np.max(util)*threshold):
            continue
        if(np.isnan(uf[j])):
            continue
        if(uf[j] < min_uf):
            w = j
            min_uf = uf[j]
    
    # print("utilities: ", util)
    # print("unfairness: ", uf)
    # print(w)
    if(w>m-1):
        print(f"n1: {n1}, n2: {n2}, threshold: {threshold}, winner: {w}")
        print(util)
        print(uf)
    return w, uf

def fair_plurality(votes, n1, n2, threshold):
    #minimize unfairness for SW > threshold*maxSW
    # SW computed for top1 utility
    util, uf = util_uf(votes[:n1], votes[n1:n1+n2])
    m = len(util)
    min_uf = np.inf
    w = m+1
    for j,u in enumerate(util):
        if(u < np.max(util)*threshold):
            continue
        if(np.isnan(uf[j])):
            continue
        if(uf[j] < min_uf):
            w = j
            min_uf = uf[j]
    
    # print("utilities: ", util)
    # print("unfairness: ", uf)
    # print(w)
    if(w>m-1):
        print(f"n1: {n1}, n2: {n2}, threshold: {threshold}, winner: {w}")
        print(util)
        print(uf)
    return w, uf

def fairness_efficiency(voting_rule, n1 = 200, n2 = 100, m=4, profiles=1000, threshold = 0.8):
    """
    Computes fairness (compared to fairness with certain threshold) and 
    efficiency (Condorcet efficiency) for a voting rule

    Parameters
    ----------
    voting_rule : any voting function (plurality, copeland, borda)
    n1 : group size of group1
    n2 : group size of group2 
    m : no of alternatives
    profiles : no of profiles to fenerate for each test
    threshold : t
    Returns
    -------
    eff : efficiency
    unfairness_fair : average unfairness for most fair candidate
    unfairness_w : average unfairness for voting rule winner
    """
    eff = []
    unfairness_fair = []
    unfairness_w = []
    for test in range(20):
        # print("test = %d"%test)
        cnt = 0
        fair_ufmean = 0
        w_ufmean = 0
        for t in range(profiles):
            votes = gen_pref_profile(n1+n2, m)
            winner, _ = voting_rule(votes)
            w = singleton_lex_tiebreaking(votes, winner)
            w_fair, uf = fair_borda(votes, n1,n2, threshold)
        
            # print(f"{test}, {t}: n1={n1}, n2={n2}, w_fair={w_fair}, w={w}")
            fair_uf = uf[w_fair]
            w_uf = uf[w]
            if(w == w_fair):
                cnt += 1
            fair_ufmean += fair_uf
            w_ufmean += w_uf
            # print("profile %d"%t, w, w_fair, min_uf)
        
        unfairness_fair.append(fair_ufmean/profiles)
        unfairness_w.append(w_ufmean/profiles)
        eff.append(cnt/profiles)
        print(f"{test}: n1={n1}, n2={n2}, count={cnt}, total={profiles}")
        # print(voting_rule.__name__,"N = %d, m = %d"%(N,m))
        # print("profiles = %d, Condorcet_winner = %d, V_winner = %d"%(profiles, cnt, cnt_v))
        
        # eff.append(cnt_v/cnt)
    return eff, unfairness_fair, unfairness_w

def fairness_efficiency_all(n1 = 100, n2 = 30, m=4, profiles = 100):
    """
    Computes fairness (compared to fairness with certain threshold) and 
    efficiency (Condorcet efficiency) for a familhy of voting rule
    
    Either can be run for traditional voting rules: plurality_winner, Borda_winner, 
            Copeland_winner, maximin_winner, STV_winner
    Or for a family of alpha-fair Borda voting rules for different alpha
    
    Parameters
    ----------
    voting_rule : any voting function (plurality, copeland, borda)
    n1 : group size of group1
    n2 : group size of group2 
    m : no of alternatives
    profiles : no of profiles to fenerate for each test
    threshold : t
    Returns
    -------
    eff : efficiency
    unfairness_fair : average unfairness for most fair candidate
    unfairness_w : average unfairness for voting rule winner
    """
    
    print(f"n1={n1},n2={n2},m={m}")
    sw_w = []
    unfairness_w = []
    sw_fair = []
    unfairness_fair = []
    
    eff = []
    # voting_rules = [plurality_winner, Borda_winner, Copeland_winner, \
    #                 maximin_winner, STV_winner]
    voting_rules = [Borda_winner, Copeland_winner]
    # alpha = np.arange(0.82,0.99,0.02)
    
    utils = []
    
    for test in range(10):
        tic = time()
        # print("test = %d"%test)
        cond_cnt = 0
        
        # ll = len(alpha)
        ll = len(voting_rules)
        # cnt = np.zeros(len(alpha))
        cnt = np.zeros(ll)
        fair_ufmean = 0
        fair_swmean = 0
        w_ufmean = np.zeros(ll)
        w_swmean = np.zeros(ll)
        
        # w_ufmean = np.zeros(len(voting_rules))
        # w_swmean = np.zeros(len(voting_rules))
        
        maxu = 0
        minu = 0
        
        for t in range(profiles):
            # votes = gen_pref_profile(n1+n2, m) # for uniform ballots
            
            ballots1, ballots2 = PL_ballots_gen(n1, n2, m) # for PL ballots
            votes = np.concatenate((ballots1, ballots2))
            
            # ballots1, ballots2 = gaussian_ballots_gen(n1, n2, m) # for Gaussian ballots
            # votes = np.concatenate((ballots1, ballots2))
            
            exist, cond = condorcet_exist(votes)
            if(exist):
                cond_cnt += 1
            
            _, util = Borda_winner(votes)
            maxu += np.max(util)
            minu += np.min(util)
            
            w_fair, uf = fair_borda(votes, n1,n2, 0)
            # print(f'util: {util}')
            # print(f'uf: {uf}')
            
            # for r,rule in enumerate(voting_rules):
            #     winner, _ = rule(votes) # plurality
            #     w = singleton_lex_tiebreaking(votes, winner)
            #     w_ufmean[r] += uf[w]
            #     w_swmean[r] += util[w]
                
            # for r,a in enumerate(alpha):
            for r,rule in enumerate(voting_rules):
                # w, _ = fair_borda(votes, n1,n2, a)
                winners, scores = rule(votes)
                w = singleton_lex_tiebreaking(votes, winners)
                # print(r, w)
                w_ufmean[r] += uf[w]
                w_swmean[r] += util[w]
                
                if(exist):
                    # print(w,cond)
                    if(w in cond):
                        cnt[r] += 1
            
            # print(f"{test}, {t}: n1={n1}, n2={n2}, w_fair={w_fair}, w={w}")
            
            fair_ufmean += uf[w_fair]
            fair_swmean += util[w_fair]
            # print("profile %d"%t, w, w_fair, min_uf)
        
        unfairness_fair.append(fair_ufmean/profiles)
        unfairness_w.append(w_ufmean/profiles)
        
        sw_fair.append(fair_swmean/profiles)
        sw_w.append(w_swmean/profiles)
        
        utils.append([maxu/profiles, minu/profiles])
        
        eff.append(cnt/cond_cnt)
        
        toc = time()
        print(f"time taken for each iteration: {toc-tic}")
    
    return voting_rules, np.array(unfairness_fair), np.array(unfairness_w), np.array(sw_fair), \
        np.array(sw_w), np.array(utils), np.array(eff)
    # return alpha, np.array(unfairness_fair), np.array(unfairness_w), np.array(sw_fair), \
    #     np.array(sw_w), np.array(utils), np.array(eff)
#%%
 
if __name__ == "__main__":
    
    n1 = 100
    
    method = "PL"
    
    for m in [4]:
        for n2 in [40]:
            
            print()
            alpha, UF, UW, SWF, SWW, U, EFF = fairness_efficiency_all(n1, n2, m)
            print("UF",np.mean(UF,axis=0))
            print("UW", np.mean(UW,axis=0))
            print("SWF", np.mean(SWF,axis=0))
            print("SWW", np.mean(SWW,axis=0))
            print("U", np.mean(U,axis=0))
            print("EFF", np.mean(EFF, axis=0))
            
            # x2 = np.mean(UW, axis=0)
            # y2 = np.mean(EFF, axis=0)
            
            # fig, ax = plt.subplots()
            
            # ax.scatter(-1*np.array(x2),y2)
            # for i in range(len(alpha)):
            #     ax.annotate("%.1f-FB"%(alpha[i]), (-x2[i], y2[i]), horizontalalignment='right')
            
            # ax.set_xlabel('Mean Fairness')
            # ax.set_ylabel('Condorcet Efficiency')
            
            # ax.set_title(f"n1={n1}, n2={n2}, m={m}, data={method}")
            
            # # plt.show()
            # plt.savefig(f'imgs/{n1}-{n2}-{m}-{method}-fairness-voting.pdf')
            
            # with open(f"data/{n1}-{n2}-{m}-{method}-fairness-voting.npy", 'wb') as f:
            #     np.save(f, UW)
            #     np.save(f, EFF)
            #     np.save(f, SWW)