class LineSemantics:
    def __init__(self):
        self.load_empty = False
        self.load_categories = []
        self.imps = []

class Semantics:
    def __init__(self, matcher):
        self.matcher = matcher
        self.total_weight = 0
        self.stations = {}
        self.bays = []
        self.uld_types = []
        self.imp_seq = {}
        self.imp_debates = []
        self.prev_bay = ('', '')

    def imp_flw(self, iin, ifn):
        queue = [iin]
        while len(queue) > 0:
            ci = queue.pop(0)
            if ci == ifn:
                return True
            if ci in self.imp_seq:
                queue += self.imp_seq[ci]
        return False

def ftoc(f):
    return (f-32)*5/9

def backmatch_suggest(bm, suggestions):
    if 'wrong' in bm:
        bm['possible'] += suggestions
    else:
        bm['wrong'] = True
        bm['possible'] = suggestions


    