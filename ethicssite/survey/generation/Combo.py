class Combo():
    def __init__(self, value={}):
        self.combo = value

    @classmethod
    def fromList(cls, ls):
        opt = {}
        for name, key in ls:
            opt[name] = key
        return cls(value=opt)

    def getCombo(self):
        return self.combo

    def getExtended(self, listOfCategories):
        opt = {}
        for key, value in self.combo.items():
            opt[key] = listOfCategories[key][value]
        return opt
