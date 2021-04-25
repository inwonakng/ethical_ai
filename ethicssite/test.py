from survey.pref_pl.plackettluce import *
from survey.pref_pl.egmm_mixpl import *

#%% create sample pref_profile and output to text file

n = 100
m = 4
useDirichlet = False

with open('sample_output.txt','w') as outfile:
    # what this does in generate a new dataset with random parameters
    # gamma is initalized randomly, gamma, a m-length vector is the parameters for the PL
    # using gamma, a preference profile with n votes are created
    gamma, votes = generate_pl_dataset(n, m, useDirichlet)
    # outfile.write(str(len(gamma)) + ',' + str(len(votes)) + '\n')
    # outfile.write(','.join(map(str, gamma)) + '\n')
    
    # I'm only outputting the votes
    # votes is essentially a n*m matrix. A list of n votes (i.e. n rankings over m alternatives)
    for vote in votes:
        outfile.write(','.join(map(str, vote)) + '\n')
        
#%% read in file and learn pl parameters (not a mixture of PL, i.e. k=1)

with open('sample_output.txt','r') as infile:
    txt = infile.read()
    lines = txt.split('\n')
    votes = []
    for l in lines[:-1]:
        # recreating the preference profile from the output
        votes.append([int(x) for x in l.split(',')])
    print(votes)

rslt = egmm_mixpl(np.array(votes), m, k = 1, itr = 20)

# for 1-PL, rslt has shape (1,m+1). rslt[0][0] = 1
# in general, in rslt, the alpha values are the mixture coefficients. Suppose, in a 2-PL with
#   mixture coefficients 0.6, 0.4, alpha would be 0.6,0.4 
#   So, rslt would store the alpha values, and the gamma values for each mixture
# But we care about only one parameter, so one set of gamma is enough
# after that, the rest of the rslt stores the PL parameters

print('Learned PL parameters:',rslt[0][1:])
