class LineSemantics:
    # Stores semantic information for each line of CPM file
    def __init__(self):
        self.load_empty = False
        self.load_categories = []
        self.imps = []

class Semantics:
    # Stores semantic information across the whole CPM file
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
        # iin: the initial IMP code; ifn: the final IMP code
        # The function checks whether ifn appears after iin based on IMP orderings across the CPM file
        queue = [iin]
        while len(queue) > 0:
            ci = queue.pop(0) # ci: the current IMP code
            if ci == ifn:
                return True
            if ci in self.imp_seq:
                queue += self.imp_seq[ci]
        return False

def ftoc(f):
    return (f-32)*5/9



    