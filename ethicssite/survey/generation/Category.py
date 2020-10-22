class Category():
    def __init__(self, name, options):
        if len(name) == 0:
            raise 'Category name must be filled'
        if len(options) == 0:
            raise 'Category {} is empty'.format(name)

        self.name = name
        if options.get('range'):
            self.__permutate_range(
                options['range'][0], options['range'][1], options['unit'])
        else:
            '''
                We should not make value a set.
                The value itself should not be dumplicate when come in
            '''
            self.options = options
            self.keys = list(options.keys())
            self.total_option_index_length = len(options) - 1

    def __permutate_range(self, min, max, unit=""):
        self.options = {}
        for i in range(min, max + 1):
            self.options[i] = str(i) + unit
        self.keys = list(self.options.keys())
        self.total_option_index_length = len(self.options) - 1

    def index(self):
        return self.total_option_index_length

    def getKeys(self):
        return self.keys

    def getValue(self, index):
        return self.options[index]
