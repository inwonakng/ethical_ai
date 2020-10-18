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

    # returns lists of duplicate key and value in tuples.
    def compare(self,othercombo):
        duplicates = []
        for k,c in self.combo.items():
            if othercombo.combo[k] == c: duplicates.append((k,c))
        return duplicates

    def __repr__(self):
        return str(self.combo)
