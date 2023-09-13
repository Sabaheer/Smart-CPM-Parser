from parser import helper, GrammarDesc
from parser.Corrector import Corrector
from parser.Rule import Rule


class Parser:

    def __init__(self):
        self.backmatches = None
        self.lines = []

        self.header = None
        self.res_carrier = None
        self.res_uld = []
        self.res_blk = []
        self.si = []

       # self.preparsed_lines = [] # it was never used


    def parse_text(self, text):
        self.lines = text.split("\n")
        self.remove_empty_lines() # we need to remove empty spaces/lines
        from PreParser import PreParser 
        preparser = PreParser() # use preparser to identify regions
        self.lines = preparser.preparse_engine(self.lines) # output of the preparser
        print("After preparse:", self.lines)
        self.backmatches = []
        self.backmatches += [[{"part":"CPM"}]]
        self.parse_header()
        self.parse_carrier()

        bulk = False
        while len(self.lines) > 0:
            res, bulk = self.parse_load(bulk)
            #if not res:
            #    break

        res = {"Header": self.header, "Carrier": self.res_carrier, "ULDs": self.res_uld, "Bulks": self.res_blk, "SI": []}

        if preparser.SI_content:
            res["SI"] = preparser.SI_content

        return res

    def parse_file(self, filename): 
        text = helper.load_file_simple(filename)
        return self.parse_text(text)


    def remove_empty_lines(self): # it removes all the empty lines. 
        res = []
        for line in self.lines:
            tmp = line.strip()
            if len(tmp) > 0:
                res += [line.strip()]

        self.lines = res

    def show(self, text, result):
        pass
        #print(f"{text} --> {result}")


    def parse_header(self): # parse header (CPM)
        line = self.pop()
        if not line:
            return None

        result, backmatch = self.parse_line(line, GrammarDesc.CPM)

        self.show(line, result)
        self.header = result
        return result

    def pop(self):
        if len(self.lines) > 0:
            return self.lines.pop(0)
        else:
            return None

    def parse_line(self, line, grammar): # it uses the rule and grammar to parse each line
        rule = Rule(grammar)
        result = rule.match_line(line)


        # first we check if there is no result
        if not result:
            corrector = Corrector() # it uses the fix function from the corrector function to get fixed value
            fixedValue = corrector.fix(line, grammar)
            if fixedValue:
                result = rule.match_line(fixedValue)
        # if it is still no result then we return None
        if result == None:
            return (None, None)

        return (result, rule.backmatch)

    def parse_load(self, bulk): # it parses the ULD using Grammar Desc.
        line = self.pop()
        if not line:
            return None

        result, backmatch = self.parse_line(line, GrammarDesc.BLK)
        if not bulk:
            if result:
                bulk = True
            else:
                result, backmatch = self.parse_line(line, GrammarDesc.ULD)

        if result:
            if bulk:
                self.res_blk += [result]
            else:
                self.res_uld += [result]
            self.backmatches += [backmatch]
        else:
            self.backmatches += [[{"part": line, "allwrong": True}]]
        self.show(line, result)
        return result, bulk


    def parse_carrier(self):

        line = self.pop()
        if not line:
            return None
        result, backmatch = self.parse_line(line, GrammarDesc.CARRIER)
        if result:
            self.res_carrier = result
            self.backmatches += [backmatch]
        self.show(line, result)

        return result