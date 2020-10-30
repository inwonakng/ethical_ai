class Combo():
    def __init__(self, value={}):
        self.combo = value

    @classmethod
    def fromList(cls, ls):
        opt = {}
        for name, key in ls:
            opt[name] = key
        return cls(value=opt)

    def attach(self,name,value):
        self.combo[name] = value

    def getCombo(self):
        return self.combo

    def getExtended(self, listOfCategories):
        opt = {}
        for key, value in self.combo.items():
            opt[key] = listOfCategories[key].getValue(value)
        return opt

    # Count same number of same Keys between two combo
    def sameKey(self, other):
        i = 0
        for k in self.combo:
            if self.combo[k] == other.combo[k]:
                i += 1

        return i

    # returns lists of duplicate key and value in tuples.
    def compare(self, othercombo):
        duplicates = []
        for k, c in self.combo.items():
            if othercombo.combo[k] == c:
                duplicates.append((k, c))
        return duplicates

    def __repr__(self):
        return str(self.combo)
