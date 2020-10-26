from random import randint as rint
from generation.Combo import Combo

class Category():
    def __init__(self, name, options):
        if len(name) == 0:
            raise 'Category name must be filled'
        if len(options) == 0:
            raise 'Category {} is empty'.format(name)

        self.name = name
        self.is_range = 'range' in options
        self.options = options
        # if options.get('range'):
            # self.__permutate_range(
            #     options['range'][0], options['range'][1], options['unit'])
        if not self.is_range:
            '''
                We should not make value a set.
                The value itself should not be dumplicate when come in
            '''
            self.keys = list(options.keys())
            self.total_option_index_length = len(options) - 1

    def index(self):
        return self.total_option_index_length

    def getKeys(self):
        return self.keys

    def getValue(self, index):
        return self.options[index]

    def get_range(self):
        # what are you doing!
        if not self.is_range: return False
        rng = self.options['range']
        unit = self.options['unit']
        return str(rint(rng[0],rng[1])) + unit
        
    def translate(self,combo):
        vals = combo.getCombo()
        idx = vals[self.name]
        vals[self.name] = self.options[idx]
        return Combo(vals)

