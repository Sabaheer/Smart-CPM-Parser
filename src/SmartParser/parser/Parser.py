from parser import helper, GrammarDesc
from parser.Corrector import Corrector
from parser.Rule import Rule, Segment
from parser.Semantics import Semantics
from parser.Matcher import Matcher
from parser.Keyboard import Keyboard

class Parser:

    def __init__(self):
        self.backmatches = None
        self.lines = []
        self.sem = Semantics(Matcher(Keyboard(1,1), []))

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
        self.backmatches = [[Segment('CPM', 'Header', 'CPM')]]
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

        if None in res.values():
            return res

        #Print semantic information
        print("Total weight:", self.sem.total_weight)
        max_cnt = 0
        max_stn = ""
        for (k,v) in self.sem.stations.items():
            if v > max_cnt:
                max_cnt = v
                max_stn = k
        if len(self.backmatches) >= 3:
            prevbay_bm = None
            for backmatch in self.backmatches[2:]:
                imp_bms = []
                for seg in backmatch:
                    field_name = seg.field
                    match field_name:
                        case 'UnloadingStation' | 'Destination':
                            stn = seg.value
                            if self.sem.stations[stn] == 1 and len(self.backmatches) >= 4:
                                if self.sem.matcher.similar(max_stn, stn):
                                    seg.suggest([max_stn])
                        case 'IMP':
                            imp_bms.append(seg)

                        case 'ULDBayDesignation' | 'Compartment':
                            bay = seg.value
                            num = ''
                            section = ''
                            for i in range(len(bay)):
                                if i == 0:
                                    num += bay[i]
                                elif i == len(bay) - 1 and bay[i].isalpha():
                                    section = bay[i]
                                else:
                                    num += bay[i]
                            usual = ['', 'L', 'R', 'P']
                            if section not in usual:
                                sug = []
                                for u in usual:
                                    sug.append(num+u)
                                seg.suggest(sug)

                            n1 = self.sem.prev_bay[0]
                            s1 = self.sem.prev_bay[1]
                            if n1 != '':
                                if num != n1:
                                    if s1 == 'L':
                                        prevbay_bm.suggest(['Missing '+n1+'R'])
                                    if section == 'R':
                                        seg.suggest(['Missing '+num+'L'])
                                if num == n1:
                                    if s1 == '' or section == '':
                                        seg.suggest(['Is Bay '+num+' divisible?'])
                                    elif s1 == 'L' and section != 'R':
                                        seg.suggest(['Missing '+num+'R'])
                                    elif s1 != 'L' and section == 'R':
                                        prevbay_bm.suggest(['Missing '+num+'L'])
                                elif (((n1.isalpha() and num.isalpha())
                                        or (n1.isdigit() and num.isdigit()))
                                        and num < n1):
                                    if prevbay_bm.field == field_name:
                                        seg.suggest(['Bay should be in ascending order'])


                            self.sem.prev_bay = (num, section)
                            prevbay_bm = seg

                for deb in self.sem.imp_debates:
                    for i in range(len(imp_bms)-1):
                        ii = imp_bms[i].value
                        dj = ""
                        if ii == deb[0]:
                            dj = deb[1]
                        elif ii == deb[1]:
                            dj = deb[0]
                        if len(dj) > 0:
                            for j in range(i, len(imp_bms)):
                                ij = imp_bms[j].value
                                if ij == dj:
                                    sug = ['Detected conflicts in IMP ordering ('+ii+' and '+ij+')']
                                    imp_bms[i].suggest(sug)
                                    imp_bms[j].suggest(sug)

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
        rule = Rule(grammar, self.sem)
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
            seg = Segment(line, None, None)
            seg.allwrong = True
            self.backmatches += [[seg]]
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
