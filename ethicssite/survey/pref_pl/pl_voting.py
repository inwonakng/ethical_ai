import numpy as np

#%%

# each voting rule returns w, rank
# w is the winner (not necessarily unique), rank is the ranking

def PL_plurality(gamma):
    # the highest gamma is the winner
    w = np.argmax(gamma)
    rank = np.argsort(-gamma)
    return w, rank

def PL_WMG(gamma):
    # helper function to calculate the WMG for a single PL
    # this is the only function we need to change if we're dealing with mixtures of PL
    #       or other RUMs/mixtures of RUMs
    # this is not the actual definition of WMG, since we use wmg[i][j] = gamma_ij instead of gamma_ij-gamma_ji
    # but this is easier to deal with for Borda
    m = len(gamma)
    wmg = np.zeros((m,m))
    
    for i in range(m):
        for j in range(m):
            wmg[i][j] = gamma[i]/(gamma[i]+gamma[j])
    return wmg

def PL_Borda(gamma):
    m = len(gamma)
    wmg = PL_WMG(gamma)
    
    Borda_scores = np.zeros(m)
    
    for i in range(m):
        for j in range(m):
            if i == j:
                continue
            Borda_scores[i] += wmg[i][j]
            
    w = np.argmax(Borda_scores)
    rank = np.argsort(-Borda_scores)
    return w, rank

def PL_Copeland(gamma):
    m = len(gamma)
    wmg = PL_WMG(gamma)
    
    Copeland_scores = np.zeros(m)
    
    for i in range(m):
        for j in range(m):
            if i == j:
                continue
            if(wmg[i][j] > 0.5):
                Copeland_scores[i] += 1
            elif(wmg[i][j] == 0.5):
                Copeland_scores[i] += 0.5
        
    w = np.argmax(Copeland_scores)
    rank = np.argsort(-Copeland_scores)
    return w, rank

def PL_maximin(gamma):
    m = len(gamma)
    wmg = PL_WMG(gamma)
    
    maximin_scores = np.zeros(m)
    
    for i in range(m):
        mask = [x for x in range(m) if x != i]
        maximin_scores[i] = np.min(wmg[i][mask])
    
    w = np.argmax(maximin_scores)
    rank = np.argsort(-maximin_scores)
    return w, rank