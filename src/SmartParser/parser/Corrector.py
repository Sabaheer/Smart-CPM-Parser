import string

from GrammarDesc import GrammarDesc
from parser.Rule import Rule


class Corrector:
    MAX_CHARACTER_FIX = 5

    def __init__(self):

        self.grammarDesc = None
        self.operators = {".", "-", "/"}

        self.known = []
        self.solutions = []
        self.log = None

    def change(self, s:string, pos:int, ch:string):
        return s[:pos] + ch + s[pos + 1:]

    def remove(self, s: string, pos: int):
        return s[:pos] + s[pos + 1:]

    def canMatch(self, line):
        rule = Rule(self.grammarDesc)
        return rule.match_line(line)


    def try_replace(self, current, unknown_pos:list[int], changes):

        if unknown_pos == []:
            matchResult = self.canMatch(current)
            if matchResult:
                #print(current, matchResult)
                self.solutions += [current]
            return
        for op in ["/", '.', "-"]:
            self.try_replace(self.change(current, unknown_pos[-1], op), unknown_pos[:-1], changes + [f"replaced {unknown_pos[-1]} with {op} "])

        self.try_replace(self.remove(current, unknown_pos[-1]), unknown_pos[:-1], changes + [f"deleted {unknown_pos[-1]} "])

    def fix_more(self):
        self.known = set.union(set(string.ascii_uppercase), set(string.digits))
        self.known = set.union(set(string.ascii_uppercase), set(string.digits))

    def fix(self, line: string, grammarDesc:GrammarDesc):
        line = line.replace(' ', '')
        self.solutions = []
        result = None
        self.known = set.union(set(string.ascii_uppercase), set(string.digits), self.operators)
        #if grammarDesc.name == "ULD":
        #    result = self._fix("-" + line, grammarDesc)

        if result == None:
            result = self._fix(line, grammarDesc)

        return result

    def _fix(self, carrier_line:string, grammarDesc:GrammarDesc):
        self.grammarDesc = grammarDesc
        unknown_pos = self.identifyUnknownPos(carrier_line)

        if len(unknown_pos) > self.MAX_CHARACTER_FIX:
            return None

        self.try_replace(carrier_line, unknown_pos, [])

        if len(self.solutions) == 1:
            return self.solutions[0]

        return None


    def identifyUnknownPos(self, carrier_line, known = []):
        if len(known)==0:
            known = self.known

        unknown = []
        for i in range(len(carrier_line)):
            if carrier_line[i] not in known:
                unknown += [i]

        return unknown


