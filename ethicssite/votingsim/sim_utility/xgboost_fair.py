import xgboost as xgb

import pickle
from time import time

import pandas as pd
import numpy as np
np.set_printoptions(precision=4)
from sklearn.model_selection import KFold, train_test_split, GridSearchCV, ShuffleSplit
from sklearn.metrics import confusion_matrix, accuracy_score
#from sklearn.datasets import load_iris, load_digits, load_boston
#def create_voters_candidates(n1, n2, m, d=2):
#def random_pref_profile(g1,g2,candidates):

from .fairness_SW_tradeoff_2 import create_voters_candidates, random_pref_profile, PL_ballots_gen
from .satisfaction_calc import gen_pref_profile, Copeland_winner, \
    singleton_lex_tiebreaking, permutation
from .autoVoting import weighted_majority_graph, position_vector, posvec_to_sw
from .fairness_new_tradeoffs import util_uf, fair_borda


def convert_votes_to_features(votes1, votes2, n1, n2):
    WMG1 = weighted_majority_graph(votes1)
    posvec1 = position_vector(votes1)
    WMG1 /= n1
    posvec1 /= n1
    
    WMG2 = weighted_majority_graph(votes2)
    posvec2 = position_vector(votes2)
    WMG2 /= n2
    posvec2 /= n2
    
    return WMG1, posvec1, WMG2, posvec2

def permute_rows(feats, perm, m):
    y = feats.copy()
    y[perm] = y[list(range(m))]
    return y

def permute_rows_cols(feats, perm, m):
    y = feats.copy()
    # y[list(range(m))] = y[perm]
    # y[:,list(range(m))] = y[:,perm]
    y[perm] = y[list(range(m))]
    y[:,perm] = y[:,list(range(m))]
    return y

def permute_features(WMG1, posvec1, WMG2, posvec2, perm):
    w1 = WMG1.copy()
    pv1 = posvec1.copy()
    w2 = WMG2.copy()
    pv2 = posvec2.copy()
    m = len(perm)
    w1 = permute_rows_cols(w1, perm, m)
    w2 = permute_rows_cols(w2, perm, m)
    pv1 = permute_rows(pv1, perm, m)
    pv2 = permute_rows(pv2, perm, m)
    
    return w1, pv1, w2, pv2

#%% generate and save base data

# for t in range(20):
    
def gen_dataset(n1, n2, m):
    """
    Generate base dataset with random preference profiles
    For testing purpose, we stick to group sizes n1=200, n2=60 and m=4 alternatives
    
    We generate fixed number of profiles for each experiment
    
    Returns
    -------
    df : TYPE pandas dataframe
        DESCRIPTION: Contains the following information about each preference profile
            WMG1 - weighted majority graph for group 1
            posvec1 - position score matrix for group 1
            WMG2 - weighted majority graph for group 2
            posvec2 - position score matrix for group 2
            n1, n2 - group sizes
            - The data up to this shall be used as features for learning
            
            Condorcet winner - Copeland winner, boolean to indicate if Condorcet winner exists
            max fair winner
            
            gen - data generation indicator: Possible to randomly choose data generation method,
                    but for consistency's sake we always generate data from uniform distribtuion
                    So, this is always 1 and can be ignored
    """

    profiles = 100
    # we will generate 4! permutation of each profile
    # so essentially will have 25000*24 = 0.6M data points
    
    perms = permutation(list(range(m)))
    # voting rule: maximin_winner
    # tiebreaking rule: singleton_lex_tiebreaking
    
    X = []
    W1 = []
    W2 = []
    Wmix = []
    
    cond_exists = []
    
    mix_cnt = 0
    
    df = pd.DataFrame()
    # df_uf = pd.DataFrame()
    
    tic0 = time()
    
    fair_ufmean = np.zeros(2)
    w_ufmean = np.zeros(2)
    
    cnt_special = 0
    uf_special = 0
    
    cnt_special2 = 0
    uf_special2 = 0
    
    cnt_special3 = 0
    uf_special3 = 0
    
    beta = 0.7
    
    for t in range(profiles):
        # tic = time()
        data_random = np.random.choice(2,p=[1-beta,beta]) # beta is the sampling parameter
        # mix_cnt += data_random
        # gen = np.random.choice(2)
        gen = 0
        # sample n2 from [10,20,...,200]
        # n2_all = np.array(range(1,21))*10
        # n2 = np.random.choice(n2_all)    
        
        # tic = time()
        if(gen): # generate data unifomrly
            votes1 = gen_pref_profile(n1, m)
            votes2 = gen_pref_profile(n2, m)    
        else: # generate data where groups are clustered
            g1, g2, candidates = create_voters_candidates(n1, n2, m)
            # votes1, votes2 = random_pref_profile(g1, g2, candidates) 
            votes1, votes2 = PL_ballots_gen(n1, n2, m) # for PL ballots
        # toc = time()
        # print(f"Time to generate: {toc-tic} s")
        
        WMG1, posvec1, WMG2, posvec2 = convert_votes_to_features(votes1, votes2, n1, n2)
        x = np.concatenate((WMG1.flatten(), posvec1.flatten(), WMG2.flatten(), \
                            posvec2.flatten()))
        
        x = np.append(x, [n1, n2]) # x is our feature vector
        
        votes = np.concatenate((votes1,votes2))
        winners, scores = Copeland_winner(votes)
        
        exist = 0
        if(len(winners) == 1):
            if(scores[winners[0]] == m-1):
                exist = 1
        
        w = singleton_lex_tiebreaking(votes, winners)   # in case there are ties, 
                                                        #we keep a consistent tiebreaking method
        
        wfair, _ = fair_borda(votes, n1, n2, 0)
        util, uf = util_uf(votes1, votes2)
        
        fair_ufmean[gen] += uf[wfair]
        w_ufmean[gen] += uf[w]
        
        X.append(x)
        W1.append(w)
        W2.append(wfair)
        
        # beta-sampling algorithm described in Algorithm 2 in the appendix
        if(exist):
            if(w==wfair):
                Wmix.append(w)
                mix_cnt += 1
                if(gen):
                    cnt_special += 1
                    uf_special += uf[w]
            else:
                if(data_random):
                    Wmix.append(w)
                    mix_cnt += 1
                else:
                    Wmix.append(wfair)
                
                if(gen):
                    cnt_special2 += 1
                    uf_special2 += beta*uf[w]+(1-beta)*uf[wfair]
        else:
            Wmix.append(wfair)
            if(gen):
                cnt_special3 += 1
                uf_special3 += uf[wfair]
        df = df.append(pd.Series(np.concatenate((x,[w,wfair,gen,exist],uf))),ignore_index=True)
    
    # df.to_csv('xgboostFairInput.csv',index=False)
    toc0 = time()
    print(f"Time to gen data: {toc0-tic0}")
    
    X = np.array(X)
    W1 = np.array(W1)
    W2 = np.array (W2)
    Wmix = np.array(Wmix)
    
    print(beta)
    
    print(mix_cnt, profiles)
    print(fair_ufmean/(profiles/2))
    print(w_ufmean/(profiles/2))
    
    # print(cnt_special, uf_special)
    # print(cnt_special2, uf_special2)
    # print(cnt_special3, uf_special3)
    
    # print(f"Condorcet: {(cnt_special+beta*cnt_special2)/(cnt_special+cnt_special2)}, unfairness: {(uf_special+uf_special2+uf_special3)/(cnt_special+cnt_special2+cnt_special3)}")
    
    return df

#%% read data from written file and generate permutations
# df = pd.read_csv('xgboostFairInput.csv')

def learn_voting_rule(df, n1, n2, m):
    """
    We repeat the beta-sampling part from the data generation function. Since we saved
    both fair winner and Condorcet info for each preference profile, it is possible 
    for us to do so
    
    First, we compute all m! permutations for all the data generated in the data generation
    function. Then we sample data using the beta_sampling method

    """
    # range of beta for which we learn beta-ML voting rule
    beta_all = np.arange(0,1.01,0.1)
    xgboost_all = []
    print("\tLearning has started")
    
    uf_all = []
    eff_all = []
    sw_all = []
    for beta in beta_all:
        print(f"\t {beta},{n1},{n2},{m}")        
        perms = permutation(list(range(m)))
        
        X = []
        W1 = []
        W2 = []
        Wmix = []
        
        random_idx = []
        
        tic = time()
        
        for row in df.values:
            # feature length = 74 = m**2 + m**2 + m**2 + m**2 + 2 + 4 + 4
            #x(64), n1, n2, [w,wfair,gen,exist],uf
            # beta = 0.8
            data_random = np.random.choice(2,p=[1-beta,beta])
            
            WMG1 = np.reshape(row[:m*m],(m,m))
            posvec1 = np.reshape(row[m*m: 2*m*m],(m,m))
            WMG2 = np.reshape(row[2*m*m: 3*m*m],(m,m))
            posvec2 = np.reshape(row[3*m*m: 4*m*m],(m,m))
            n1 = row[4*m*m] # 64
            n2 = row[4*m*m+1] # 65
            w = int(row[4*m*m+2]) # 66
            wfair = int(row[4*m*m+3]) # 67
            
            gen = int(row[4*m*m+4]) # 68
            exist = int(row[4*m*m+5]) # 69
            
            x = np.concatenate((WMG1.flatten(), posvec1.flatten(), WMG2.flatten(), \
                                posvec2.flatten()))
            x = np.append(x, [n1, n2])
            
            # X.append(x)
            # W1.append(w)
            # W2.append(wfair)
            
            for pi in perms:
                wmg1,pv1,wmg2,pv2 = permute_features(WMG1, posvec1, WMG2, posvec2, pi)       
                x = np.concatenate((wmg1.flatten(), pv1.flatten(), wmg2.flatten(), \
                                    pv2.flatten()))
                x = np.append(x, [n1, n2])
                
                X.append(x)
                W1.append(pi[w])
                W2.append(pi[wfair])
                if(exist):
                    if(w==wfair):
                        Wmix.append(pi[w])
                    else:
                        if(data_random):
                            Wmix.append(pi[w])
                        else:
                            Wmix.append(pi[wfair])
                else:
                    Wmix.append(pi[wfair])
                    
        toc = time()
        print(f'{len(df)} {toc-tic}')
        
        X = np.array(X)
        W1 = np.array(W1)
        W2 = np.array (W2)
        Wmix = np.array(Wmix)
        print(len(X), len(Wmix))
        
            
        #% learning mixedRule
        """
        Applying Xgboost
        ----------------
        For illustratory purposes, we skip the hyperparameter tuning in this function
        In reality, we had done hyperparameter tuning using gridsearch over the following
        grid for each beta-sampled dataset
        
        {"max_depth"        : [ 2, 4, 6, 8],
         "min_child_weight" : [ 1, 3, 5, 7 ],
         "gamma"            : [ 0.0, 0.1, 0.2 , 0.3, 0.4 ]}
        """
        
        rng = np.random.RandomState(31337)
        
        ss = ShuffleSplit(n_splits=1, test_size=0.1, random_state = rng)
        ss.get_n_splits(X, Wmix)
        train_index, test_index = next(ss.split(X, Wmix))
        
        clf3 = xgb.XGBClassifier()
        xgb_model3 = clf3.fit(X[train_index], Wmix[train_index])
        xgboost_all.append(xgb_model3)
        
        predictions3 = xgb_model3.predict(X[test_index])
        actuals = Wmix[test_index]
        print(confusion_matrix(actuals, predictions3))
        print(accuracy_score(actuals, predictions3))
        
            
        #% Compute condorcet_efficiency and unfairness for 
        factm = len(perms)
        
        """
        Test Set Results
        ----------------
        For the learned model, more than the accuracy, the average unfairness and
            efficiency of the learnt rule is of more importance to us.
        So, for the test set, we apply the learned voting rule and compute 
            expected unfairness and Condorcet efficiency. This is also what
            we plot in Figure 2
        """
        
        tot_Cond = 0
        acc_Cond = 0
        acc_gen1 = 0
        tot_gen1 = 0
        min_uf = 0
        w_uf = 0
        w_sw = 0
        for i,ix in enumerate(test_index):
            og_ix = int(ix/factm)
            pi = perms[ix%factm]
            val = df.iloc[og_ix].values
            # 74 = m*2 + m*2 + m*2 + m*2 + 2 + 4 + m
            # x(64), n1, n2, [w,wfair,gen,exist],uf
            posvec1 = np.reshape(val[m*m: 2*m*m],(m,m))
            posvec2 = np.reshape(val[3*m*m: 4*m*m],(m,m))
            sw1 = posvec_to_sw(posvec1)
            sw2 = posvec_to_sw(posvec2)
            sw = (sw1 + sw2)/(val[4*m*m] + val[4*m*m+1])
            # if(val[4*m*m+5] and val[4*m*m+4]): # this was true when we wanted gen=1
            if(val[4*m*m+5]): # instead we want this now
                if(predictions3[i] == pi[int(val[4*m*m+2])]):
                    acc_Cond += 1
                tot_Cond += 1
            # if((val[4*m*m+4])): # this was true when we wanted gen=1
            if(True):
                uf_og = val[4*m*m+6:4*m*m+6+m]
                w = predictions3[i]
                # print(i, w, pi)
                w_og = pi.index(w)
                min_uf += np.nanmin(uf_og)
                w_uf += uf_og[w_og]
                w_sw += sw[w_og]
                tot_gen1 += 1
        
        print(tot_Cond, acc_Cond/tot_Cond)
        print(w_uf/tot_gen1, min_uf/tot_gen1)
        uf_all.append(w_uf/tot_gen1)
        eff_all.append(acc_Cond/tot_Cond)
        sw_all.append(w_sw/tot_gen1)
        
    return xgboost_all, beta_all, np.array(uf_all), np.array(eff_all), np.array(sw_all)

def just_train(df, n1, n2, m):
    # range of beta for which we learn beta-ML voting rule
    beta_all = np.arange(0,1.01,0.1)
    
    print("\tLearning has started")
    xgboost_all = []
    for beta in beta_all:
        print(f"\t {beta},{n1},{n2},{m}")        
        perms = permutation(list(range(m)))
        
        X = []
        W1 = []
        W2 = []
        Wmix = []
        
        random_idx = []
        
        tic = time()
        
        for row in df.values:
            # feature length = 74 = m**2 + m**2 + m**2 + m**2 + 2 + 4 + 4
            #x(64), n1, n2, [w,wfair,gen,exist],uf
            # beta = 0.8
            data_random = np.random.choice(2,p=[1-beta,beta])
            
            WMG1 = np.reshape(row[:m*m],(m,m))
            posvec1 = np.reshape(row[m*m: 2*m*m],(m,m))
            WMG2 = np.reshape(row[2*m*m: 3*m*m],(m,m))
            posvec2 = np.reshape(row[3*m*m: 4*m*m],(m,m))
            n1 = row[4*m*m] # 64
            n2 = row[4*m*m+1] # 65
            w = int(row[4*m*m+2]) # 66
            wfair = int(row[4*m*m+3]) # 67
            
            gen = int(row[4*m*m+4]) # 68
            exist = int(row[4*m*m+5]) # 69
            
            x = np.concatenate((WMG1.flatten(), posvec1.flatten(), WMG2.flatten(), \
                                posvec2.flatten()))
            x = np.append(x, [n1, n2])
            
            # X.append(x)
            # W1.append(w)
            # W2.append(wfair)
            
            for pi in perms:
                wmg1,pv1,wmg2,pv2 = permute_features(WMG1, posvec1, WMG2, posvec2, pi)       
                x = np.concatenate((wmg1.flatten(), pv1.flatten(), wmg2.flatten(), \
                                    pv2.flatten()))
                x = np.append(x, [n1, n2])
                
                X.append(x)
                W1.append(pi[w])
                W2.append(pi[wfair])
                if(exist):
                    if(w==wfair):
                        Wmix.append(pi[w])
                    else:
                        if(data_random):
                            Wmix.append(pi[w])
                        else:
                            Wmix.append(pi[wfair])
                else:
                    Wmix.append(pi[wfair])
                    
        toc = time()
        print(f'{len(df)} {toc-tic}')
        
        X = np.array(X)
        W1 = np.array(W1)
        W2 = np.array (W2)
        Wmix = np.array(Wmix)
        print(len(X), len(Wmix))
        
            
        #% learning mixedRule using 
              
        # rng = np.random.RandomState(31337)
        # ss = ShuffleSplit(n_splits=1, test_size=0.1, random_state = rng)
        # ss.get_n_splits(X, Wmix)
        # train_index, test_index = next(ss.split(X, Wmix))
        
        clf3 = xgb.XGBClassifier()
        # xgb_model3 = clf3.fit(X[train_index], Wmix[train_index])
        # why not just train on the whole thing?
        xgb_model3 = clf3.fit(X, Wmix)
        xgboost_all.append(xgb_model3)
        
    return xgboost_all

#%%
def read_pref_profile(input_file):
    """
    Parameters
    ----------
    input_file : txt content of input file
    example:
    2
    3
    1 0
    1 0
    0 1
    2
    1 0
    0 1
    
    Returns
    -------
    preference profile
    """
    
    lines = input_file.split('\n')
    m = int(lines[0])
    n1 = int(lines[1])
    g1 = lines[2:2+n1]
    
    votes1 = []
    for line in g1:
        int_vote = [int(x) for x in line.split()]
        votes1.append(int_vote)
    
    n2 = int(lines[2+n1])
    g2 = lines[n1+3:n1+3+n2]
    
    votes2 = []
    for line in g2:
        int_vote = [int(x) for x in line.split()]
        votes2.append(int_vote)
        
    return np.array(votes1), np.array(votes2)

def just_test(xgb_model, X):
    """
    Parameters
    ----------
    xgb_model3 : xgboost classifier learnt in just_train
    X : Input preference profile
    Returns
    -------
    Returns winner for various beta
        Remember to also do this for alpha-fair ML
    """
    votes1, votes2 = read_pref_profile(X)
    
    WMG1, posvec1, WMG2, posvec2 = convert_votes_to_features(votes1, votes2, n1, n2)
    x = np.concatenate((WMG1.flatten(), posvec1.flatten(), WMG2.flatten(), \
                            posvec2.flatten()))
    x = np.append(x, [n1, n2])
    print(x)
    xgb_pred = xgb_model.predict(np.array([x]))
    print(xgb_pred)
    return xgb_pred[0]
    
#%%
def learning_main():
    df = gen_dataset()
    beta, uf, eff = learn_voting_rule(df)
    
    return beta, uf, eff
