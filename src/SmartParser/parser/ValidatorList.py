from parser.Validator import Validator
from Levenshtein import distance as levenshtein_distance

class ValidatorList(Validator):
    def __init__(self, values):
        self.values = values

    def tryToFix(self, toBeValidated):
        return None

    def distance(self, toBeValidated):
        distances = []
        for value in self.values:
            distances += [(levenshtein_distance(value, toBeValidated), value)]
            # print(value, toBeValidated, levenshtein_distance(value, toBeValidated))
        distances.sort(key=lambda tup: tup[0])
        
        #if distances[0][0] != distances[1][0]:
        #    return distances[0][1]

        #if len(distances) > self.POSSIBILITIES:
        tmp = []
        for i in range(5):
            tmp += [distances[i][1]]
        return tmp



    def validate(self, toBeValidated):
        if toBeValidated in self.values:
            return {"CODE": self.CODE_ACCEPT}

        correct = self.distance(toBeValidated)
        #correct = self.tryToFix(toBeValidated)
        if len(correct) == 1:
            #print("correcting")
            return {"CODE": self.CODE_REPLACE, "NEW_VALUE": correct}
        else:
            return {"CODE": self.CODE_SUGGEST, "VALUE": correct}

        return {"CODE": self.CODE_REJECT}