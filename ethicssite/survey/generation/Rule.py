class Rule():
    def __init__(self, key, value):
        if len(value) == 0:
            raise 'Rule is empty'
        self.combo = value
        self.id = key
