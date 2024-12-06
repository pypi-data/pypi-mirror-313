class CustDict(dict):

    def update(self, key, value):
        self[key] = value if key in self else None

    def insert(self, key, value):
        self[key] = value if key not in self else None

#==========================================================
