class Rule():
    def __init__(self, category, value):
        '''
        value: dictionary object containing [feature][value][bad combinations]
        '''
        if len(value) == 0:
            raise 'Rule is empty'
        self.bad_combos = value
        self.id = value.keys()

    def check(self,combo,nextcateg):
        bad = set()
        for feat,val in combo:
            if feat in self.bad_combos and val in self.bad_combos[feat]:
                # if the rule has anything to say
                lookout = self.bad_combos[feat]
                bad |= set(lookout[nextcateg.name]) 
            else: continue
        return list(bad)
