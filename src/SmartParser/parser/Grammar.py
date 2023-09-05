from GrammarDesc import GrammarDesc
from parser.MatchField import MatchField


class Grammar:
    def __init__(self, grammarDesc:GrammarDesc):
        self.grammarDesc = grammarDesc

    def get_following(self, field:MatchField): # Check in grammarDesc for field name and if it depends on anything just add it.
        folowing = []
        for item in self.grammarDesc.rules:

            if field.field_name in item.depends_on: # we search in a sequence that we can find on the graph. 
                folowing += [item]
        return folowing

    def buildSyntaxTree(self): # Check the leftover rules 

        self.grammarDesc.rules[0].gr_start = True
        for item in self.grammarDesc.rules:
            item.gr_followers = self.get_following(item)
