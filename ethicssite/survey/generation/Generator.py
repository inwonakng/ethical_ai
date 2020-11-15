from .Category import Category
from .Rule import Rule
from .Combo import Combo
from random import sample, randint
from pathlib import Path
from itertools import combinations as comb
# from ..models import RuleSet
import yaml
from ..models import *


class Generator():
    def __init__(self, adaptive=False, rule={}, rule_model=None, plain_text_scenarios=None):

        # assign attributes
        self.adaptive = adaptive
        self.categories = {}
        self.range_categories = {}
        self.bad_combos = []
        self.config = {}

        # collection of scenarios, if it exists
        self.plain_text_scenarios = plain_text_scenarios

        # index bound of collection that still hasn't been picked
        # [yet to pick elements, hat, already picked]
        self.hat = len(plain_text_scenarios) - 1

        # if plain_text_scenarios is not None, then use this to get scenarios.
        return

        # if rule dictionary (passed in) is empty
        if len(rule) == 0:

            # if rule_model is a RuleSet model AND the model is not empty
            if (type(rule_model) == RuleSet) and (len(rule_model.object_form()) > 0):
                rule = rule_model.object_form()
                print('i am using model!!!')

            # if rule model is empty
            # else:
            #     # DEFAULT to the rules.json file
            #     rule = {}
            #     with open(str(Path("survey/generation/rule/rule.yaml").resolve()), "r") as stream:
            #         try:
            #             rule = yaml.safe_load(stream)
            #         except yaml.YAMLError as exc:
            #             print(exc)

        self.config['same_categories'] = rule['config'].get(
            'same_categories', -1)
        self.config['scenerio_size'] = rule['config'].get('scenerio_size', 2)

        for key, value in rule['categories'].items():
            cc = Category(name=key, options=value)
            if cc.is_range:
                self.range_categories[key] = cc
            else:
                self.categories[key] = cc

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

        # Random pick from hat if plain_text_scenarios is not None
        if not self.plain_text_scenarios == None:
            if self.hat == -1:
                self.hat = len(self.plain_text_scenarios) - 1
            ridx = randint(0, self.hat)
            self.plain_text_scenarios[ridx], self.plain_text_scenarios[self.hat] = \
                self.plain_text_scenarios[self.hat], self.plain_text_scenarios[ridx]
            self.hat -= 1
            return self.plain_text_scenarios[self.hat + 1]

        selected = []
        while True:
            s = sample(self.combos, self.config['scenerio_size'])
            for ss in s:
                for k, v in self.range_categories.items():
                    ss.attach(k, v.get_range())
            if self.check_duplicates(s):
                selected = s
                break
        for c in self.categories.values():
            selected = [c.translate(ss) for ss in selected]

        return [ss.getCombo() for ss in selected]

    def permutate_combos(self):
        # initialize array to fill
        self.combos = []
        # Calculate all keys for category ONLY IF THEY ARE NOT RANGE!
        temp_keys = dict([(k, c.getKeys())
                          for k, c in self.categories.items()])
        self.__recursive_permutation(temp_keys)
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
