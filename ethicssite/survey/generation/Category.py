class Category():
    def __init__(self, name, options):
        if len(name) == 0:
            raise 'Category name must be filled'
        if len(options) == 0:
            raise 'Category {} is empty'.format(name)
        self.name = name
        self.options = options

        # counter
        self.keys = options.keys()
        self.total_option_index_length = len(options) - 1

    def index(self):
        return self.total_option_index_length

    def getKeys(self):
        return self.keys

    def getValue(self, key):
        if key not in self.keys:
            raise "{} was not in Catagory {}".format(key, self.name)
        return self.options[key]

    def __getitem__(self, key):
        return self.getValue(key)
