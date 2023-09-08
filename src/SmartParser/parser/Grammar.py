from GrammarDesc import GrammarDesc
from parser.MatchField import MatchField


class Grammar:
    def __init__(self, grammarDesc:GrammarDesc):
        self.grammarDesc = grammarDesc ## CARRIER

    def get_following(self, field:MatchField): # Check in grammarDesc for field name and if it depends on anything just add it.
        following = [] # followers of a field. 
        for item in self.grammarDesc.rules: # We loop through list of rules again to find which one follows field.

            if field.field_name in item.depends_on: # we search in a sequence that we can find on the graph. 
                following += [item]
        
        for i in range(len(following)):
            if following[i].type == MatchField.MATCH_FIELD_MANDATORY:
                following.append(following.pop(i))
                break
        
        return following

    def buildSyntaxTree(self): # Check the leftover rules 

        self.grammarDesc.rules[0].gr_start = True ## Rule 0 Airline designator ## Airline designator==true 
        for item in self.grammarDesc.rules: ## Again loop over carrier rules. 
            item.gr_followers = self.get_following(item) # following is assigned to item.gr_followers. 
