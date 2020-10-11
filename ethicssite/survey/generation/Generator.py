from Category import Category
from Rule import Rule
from Combo import Combo


class Generator():
    def __init__(self, adaptive=False, rule={}):
        if len(rule) == 0:
            raise "Rule is empty"
        elif len(rule['categories']) == 0:
            raise "Categories is empty"
        # assign attributes
        self.adaptive = adaptive
        self.categories = {}
        self.bad_combo = []

        for key, value in rule['categories'].items():
            self.categories[key] = Category(name=key, options=value)
        for key, value in rule['bad_combos'].items():
            self.bad_combo.append(Rule(key=key, value=value))

        # Cache result
        self.options = []
        self.extended_options = []

        self.permutate_options()
        self.extend_options()

    def permutate_options(self):
        self.__recursive_permutation([], 0)
        return True

    def __recursive_permutation(self, stack, categoryIndex):
        if categoryIndex >= len(self.categories):
            # The end of recursion
            self.options.append(Combo.fromList(stack))
            return

        ckey = list(self.categories.keys())[categoryIndex]
        name = self.categories[ckey].name
        for key in self.categories[ckey].getKeys():
            stack.append((name, key))
            self.__recursive_permutation(stack, categoryIndex + 1)
            stack.pop()

    def extend_options(self):
        self.extended_options = []
        for i in self.options:
            self.extended_options.append(i.getExtended(self.categories))

    def get_story(self):
        return(['This is scenario 1',
                'This is scenario 2',
                'This is scenario 3'])

    def check_rule(self):
        return
