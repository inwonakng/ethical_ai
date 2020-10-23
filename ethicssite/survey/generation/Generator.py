from .Category import Category
from .Rule import Rule
from .Combo import Combo
from random import sample

from itertools import combinations as comb


class Generator():
    def __init__(self, adaptive=False, rule={}):
        if len(rule) == 0:
            raise "Rule is empty"
        elif len(rule['categories']) == 0:
            raise "Categories is empty"
        # assign attributes
        self.adaptive = adaptive
        self.categories = {}
        self.bad_combos = []
        self.config = {}
        self.config['same_categories'] = rule['config'].get(
            'same_categories', -1)
        self.config['scenerio_size'] = rule['config'].get('scenerio_size', 2)

        for key, value in rule['categories'].items():
            self.categories[key] = Category(name=key, options=value)

        self.categoriesKeys = list(self.categories.keys())
        self.rule = Rule(rule['bad_combos'])

        # Cache result
        self.combos = []
        self.extended_combos = []
        self.scenarios = []

        # Init
        self.permutate_combos()
        # self.extend_combos()

    # should return a dictionary
    def get_scenario(self):
        '''
            random pick
            @TODO we need to record what we have already
            @TODO maybe take too long
        '''
        selected = []
        while True:
            s = sample(self.combos, self.config['scenerio_size'])
            if self.check_duplicates(s):
                selected = s
                break

        return [s.getCombo() for s in selected]

    def permutate_combos(self):
        self.combos = []
        # Calculate all keys for category
        tempCategoryKeys = {}
        for i in self.categories:
            tempCategoryKeys[i] = list(self.categories[i].getKeys())

        self.__recursive_permutation(tempCategoryKeys)

    '''
        @TODO Need docs for this rule
    '''

    def check_duplicates(self, scenario):
        # get all possible pairs to compare duplicates
        tocheck = list(comb(scenario, 2))
        found = {}
        for c1, c2 in tocheck:
            dups = c1.compare(c2)
            for d in dups:
                if not d in found:
                    found[d] = 0
                else:
                    found[d] += 1
        numfound = list(found.values())
        numlen = len(numfound)
        return numlen == 0 or (max(numfound) < self.config['same_categories'] + 1 and numfound.count(self.config['same_categories']) < len(scenario) - 1)

    def __recursive_permutation(self, tempCategoryKeys, stack=[], categoryIndex=0):
        if categoryIndex >= len(self.categories):
            # The end of recursion
            self.combos.append(Combo.fromList(stack))
            return

        currentCategoryKey = self.categoriesKeys[categoryIndex]
        currentName = self.categories[currentCategoryKey].name

        # iterator over current legit option set
        for num in tempCategoryKeys[currentName]:
            stack.append((currentName, num))
            bad_rules = self.rule.getBadRuleFromCategory(currentName)  # dict
            if bad_rules:
                for conflict_rule in bad_rules.get(num, {}):
                    # list of combos
                    for conflict_num in bad_rules[num][conflict_rule]:
                        '''
                            The way we are not using set() or similar because we
                            want to keep the sequence of the result.
                            The performance here is similar, as set to list also 
                            takes nlogn.
                            Using dictionary will also give overhead
                        '''
                        tempCategoryKeys[conflict_rule].remove(conflict_num)
            self.__recursive_permutation(
                tempCategoryKeys, stack, categoryIndex + 1)
            # Add back removed index
            if bad_rules:
                for conflict_rule in bad_rules.get(num, {}):
                    # list of combos
                    for conflict_num in bad_rules[num][conflict_rule]:
                        tempCategoryKeys[conflict_rule].append(conflict_num)

            stack.pop()

    def extend_combos(self):
        self.extended_combos = []
        for i in self.combos:
            self.extended_combos.append(i.getExtended(self.categories))