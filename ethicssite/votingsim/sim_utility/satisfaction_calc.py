import numpy as np
from time import time
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
    """
    Generate a random preference profile with N agents and m alternatives
    """
    votes = []
    for t in range(N):
        votes.append(gen_random_vote(m))
    return np.array(votes)

#%% functions for calculating winners (multiwinner version)
# TODO: Need to write a multi-round version (have function as parameters)
    
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
    
def Borda_winner(votes):
    n, m = votes.shape
    scores = np.zeros(m)
    for i in range(n):
        for j in range(m):
            scores[votes[i][j]] += m-j-1 
    winner = np.argwhere(scores == np.max(scores)).flatten().tolist()
    
    return winner, scores

def plurality_winner(votes):
    n, m = votes.shape
    scores = np.zeros(m)
    for i in range(n):
        scores[votes[i][0]] += 1
    winner = np.argwhere(scores == np.max(scores)).flatten().tolist()
    
    return winner, scores

def STV_helper(votes, n, m, removed):
    """
    Parameters
    ----------
    votes : preference profile
    n : #votes
    m : #candidates in original election
    removed : already removed candidates
    """
    winner, scores = plurality_winner(votes)
    
    if(np.max(scores) >= n/2):
        return winner, scores
    rest_scores = scores
    rest_scores[removed] = np.inf
    c_last = np.argmin(rest_scores)
    
    removed.append(c_last)
    new_votes = []
    for v in votes:
        newv = np.delete(v, np.where(v==c_last))
        newv = np.append(newv, c_last)
        
        new_votes.append(newv)
    
    return STV_helper(np.array(new_votes), n, m, removed)
    
def STV_winner(votes):
    votes_cpy = votes.copy()
    n, m = votes_cpy.shape
    return STV_helper(votes_cpy, n, m, [])

def maximin_winner(votes):
    """
    Description:
        Calculate maximin winner given a preference profile
    Parameters:
        votes:  preference profile with n voters and m alternatives
    Output:
        winner: maximin winner
        scores: min{D_p(c,c') |c' != c}
    """
    n,m = votes.shape
    Dp_matrix = np.zeros([m,m])
#    scores = np.zeros(m)
    for m1 in range(m):
        for m2 in range(m1+1,m):
            m1prefm2 = 0        #m1prefm2 would hold #voters with m1 \pref m2
            for v in votes:
                if(v.tolist().index(m1) < v.tolist().index(m2)):
                    m1prefm2 += 1
            m2prefm1 = n - m1prefm2
            Dp_matrix[m1][m2] = m1prefm2 - m2prefm1
            Dp_matrix[m2][m1] = m2prefm1 - m1prefm2
    # print(Dp_matrix)        
    scores = np.min(Dp_matrix, axis = 1)
            
    winner = np.argwhere(scores == np.max(scores)).flatten().tolist()
    
    return winner, scores

def kapprov_winner(votes, k):
    """
    Description:
        Return k-approval utility for each candidate
    """
    n, m = votes.shape
    scores = np.zeros(m)
    
    for vote in votes:
        for j in range(k):
            scores[vote[j]] += 1 
            
    winner = np.argwhere(scores == np.max(scores)).flatten().tolist()
    return winner, scores

def two_approv_winner(votes):
    return kapprov_winner(votes, 2)

def veto_winner(votes):
    n, m = votes.shape
    return kapprov_winner(votes, m-1)

#%% tiebreakers
def ranking_count(votes):
    # index for permutation [0,1,...,m-1] is 0
    # index for permutation [m-1,...,1,0] is (m!-1)
    n,m = votes.shape
    
    all_perms = permutation(list(range(m)))
    all_perms = np.array(all_perms)
    ranking_count = np.zeros(len(all_perms))
    
    for vote in votes:
        for p, perm in enumerate(all_perms):
            if((vote == perm).all()):
                ranking_count[p] += 1
    
    return ranking_count

def singleton_winner(vote, winners):
    ranks = [np.argwhere(vote == w).flatten()[0] for w in winners]
    return winners[np.argmin(ranks)]

def lexicographic_tiebreaking(votes, winners):
    return np.min(winners)

def voter1_tiebreaking(votes, winners):
    return singleton_winner(votes[0],winners)

def singleton_lex_tiebreaking(votes, winners):
    rank_cnt = ranking_count(votes)
    rank_srt = np.flip(np.argsort(rank_cnt))
    
    flag = False
    for r in rank_srt:
        rank = rank_cnt[r]
        l = len(np.argwhere(rank_cnt==rank))
        if(l==1):
            flag = True
            break
    
    if(flag):
        n,m = votes.shape
        perms = permutation(list(range(m)))
        return singleton_winner(np.array(perms[r]),winners)
    else:
        return(lexicographic_tiebreaking(votes, winners))
        
def singleton_v1_tiebreaking(votes, winners):
    rank_cnt = ranking_count(votes)
    rank_srt = np.flip(np.argsort(rank_cnt))
    
    flag = False
    for r in rank_srt:
        rank = rank_cnt[r]
        l = len(np.argwhere(rank_cnt==rank))
        if(l==1):
            flag = True
            break
    
    if(flag):
        n,m = votes.shape
        perms = permutation(list(range(m)))
        return singleton_winner(perms[r],winners)
    else:
        return(voter1_tiebreaking(votes, winners))
    
#%%
def Condorcet_efficiency(voting_rule, N=250, m=6, profiles=1000):
    eff = []
    for test in range(50):
        cnt = 0
        cnt_v = 0
        for t in range(profiles):
            votes = gen_pref_profile(N, m)
            exist, winner = condorcet_exist(votes)
            if(exist):
                cnt += 1
                v_winner, _ = voting_rule(votes)
                
                if(winner[0] in v_winner):
                    cnt_v += 1
        print(voting_rule.__name__,"N = %d, m = %d"%(N,m))
        print("profiles = %d, Condorcet_winner = %d, V_winner = %d"%(profiles, cnt, cnt_v))
        
        eff.append(cnt_v/cnt)
    return np.mean(eff)

def Consistency_efficiency(voting_rule, N=250, m=6, profiles=1000):
    for test in range(50):
        #Now we have to store the profiles as well
        cnt = 0
        cnt_v = 0
        votes_all = []
        
        tic = time()
        for t in range(profiles):
            votes = gen_pref_profile(N, m)
            votes_all.append(votes)
        toc = time()
        print("Profiles generated in %lf s"%(toc-tic))
        
        # calculate all winners given some voting rule and tiebreaking scheming
        winner_sets = [[] for i in range(m)]
        tic = time()
        for t in range(profiles):
            winner, _ = voting_rule(votes_all[t])
            w = singleton_lex_tiebreaking(votes_all[t], winner)
            winner_sets[w].append(t)
        toc = time()
        print("Winners computed in %lf s"%(toc-tic))
        
        for w,wset in enumerate(winner_sets):
            len_set = len(wset)
            for i1 in range(len_set):
                for i2 in range(i1+1,len_set):
                    tic = time()
                    joined = np.append(votes_all[wset[i1]],votes_all[wset[i2]],axis = 0)
                    winner, _ = voting_rule(joined)
                    w_new = singleton_lex_tiebreaking(joined, winner)
                    if(w_new == w):
                        cnt_v += 1
                    
                    cnt += 1
                    toc = time()
                    # print("Alternative %d. Comparison %d takes %lf s, cnt_v = %d"%(w, cnt, toc-tic, cnt_v))
        print("profiles = %d, Comparisons = %d, Consistent = %d"%(profiles, cnt, cnt_v))
    return 0

#%%

def main():
    print("Consistency efficiency results for m = 6")
    # print("Copeland")
    # Consistency_efficiency(Copeland_winner)
    # print("STV")
    # Consistency_efficiency(STV_winner, profiles = 100)
    print("maximin")
    Consistency_efficiency(maximin_winner, profiles = 100, N=1000)

    # print("Condorcet efficiency results for m = 8")
    # print("STV")
    # Condorcet_efficiency(STV_winner)
    # print("Borda")
    # Condorcet_efficiency(Borda_winner)
    
if __name__ == "__main__":
    main()
