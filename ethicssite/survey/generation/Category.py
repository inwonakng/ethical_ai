from random import choice
import numpy as np

class Category():
    operations = {
        'range': lambda x: [i for i in range(x[0],x[1]+1)]
    }

    def __init__(self, name, options):
        if len(name) == 0:
            raise 'Category name must be filled'
        if len(options) == 0:
            raise 'Category {} is empty'.format(name)
        self.name = name
        self.display_unit = ''

        toparg = list(options.keys())[0]
        topvals = list(options.values())[0]
        if toparg in self.operations:
            self.options = set(self.operations[toparg](topvals))
            self.display_unit = list(options.values())[1]
        
        else: self.options = set(options.values())

        # counter
        self.keys = options.keys()
        self.total_option_index_length = len(options) - 1

    def index(self):
        return self.total_option_index_length

    def getKeys(self):
        return self.keys

    def getnext(self,rules,combo_sofar):
    # rules is a list of Rule objects. 
    # iterate through them and return a list of values that don't match the rules

        # for each value in combo, check for rule that applies
        all_rulsets = [r.check(combo_sofar,self.options) for r in rules]     
        not_allowed = set.intersection(*map(set,all_rulsets))
        return str(choice(list(self.options - not_allowed))) + self.display_unit
