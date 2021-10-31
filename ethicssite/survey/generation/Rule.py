class Rule():
    def __init__(self, value):
        '''
        value: dictionary object containing [feature][value][some feature]: [list of bad option to choose]
        '''
        if len(value) == 0:
            raise 'Rule is empty'
        self.bad_combos = value

    def getBadRuleFromCategory(self, category):
        return self.bad_combos.get(category)

    # def check(self, combo, nextcateg):
    #     bad = set()
    #     for feat, val in combo:
    #         if feat in self.bad_combos and val in self.bad_combos[feat]:
    #             # if the rule has anything to say
    #             lookout = self.bad_combos[feat]
    #             bad |= set(lookout[nextcateg.name])
    #         else:
    #             continue
    #     return list(bad)
