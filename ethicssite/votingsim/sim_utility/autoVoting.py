import numpy as np
import pandas as pd


def random_pref_profile(n, m):
    """
    Description:
        Generate a random preference profile
    Parameters:
        n:  number of ballots to generate
        m:  number of alternatives
    """
    votes = []
    for i in range(n):
        # Each ballot is just a random permutation of [m]
        votes.append(np.random.permutation(m))
    return np.array(votes)

def Borda_winner(votes):
    """
    Description:
        Calculate Borda winner given a preference profile
    Parameters:
        votes:  preference profile with n voters and m alternatives
    Output:
        winner: Borda winner
        scores: Borda score for each alternative
    """
    n, m = votes.shape
    scores = np.zeros(m)
    for i in range(n):
        for j in range(m):
            scores[votes[i][j]] += m-j-1 
    winner = np.argwhere(scores == np.max(scores)).flatten().tolist()
    
    return winner, scores

def plurality_winner(votes):
    """
    Description:
        Calculate plurality winner given a preference profile
    Parameters:
        votes:  preference profile with n voters and m alternatives
    Output:
        winner: plurality winner
        scores: plurality score for each alternative
    """
    n, m = votes.shape
    scores = np.zeros(m)
    for i in range(n):
        scores[votes[i][0]] += 1
    winner = np.argwhere(scores == np.max(scores)).flatten().tolist()
    
    return winner, scores

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
            
    scores = np.min(Dp_matrix, axis = 1)
            
    winner = np.argwhere(scores == np.max(scores)).flatten().tolist()
    
    return winner, scores



def weighted_majority_graph(votes):
    """
    Description:
        Calculate weighted majority graph
    Parameters:
        votes:  preference profile with n voters and m alternatives
    Defn:
        WMG = directed graph (V,E)
        V = list of alternatives
        E = {e = D_p(a,b) | D_p(a,b)>0}
    Output: returned as m*m adjacency matrix
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
    
    Dp_matrix[Dp_matrix < 0] = 0
    
    return Dp_matrix

def position_vector(votes):
    """
    Description:
        Calculate how many times alternate i was ranked j-th
            for all i, j
    Parameters:
        votes:  preference profile with n voters and m alternatives
    Output: 
        m*m matrix
        positional_score[i][j] = #times alternate i was ranked j-th
            index 0 means ranked 1st
            index m-1 means ranked last
    """ 
    n,m = votes.shape
    positional_score = np.zeros([m,m])
    for v in votes:
        for j in range(m):
            positional_score[v[j]][j] += 1
    
    return positional_score

def posvec_to_sw(posvec):
    """
    Parameters
    ----------
    posvec : m*m np array
    
    Returns
    -------
    m np array, sw for each alternative
    """
    m = len(posvec)
    sw = np.zeros(m)
    for i in range(m):
        for j in range(m):
            sw[i] += (m-j-1)*posvec[i][j]
    return sw

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

def ranking_count(votes):
    """
    Description:
        Calculate how many times each full ranking (total order) has occured
            in the full pref profile
    Parameters:
        votes:  preference profile with n voters and m alternatives
    Defn:
        index for permutation [0,1,...,m-1] is 0
        index for permutation [m-1,...,1,0] is (m!-1)
    Output:
        for each ranking p with index i, ranking_count[i] will hold #voters
            whose vote is p
    """
    n,m = votes.shape
    
    all_perms = permutation(list(range(m)))
    all_perms = np.array(all_perms)
    ranking_count = np.zeros(len(all_perms))
    
    for vote in votes:
        for p, perm in enumerate(all_perms):
            if((vote == perm).all()):
                ranking_count[p] += 1
    
    return ranking_count

class profile_winner_pair:
    """
    Class will hold a preference profile and winner pair
    Preference profile will not strictly be stored for all data, rather be 
        represented by positional vector and weighted majority graph
    So a total of 2m*m features
    We allow for storage for preference profile for the original true data 
        because we want to sample for monotonicity
    Winner for this class will be a single candidate and not a set
    """
    def __init__(self, position_vector, WMG, W):
        self.position_vector = position_vector
        self.WMG = WMG
        self.winner = W
        self.alternate_size = len(WMG[0])
    def set_pref_profile(self, pref_profile):
        self.pref_profile = pref_profile
        
class f_profile_winner_pair:
    """
    To consider for fair profiles, allow multiple pos_vector, WMG
    """
    def __init__(self, n1, n2, position_vectors, WMGs, W):
        self.n1 = n1
        self.n2 = n2
        self.position_vectors = position_vectors
        self.WMGs = WMGs
        self.winner = W
        self.alternate_size = len(WMGs[0][0])
    def set_pref_profile(self, pref_profiles):
        self.pref_profiles = pref_profiles
        
def neutral_sample_gen(prof_win_pair):
    """
    Description:
        Generate a new sample preference-winner pair using the neutrality axiom
        Permuting the voters also permutes the winner, majority graph etc accordingly
    """
    m = prof_win_pair.alternate_size
    orig_a = np.arange(m)
    while(1):
        new_a = np.random.permutation(m)
        if(not((new_a == orig_a).all())):
            break
    wmg = np.zeros([m,m])
    pos_vec = np.zeros([m,m])
    for i in range(m):
        for j in range(m):
            wmg[new_a[i]][new_a[j]] = prof_win_pair.WMG[i][j]
        pos_vec[new_a[i]] = prof_win_pair.position_vector[i]
    
    w = new_a[prof_win_pair.winner]
    new_prof_win = profile_winner_pair(pos_vec, wmg, w)
    return new_prof_win

def neutral_profile_gen(pwp):
    """
    Description:
        Generate a complete (new) pref profile (using neutrality axiom)
    """    
    
    """
    TODO: might do well to write a permute function for composition
    """
    m = pwp.alternate_size
    orig_a = np.arange(m)
    while(1):
        new_a = np.random.permutation(m)
        if(not((new_a == orig_a).all())):
            break
    P = pwp.pref_profile
    
    new_P = []
    for vote in P:
        v = []
        for j in vote:
            v.append(new_a[j])
        new_P.append(v)
    new_P = np.array(new_P)
    w = new_a[pwp.winner]
    new_prof_win = profile_winner_pair(position_vector(new_P), \
                        weighted_majority_graph(new_P), w)
    new_prof_win.set_pref_profile(new_P)
    return new_prof_win
    
def consistent_sample_gen(pwp1, pwp2):
    """
    Description:
        Generate a new sample preference-winner pair using the consistency axiom
        if r(P1) = c, r(P2) = c, then r(P1 union P2) = c
    """
    m = pwp1.alternate_size
    
    wmg = np.zeros([m,m])
    pos_vec = np.zeros([m,m])
    
    for i in range(m):
        for j in range(m):
            wmg_ij = pwp1.WMG[i][j] + pwp2.WMG[i][j] - pwp1.WMG[j][i] - pwp2.WMG[j][i]
            wmg[i][j] = np.max([0, wmg_ij])
        pos_vec[i] = pwp1.position_vector[i] + pwp2.position_vector[i]
    
    w = pwp1.winner
    new_prof_win = profile_winner_pair(pos_vec, wmg, w)
    return new_prof_win

def consistent_profile_gen(pwp1, pwp2):
    """
    Description:
        Generate a complete (new) pref profile (using consitency axiom)
    """    
    P1 = pwp1.pref_profile
    P2 = pwp2.pref_profile
    
    P = np.concatenate((P1, P2))
    w = pwp1.winner
    pos_vec = position_vector(P)
    wmg = weighted_majority_graph(P)
    new_prof_win = profile_winner_pair(pos_vec, wmg, w)
    new_prof_win.set_pref_profile(P)
    return new_prof_win

def monotonic_sample_gen(pwp):
    """
    Description:
        Generate a new sample preference-winner pair using the monotonicity axiom
        pushing a winner forward in all rankings cannot make them lose
    """
    ballots = pwp.pref_profile
    w = pwp.winner
    
    for i,v in enumerate(ballots):
        w_idx = v.tolist().index(w)
        if(w_idx > 0):
            # if winner is not 1st choice in this vote
            #   swap winner with someone higher
            new_idx = np.random.randint(w_idx+1)
            temp = ballots[i][new_idx]
            ballots[i][new_idx] = ballots[i][w_idx]
            ballots[i][w_idx] = temp
    new_prof_win = profile_winner_pair(position_vector(ballots), \
                        weighted_majority_graph(ballots), w)
    new_prof_win.set_pref_profile(ballots)
    return new_prof_win

def upscale_sample_gen(pwp):
    """
    Description:
        Just update everything by multiplying with a scalar factor.
        Basically a glorified consistent case generator"
    """
    s = np.random.randint(1,4)
    new_pwp = profile_winner_pair(s * pwp.position_vector, \
                        s * pwp.WMG, pwp.winner)
    return new_pwp

def main():
#    profile_list = []
    N = 10
    m = 3
    '''testing random true dataset generation'''
#    for t in range(100):
#        ballots = random_pref_profile(N,m)
#        wmg = weighted_majority_graph(ballots)
#        pos_vec = position_vector(ballots)
#        W = Borda_winner(ballots)[0]
#        prof_win_pair = profile_winner_pair(pos_vec, wmg, W)
#        prof_win_pair.set_pref_profile(ballots)
#        profile_list.append(prof_win_pair)
    
    ballots = random_pref_profile(N,m)
    wmg = weighted_majority_graph(ballots)
    pos_vec = position_vector(ballots)
    W = Borda_winner(ballots)[0]
    print(ballots)
    print(wmg)
    print(pos_vec)
    print(W)
    
    prof_win_pair = profile_winner_pair(pos_vec, wmg, W[0])
    prof_win_pair.set_pref_profile(ballots)
    
    '''testing monotonic sampler'''
    new_pw = monotonic_sample_gen(prof_win_pair)
    
    print(new_pw.WMG)
    print(new_pw.position_vector)
    print(new_pw.winner)
    
    '''testing consistent sampler'''
    new2 = consistent_sample_gen(prof_win_pair, new_pw)
    print(new2.WMG)
    print(new2.position_vector)
    print(new2.winner)
    
    '''testing upscale sampler'''
    new3 = upscale_sample_gen(prof_win_pair)
    print(new3.WMG)
    print(new3.position_vector)
    print(new3.winner)
    
if __name__ == "__main__":
    # main()
    N = 10
    m = 4
    ballots = random_pref_profile(N,m)
    wmg = weighted_majority_graph(ballots)
    pos_vec = position_vector(ballots)
        
