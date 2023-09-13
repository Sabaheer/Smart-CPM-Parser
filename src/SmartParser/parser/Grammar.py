from GrammarDesc import GrammarDesc, CPM, CARRIER, ULD
from parser.MatchField import MatchField


class Grammar:
    def __init__(self, grammarDesc:GrammarDesc):
        self.grammarDesc = grammarDesc ## CARRIER

    def add_link(self, progress, field):
        i = progress
        check_forward = False
        while True:
            if self.grammarDesc.rules[i].field_name == field:
                self.grammarDesc.rules[progress].gr_followers.append(self.grammarDesc.rules[i])
                for j in range(i, progress+1):
                    self.grammarDesc.rules[j].repeated = True
                break
            i -= 1
            if not check_forward:
                if i < 0:
                    i = len(self.grammarDesc.rules)-1
                    check_forward = True
            else:
                if i == progress:
                    break

    def buildSyntaxTree(self): # Check the leftover rules
        if not self.grammarDesc.rules[0].gr_start:
            self.grammarDesc.rules[0].gr_start = True ## Rule 0 Airline designator ## Airline designator==true
            if len(self.grammarDesc.rules) <= 1:
                return

            for i in range(len(self.grammarDesc.rules)-1):
                for field in self.grammarDesc.rules[i].link_to:
                    self.add_link(i, field)
                for j in range(i+1, len(self.grammarDesc.rules)):
                    self.grammarDesc.rules[i].gr_followers.append(self.grammarDesc.rules[j])
                    if self.grammarDesc.rules[j].type == MatchField.MATCH_FIELD_MANDATORY:
                        break
            for field in self.grammarDesc.rules[-1].link_to:
                self.add_link(len(self.grammarDesc.rules)-1, field)
        return self

def testing(gt):
    print("test")
    for r in gt.grammarDesc.rules:
        print("--", r.field_name,"--")
        for f in r.gr_followers:
            print(f.field_name)
#testing(Grammar(CARRIER).buildSyntaxTree())
