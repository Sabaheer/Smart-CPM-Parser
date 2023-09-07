class RegionMatch:
    def __init__(self, configuration, matchList):
        self.configuration = configuration
        self.matchList = matchList

    def cnt_unmatched(self): # it checks every matchRes and if it is equal to None, it decreases the score otherwise it returns score
        # [[a,b,c],[d,e,f]] length is 6x
        score = len(self.matchList)
        for match in self.matchList:
            # print("------", match)
            for matchRes in match[1]: #b = [None, 1,2,3]
                if matchRes != None: # if matches
                    score -= 1
                    break
        # print("score", score)
        return score


class RegionMatcher:
    def __init__(self):
        self.matches = []

    def addMatch(self, match:RegionMatch): # It adds a match to the matches
        self.matches += [match]

    def find_best_match(self)->RegionMatch: # it finds the best mach by score list. 
        print("searching for the best match")
        score_list = []
        for match in self.matches:
            score = match.cnt_unmatched()
            score_list += [(match, score)]

        if len(score_list) > 0:
            score_list.sort(key=lambda tup: tup[1]) #sort by score
            print(score_list)
            return score_list[0][0] # return the top most score

        return None







