class RegionMatch:
    def __init__(self, configuration, matchList):
        self.configuration = configuration
        self.matchList = matchList

    def cnt_unmatched(self):

        score = len(self.matchList)
        for match in self.matchList:
            # print("------", match)
            for matchRes in match[1]:
                if matchRes != None:
                    score -= 1
                    break
        # print("score", score)
        return score


class RegionMatcher:
    def __init__(self):
        self.matches = []

    def addMatch(self, match:RegionMatch):
        self.matches += [match]

    def find_best_match(self)->RegionMatch:
        print("searching for the best match")
        score_list = []
        for match in self.matches:
            score = match.cnt_unmatched()
            score_list += [(match, score)]

        if len(score_list) > 0:
            score_list.sort(key=lambda tup: tup[1])
            print(score_list)
            return score_list[0][0]

        return None







