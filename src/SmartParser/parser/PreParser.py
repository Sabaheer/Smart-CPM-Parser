import copy

from Parser import Parser
from RegionMatcher import RegionMatcher, RegionMatch
from parser import helper, GrammarDesc # helper is never called



class PreparseResult(): # this class was never used. 
    def __init__(self, preparsed_lines):
        self.preparsed_lines = preparsed_lines


class PreParser():
    def __init__(self):
        super().__init__()
        self.SI_content = None
        self.header_pos = None
        self.SI_pos = None

        self.unparsable_regions = None
        self.preparsed_lines = []
        self.parser = Parser()

    def findHeader(self): # first we check where is "CPM" so we can start parsing
        for i in range(len(self.lines)):
            if self.lines[i] == "CPM":
                self.header_pos = i

    def findSI(self): # second we search for the location of SI
        for i in range(len(self.lines)):
            if "SI" in self.lines[i].split(" ")  :
                self.SI_pos = i

    def find_SI_content(self): # by using the SI location we separate the content from ULD content
        if self.SI_pos and self.SI_pos > 0:
            self.SI_content = self.lines[self.SI_pos:]




    def preparse_engine(self, lines): # PreParse engine function does 3 things
        self.lines = lines
        self.findHeader() # it finds the header (CPM)
        self.findSI() # identifies the location of SI
        self.find_SI_content() # separate the SI content from the header and ULD
        if self.header_pos == None:
            return []

        body_lines = self.split_hyphen() 
        SI = []
        self.to_be_preparsed_lines = body_lines + SI
        self.preparsed_lines = self.preparse()

        self.unparsable_regions = self.identify_unparsable_regions(self.preparsed_lines) # returned res
        self.try_to_join_regions() # removed temprarily

        if self.SI_content:
            SI = self.SI_content
        return ["CPM"]+body_lines# + SI # it is sent to the parser.

    def split_hyphen(self):
        tmp_list = [self.lines[self.header_pos+1]]
        up = len(self.lines)
        if self.SI_pos:
            up = self.SI_pos
        for j in range(self.header_pos+1,up):
            
            segs = self.lines[j].split('-')

            for i in range(len(segs)):
                segs[i] = '-'+segs[i]

            tmp_list += (segs[1:])
        return tmp_list

    def try_to_join_regions(self): # region: a list of consecutive line indexes not parsable
        # it only adds regions if they are less than five indexes 
        # Prepend previous index if first index greater than zero. 

        for region in self.unparsable_regions:
            if len(region) <= 5:
                if region[0] > 0: # region = [5,6,7] -> [4,5,6,7]
                    self.join_region([region[0]-1]+region) 
                else:
                    self.join_region(region)

    

    def join_region(self, region:list):
        self.region_matcher = RegionMatcher()
        self._join_region(region, [])

        best_match = self.region_matcher.find_best_match()

        print("Ok Best match: ",best_match.configuration)

        print("-----")
        for line in self.to_be_preparsed_lines:
            print(line)
        self.fillMatch(best_match)

        print("-----")
        for line in self.to_be_preparsed_lines:
            print(line)


    def fillMatch(self, match:RegionMatch):

        for i in range(len(match.configuration)):
            region = match.configuration[i]
            for j in region:
                self.to_be_preparsed_lines[j]=""
            self.to_be_preparsed_lines[region[0]] = match.matchList[i][0] # here is where preparser is effecting the parser. 

 # self._join_region(       region,         [])
 # recursive function: match different combinations of unparsable regions using 2 grammar rules, 
 # find the match with best score
    def _join_region(self, avaliable_field, region):

        if len(avaliable_field) == 0:
            matches = []
            for r in region:
                s = ""
                for sr in r: # r is [1,2,3]
                    s += self.to_be_preparsed_lines[sr]
                matchRes = self.parse_line_magic(s, [GrammarDesc.CARRIER, GrammarDesc.ULD])

                matches += [(s, matchRes)]
            self.region_matcher.addMatch(RegionMatch(region, matches))

            return

        newregion = copy.deepcopy(region)
        newregion = newregion + [[avaliable_field[0]]]
        self._join_region(avaliable_field[1:], newregion)

        newregion = copy.deepcopy(region)
        if len(region) > 0:
            newregion[-1] += [avaliable_field[0]]
            self._join_region(avaliable_field[1:], newregion)

    # preparsed_lines =[{result1}, {result2}, None, None, {result3}, {result4}, None, {result5}]
    # this function creates a list of all the non-parseable regions index. 
    def identify_unparsable_regions(self, preparsed_lines)->list:
        res = []

        buf = [] # it is a list of index of None in preparsed_lines
        for i in range(len(preparsed_lines)): # 3
            if preparsed_lines[i] == None: # 
                if len(buf) == 0: # yes zero
                    buf += [i] # buf = [2]
                else: # buf not zero
                    if buf[-1] == i-1: # 
                        buf += [i]
                    else:
                        res += [buf] #[[1], [3,4,5], [8]]
                        buf = [i] #[3]
        if len(buf) > 0:
            res += [buf]

        return res

    def parse_line_magic(self, line, grammars):
        res = []
        # For each grammar, parse the line and add the result
        for grammar in grammars:
            res += [self.parser.parse_line(line, grammar)[0]] # only extract the first output of parseline

        return res


    def preparse(self):
        '''
        Identify not parsable lines
        :param lines:
        :return:
        '''
        print("preparse")

        i = 0
        header = None
        carrier = None
        ulds = []
        preparsed_lines = []

        while i < len(self.to_be_preparsed_lines):
            line = self.to_be_preparsed_lines[i]

            tmp_carrier = None
            tmp_uld = None
            result = None

            tmp_carrier, backmatch = self.parser.parse_line(line, GrammarDesc.CARRIER) # identifies carrier by using parse line and the grammar description of the carrier
            if tmp_carrier: # (if none does nothing) otherwise stores it in result
                carrier = tmp_carrier
                result = carrier
                print("carrier found!")

            tmp_uld, backmatch = self.parser.parse_line(line, GrammarDesc.ULD) # identifies uld by using grammar description of the ULD. 
            if tmp_uld: # (if none does nothing) otherwise stores it in result
                result = tmp_uld
                ulds += [tmp_uld]
                #print("uld found", line)

            if result:  # if result exits  add it to the parse lines
                preparsed_lines += [result]
            else:
                print("Invalid line", line)
                preparsed_lines += [None] 
            i += 1

        print(preparsed_lines)
        #self.join(lines, parsing_result)
        return preparsed_lines # this is never used. 


