class LineSemantics:
    def __init__(self):
        self.load_empty = False
        self.load_categories = []
        self.imps = []

class Semantics:
    def __init__(self):
        self.total_weight = 0
        self.stations = {}
        self.bays = []
        self.uld_types = []

def ftoc(f):
    return (f-32)*5/9

def backmatch_suggest(bm, suggestions):
    if 'wrong' in bm:
        bm['possible'] += suggestions
    else:
        bm['wrong'] = True
        bm['possible'] = suggestions


    