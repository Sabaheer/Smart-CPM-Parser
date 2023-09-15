class LineSemantics:
    def __init__(self):
        self.load_empty = True
        self.load_categories = []
        self.imps = []

class Semantics:
    def __init__(self):
        self.total_weight = 0
        self.stations = {}
        self.bays = []
        self.uld_types = []
        self.lines = []

def ftoc(f):
    return (f-32)*5/9


    