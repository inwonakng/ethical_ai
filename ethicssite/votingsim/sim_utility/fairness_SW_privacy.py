import pandas as pd
import numpy as np
# from matplotlib import pyplot as plt
from time import time
from .fairness_SW_tradeoff import *

#%%
def Copeland_winner(votes):
    """
    Description:
        Calculate Copeland winner given a preference profile
    Parameters:
        votes:  preference profile with n voters and m alternatives
    Output:
        winner: Copeland winner
        scores: pairwise-wins for each alternative
    """
    n,m = votes.shape
    scores = np.zeros(m)
    for m1 in range(m):
        for m2 in range(m1+1,m):
            m1prefm2 = 0        #m1prefm2 would hold #voters with m1 \pref m2
            for v in votes:
                if(v.tolist().index(m1) < v.tolist().index(m2)):
                    m1prefm2 += 1
            m2prefm1 = n - m1prefm2
            if(m1prefm2 == m2prefm1):
                scores[m1] += 0.5
                scores[m2] += 0.5
            elif(m1prefm2 > m2prefm1):
                scores[m1] += 1
            else:
                scores[m2] += 1
    winner = np.argwhere(scores == np.max(scores)).flatten().tolist()
    
    return winner, scores

def condorcet_exist(votes):
    """
    Parameters
    ----------
    votes : preference profile
    
    Returns
    -------
    (int) : flag, whether Condorcet winner exists
    winner : Copeland winner(s)
    """
    n, m = votes.shape
    winner, scores = Copeland_winner(votes)
    if(len(winner) > 1):
        return 0, winner
    if(scores[winner[0]] == m-1):
        return 1, winner
    else:
        return 0, winner

#%% functions for generating preference profiles
def permutation(lst):
    """
    function to create permutations of a given list
        supporting function for ranking_count
    reference: https://www.geeksforgeeks.org/generate-all-the-permutation-of-a-list-in-python/
    """
    if(len(lst) == 0):
        return []
    if(len(lst) == 1):
        return [lst]
    l = []   
    for i in range(len(lst)): 
       m = lst[i] 
       remLst = lst[:i] + lst[i+1:] 
       for p in permutation(remLst): 
           l.append([m] + p) 
    return l

def gen_random_vote(m):
    # m is the number of alternatives
    # this functions generates an uniformly random profile
    # i.e 1/m! probability of each profile
    
    alts = list(range(m))
    perms = permutation(alts)
    
    t = np.random.randint(0,len(perms))
    
    return perms[t]

def gen_pref_profile(N,m):
    votes = []
    for t in range(N):
        votes.append(gen_random_vote(m))
    return np.array(votes)

#%%
def util_uf(votes1, votes2):
    util1 = plurality_utility(votes1)
    util2 = plurality_utility(votes2)
    util = plurality_utility(np.concatenate((votes1,votes2)))
    
    m = len(util)
    uf = np.zeros(m)
    for j in range(m):
        if(util[j]==0):
            uf[j] = np.nan
        else:
            uf[j] = np.abs(util1[j] - util2[j]) / util[j]
    return util, np.array(uf)

def fair_plurality(votes, n1, n2, threshold):
    #minimize unfairness for SW > threshold*maxSW
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

#%%

def local_noise_plurality(ballot, p):
    """
    Description:
        Adds noise to a ballot for plurality vote, only the top candidate is needed, so 
            only changing ballot[0]
        With probability p, ballot is unchanged,
        with probability (1-p), the other m candidates are drawn from uniformly
    """
    x = np.random.uniform()
    if(x<p):
        return ballot
    
    m = len(ballot)
    # print(ballot.shape)
    newballot = gen_random_vote(m)
    return newballot

def diff_private_rankings(ballots1, ballots2, eps):
    """
    Description:
        Calculate alternate ballots with coin-flipping algorithm
        This depends on how much data is available, so dependent on utility function
            Examples:
            For plurality, only m possibilities
            For Borda, m! possibilities (too-large)
            For k-Borda, mPk
            For k-approval, mCk
    Parameters:
        ballots1:   ballots for group1
        ballots2:   ballots for group2
        eps:        privacy parameter
    """
    m = len(ballots1[0])
    
    if(eps<100):
        p = (np.exp(eps)-1)/(m+np.exp(eps)-1) # probability that original ballot remains
    else:
        p = 1
    
    # print(f"p={p}")
    noisy_b1 = np.zeros(ballots1.shape)
    for i,ballot in enumerate(ballots1):
        noisy_b1[i] = local_noise_plurality(ballot, p)
        
    noisy_b2 = np.zeros(ballots2.shape)
    for i,ballot in enumerate(ballots2):
        noisy_b2[i] = local_noise_plurality(ballot, p)
    
    return noisy_b1, noisy_b2

#%%
# g1, g2, candidates = create_voters_candidates(n1,n2,m)
# plot_all(g1, g2,candidates) #plotting for 2d space only
# ballots1, ballots2 = random_pref_profile(g1, g2, candidates) 



#%% Fairness-privacy-SW trade-off
# We can try plurality, k-approval, k-Borda

n1 = 100
m = 4

eps_all = [0,1,2,3,5]
primary = plurality_utility

vals = []


for n2 in range(20,101,20):
    df = pd.DataFrame()
    trials = 10
    
    for tt in range(trials):    
        ballots1 = gen_pref_profile(n1, m)
        ballots2 = gen_pref_profile(n2, m)
        
        exist, C = condorcet_exist(np.concatenate((ballots1, ballots2)))
        
        tic = time()
        w_uf = np.zeros(len(eps_all))
        w_util = np.zeros(len(eps_all))
        
        for thresh in np.arange(0.5,1.01,0.1):    
                  
            # g1, g2, candidates = create_voters_candidates(n1,n2,m)
            # # plot_all(g1, g2,candidates) #plotting for 2d space only
            # ballots1, ballots2 = random_pref_profile(g1, g2, candidates) 
        
            util, _ = util_uf(ballots1, ballots2)
            w, uf = fair_plurality(np.concatenate((ballots1, ballots2)), n1, n2, thresh)
            # if(thresh>0.95):
            #     if(not(util[w] == np.max(util))):
            #        print("FAIL!!")
            #        break
            
            # w_uf[0] = uf[w]
            # w_util[0] = util[w]
            df = df.append(pd.Series([thresh, 0, uf[w], util[w], exist, 1 if w in C else 0]), ignore_index=True)
            for eps in eps_all[1:]:
                nb1, nb2 = diff_private_rankings(ballots1, ballots2, eps)
                nw, _ = fair_plurality(np.concatenate((nb1, nb2)), n1, n2, thresh)
                df = df.append(pd.Series([thresh, eps, uf[nw], util[nw], exist, 1 if nw in C else 0]), ignore_index=True)
                # w_uf[int(eps)] += uf[nw]
                # w_util[int(eps)] += util[nw]
        toc = time()
        
        if(tt%1000 == 0):
            print(f"{n1}-{n2}-trial = {tt}, iter time = {toc-tic}")
            df.to_csv(f'fairness-privacy-sw-{n1}-{n2}-{m}.csv',index=False)
        # print(toc - tic)    
        # vals = np.concatenate(([thresh],w_uf,w_util))
        # df = df.append(pd.Series(vals), ignore_index=True)
    df.rename(columns={0: "threshold", 1: "eps", 2:"uf", 3:"sw", 4: "exist", 5:"Condorcet"}, inplace = True)       
    df.to_csv(f'fairness-privacy-sw-{n1}-{n2}-{m}.csv',index=False)

#%%

# rng = np.arange(0,1.01,0.1)
# uf_mins = np.zeros(len(rng))
# n_uf_mins = np.zeros([3,len(rng)])
# n_sw_mins = np.ones([3,len(rng)])*np.inf

# n_utils = np.zeros([len(eps_all), m])
# n_ufs = np.zeros([len(eps_all), m])

# trials = 1

# uf_sums = []

# for t in range(trials):
  
    
#     utilg1 = primary(ballots1)
#     utilg2 = primary(ballots2)
#     util = primary(np.concatenate((ballots1,ballots2)))
    
#     plt.figure()
#     plt.plot(range(m),utilg1, range(m), utilg2)
    
#     uf = calculate_unfairness(utilg1, utilg2, util)
#     opt_uf = np.nanmin(uf)
# #    print(util)
# #    print(uf)    
#     for cnt,r in enumerate(rng):
#         sw_lim = np.max(util) * r
# #        print("SW_lim",sw_lim)
#         uf_comp = np.inf
#         for i,sw in enumerate(util):
#             if(sw >= sw_lim and uf[i] < uf_comp):
#                 uf_comp = uf[i]
# #                print("Hey", cnt, i)
# #                print("SW",sw)
#         uf_mins[cnt] = uf_comp
# #        if(uf_comp/opt_uf > uf_mins[cnt]):
# #            uf_mins[cnt] = uf_comp/opt_uf
    
#     uf_sums.append(uf_mins)
    
#     for e,eps in enumerate(eps_all):
        
#         sw_sum = np.zeros(len(rng))
#         uf_sum = np.zeros(len(rng))
        
#         noise_trials = 100
#         for nt in range(noise_trials):
#             noisy_b1, noisy_b2 = diff_private_rankings(ballots1, ballots2, eps)   
        
#             n_utilg1 = primary(noisy_b1)
#             n_utilg2 = primary(noisy_b2)
#             n_util = primary(np.concatenate((noisy_b1,noisy_b2)))
            
#             n_uf = calculate_unfairness(n_utilg1, n_utilg2, n_util)
            
# #            print(n_util)
# #            print(n_uf)
#             #calculating expected SW, UF
#             for j in range(m):
#                 n_utils[e][j] += n_util[j]
#                 n_ufs[e][j] += n_uf[j]
            
#             # for the tradeoff plot
#             for cnt,r in enumerate(rng):
#                 sw_lim = np.max(n_util) * r
# #                print("SW_lim",sw_lim)
#                 uf_comp = np.inf
#                 for i,sw in enumerate(n_util):
                    
#                     if(sw >= sw_lim and n_uf[i] < uf_comp):
#                         uf_comp = n_uf[i]
#                         noisy_opt = i
# #                        print("Hey", cnt, i)
# #                        print("SW",sw)
                        
# #                print(eps, nt, cnt, i)
#                 sw_sum[cnt] += util[noisy_opt]
#                 uf_sum[cnt] += uf[noisy_opt]
        
#         uf_sum /= noise_trials
#         sw_sum /= noise_trials
        
#         uf_sums.append(uf_sum)
        
#         plt.figure()
#         plt.plot(rng, uf_mins, rng, uf_sum)
#         plt.plot(rng, uf_sum, 'o')
        
#         n_utils /= noise_trials
#         n_ufs /= noise_trials
#         plt.figure()

#         s1mask = np.isfinite(uf)
#         s2mask = np.isfinite(n_ufs[e])
#         ax1 = plt.subplot(2,1,1)
#         plt.plot(range(m),util, range(m),n_utils[e])
#         ax1.set_xlabel('candidate')
#         ax1.set_ylabel('SW')
# #        ax1.set_title('original')
        
#         p = (np.exp(eps)-1)/(m+np.exp(eps)-1)
#         ax2 = plt.subplot(2,1,2)
#         plt.plot(np.arange(m)[s1mask],uf[s1mask], np.arange(m)[s2mask],n_ufs[e][s2mask])
#         ax2.set_xlabel('candidate')
#         ax2.set_ylabel('UF')
        
# #        ax2.set_title('noisy - p = %.2f'%(p))
# #        sw_sum = sw_sum / noise_trials
# #        uf_sum = uf_sum / noise_trials

# #%%
# plt.figure()

# plt.subplot(2,1,1)
# plt.plot(range(m),util, range(m),n_util)

# plt.subplot(2,1,2)
# s1mask = np.isfinite(uf)
# s2mask = np.isfinite(n_uf)
# plt.plot(np.arange(m)[s1mask],uf[s1mask], np.arange(m)[s2mask],n_uf[s2mask])

# plt.figure()
# #plt.plot(rng,-uf_mins, n_sw_mins[0],-n_uf_mins[0], n_sw_mins[1], -n_uf_mins[1],\
# #         n_sw_mins[2], -n_uf_mins[2])
# plt.plot(rng,-uf_mins, rng,-n_uf_mins[0], rng, -n_uf_mins[1],\
#         rng, -n_uf_mins[2])
        
#%%